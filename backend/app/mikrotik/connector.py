"""
MikroTik RouterOS Connector
Handles connections and communication with MikroTik routers
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from routeros_api import RouterOsApi
import paramiko
from app.core.config import settings

logger = logging.getLogger(__name__)


class MikroTikConnector:
    """
    Connector for MikroTik RouterOS
    Supports both API and SSH connections
    """
    
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        api_port: int = 8728,
        ssh_port: int = 22
    ):
        self.host = host
        self.username = username
        self.password = password
        self.api_port = api_port
        self.ssh_port = ssh_port
        self.api_connection: Optional[RouterOsApi] = None
        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.connected = False
        self.connection_type: Optional[str] = None
    
    async def connect(self, use_api: bool = True):
        """Connect to router"""
        try:
            if use_api:
                await self._connect_api()
            else:
                await self._connect_ssh()
            
            self.connected = True
            logger.info(f"? Connected to router {self.host}")
            
        except Exception as e:
            logger.error(f"? Failed to connect to router {self.host}: {e}")
            self.connected = False
            raise
    
    async def _connect_api(self):
        """Connect using RouterOS API"""
        try:
            loop = asyncio.get_event_loop()
            self.api_connection = await loop.run_in_executor(
                None,
                lambda: RouterOsApi(
                    self.host,
                    username=self.username,
                    password=self.password,
                    port=self.api_port,
                    use_ssl=False,
                    plaintext_login=True
                )
            )
            self.connection_type = "api"
            
            # Test connection
            await loop.run_in_executor(
                None,
                lambda: self.api_connection.get_resource("/system/resource").get()
            )
            
        except Exception as e:
            logger.error(f"API connection failed: {e}")
            raise
    
    async def _connect_ssh(self):
        """Connect using SSH"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.ssh_client.connect(
                    self.host,
                    port=self.ssh_port,
                    username=self.username,
                    password=self.password,
                    timeout=10
                )
            )
            
            self.connection_type = "ssh"
            
        except Exception as e:
            logger.error(f"SSH connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from router"""
        try:
            if self.api_connection:
                self.api_connection.disconnect()
                self.api_connection = None
            
            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None
            
            self.connected = False
            self.connection_type = None
            logger.info(f"?? Disconnected from router {self.host}")
            
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected"""
        return self.connected
    
    async def execute_command(
        self,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute a RouterOS command
        
        Args:
            command: RouterOS command path (e.g., "/system/resource/print")
            parameters: Optional parameters dictionary
        
        Returns:
            Command result
        """
        if not self.connected:
            raise Exception("Not connected to router")
        
        try:
            if self.connection_type == "api":
                return await self._execute_api_command(command, parameters)
            elif self.connection_type == "ssh":
                return await self._execute_ssh_command(command, parameters)
            else:
                raise Exception("Unknown connection type")
                
        except Exception as e:
            logger.error(f"Error executing command {command}: {e}")
            raise
    
    async def _execute_api_command(
        self,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Execute command via API"""
        try:
            loop = asyncio.get_event_loop()
            
            # Parse command path
            parts = command.strip("/").split("/")
            resource_path = "/" + "/".join(parts[:-1])
            action = parts[-1] if parts else "print"
            
            def execute_sync():
                resource = self.api_connection.get_resource(resource_path)
                
                if action == "print":
                    result = resource.get()
                    return result if isinstance(result, list) else [result]
                elif action == "add":
                    if parameters:
                        return resource.add(**parameters)
                    return resource.add()
                elif action == "set":
                    # Extract ID from parameters
                    params_copy = parameters.copy() if parameters else {}
                    item_id = params_copy.pop("id", None)
                    if item_id and params_copy:
                        return resource.set(id=item_id, **params_copy)
                    return None
                elif action == "remove":
                    item_id = parameters.get("id") if parameters else None
                    if item_id:
                        return resource.remove(id=item_id)
                    return None
                else:
                    # Generic method call
                    method = getattr(resource, action, None)
                    if method:
                        if parameters:
                            return method(**parameters)
                        return method()
                    else:
                        # Fallback to print
                        return resource.get()
            
            return await loop.run_in_executor(None, execute_sync)
                    
        except Exception as e:
            logger.error(f"API command execution error: {e}")
            raise
    
    async def _execute_ssh_command(
        self,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """Execute command via SSH"""
        try:
            # Build command string
            cmd_str = command
            if parameters:
                param_str = " ".join([f"{k}={v}" for k, v in parameters.items()])
                cmd_str = f"{command} {param_str}"
            
            loop = asyncio.get_event_loop()
            stdin, stdout, stderr = await loop.run_in_executor(
                None,
                lambda: self.ssh_client.exec_command(cmd_str)
            )
            
            output = stdout.read().decode("utf-8")
            error = stderr.read().decode("utf-8")
            
            if error:
                raise Exception(f"SSH command error: {error}")
            
            return output
            
        except Exception as e:
            logger.error(f"SSH command execution error: {e}")
            raise
    
    async def execute_script(self, script: str) -> Dict[str, Any]:
        """
        Execute a RouterOS script
        
        Args:
            script: RouterOS script content
        
        Returns:
            Execution result
        """
        if not self.connected:
            raise Exception("Not connected to router")
        
        try:
            if self.connection_type == "api":
                # Execute script via API
                loop = asyncio.get_event_loop()
                def run_script():
                    script_resource = self.api_connection.get_resource("/system/script")
                    return script_resource.run(script=script)
                
                result = await loop.run_in_executor(None, run_script)
                return {
                    "status": "success",
                    "result": result
                }
            elif self.connection_type == "ssh":
                # Execute script via SSH
                loop = asyncio.get_event_loop()
                stdin, stdout, stderr = await loop.run_in_executor(
                    None,
                    lambda: self.ssh_client.exec_command(
                        f"/system/script/run source=[/system/script add name=temp_script source=\"{script}\"]"
                    )
                )
                
                output = stdout.read().decode("utf-8")
                error = stderr.read().decode("utf-8")
                
                if error:
                    return {
                        "status": "error",
                        "error": error
                    }
                
                return {
                    "status": "success",
                    "result": output
                }
            else:
                raise Exception("Unknown connection type")
                
        except Exception as e:
            logger.error(f"Error executing script: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        try:
            resource_data = await self.execute_command("/system/resource/print")
            
            if isinstance(resource_data, list) and len(resource_data) > 0:
                return resource_data[0]
            elif isinstance(resource_data, dict):
                return resource_data
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}
    
    async def get_interfaces(self) -> List[Dict]:
        """Get interface list"""
        try:
            interfaces = await self.execute_command("/interface/print")
            return interfaces if isinstance(interfaces, list) else [interfaces]
        except Exception as e:
            logger.error(f"Error getting interfaces: {e}")
            return []
    
    async def get_ip_addresses(self) -> List[Dict]:
        """Get IP addresses"""
        try:
            addresses = await self.execute_command("/ip/address/print")
            return addresses if isinstance(addresses, list) else [addresses]
        except Exception as e:
            logger.error(f"Error getting IP addresses: {e}")
            return []
