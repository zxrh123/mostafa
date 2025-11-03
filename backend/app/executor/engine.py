"""
Executor Engine - Safe execution of RouterOS commands and scripts
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from app.core.config import settings
from app.ai.brain import AIBrain
from app.mikrotik.connector import MikroTikConnector
from app.models.execution import ExecutionLog

logger = logging.getLogger(__name__)


class ExecutorEngine:
    """
    Executor Engine for safely executing RouterOS commands
    Includes dry-run, rollback, and logging capabilities
    """
    
    def __init__(self, ai_brain: Optional[AIBrain] = None):
        self.ai_brain = ai_brain
        self.ready = True
        self.execution_history: List[Dict] = []
        self.snapshots: Dict[str, Dict] = {}
        
    def is_ready(self) -> bool:
        """Check if executor is ready"""
        return self.ready
    
    async def execute_script(
        self,
        router_id: str,
        script: str,
        connector: MikroTikConnector,
        dry_run: bool = True,
        require_confirmation: bool = True,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a RouterOS script safely
        
        Args:
            router_id: Router identifier
            script: RouterOS script to execute
            dry_run: If True, only validate without executing
            require_confirmation: If True, require user confirmation
            user_id: User who requested execution
        
        Returns:
            Execution result with status and details
        """
        execution_id = f"exec_{datetime.now().timestamp()}"
        
        try:
            # Create snapshot before execution
            if not dry_run:
                snapshot = await self._create_snapshot(router_id, connector)
                self.snapshots[execution_id] = snapshot
            
            # Validate script
            validation_result = await self._validate_script(script)
            if not validation_result["valid"]:
                return {
                    "execution_id": execution_id,
                    "status": "validation_failed",
                    "error": validation_result.get("error", "Script validation failed"),
                    "dry_run": dry_run
                }
            
            # Execute script
            if dry_run:
                # Dry run - just validate
                result = {
                    "execution_id": execution_id,
                    "status": "dry_run_success",
                    "message": "Script validated successfully (dry run)",
                    "dry_run": True,
                    "script": script
                }
            else:
                # Check auto-execute policy
                if not settings.AUTO_EXECUTE_ENABLED and require_confirmation:
                    return {
                        "execution_id": execution_id,
                        "status": "confirmation_required",
                        "message": "Execution requires confirmation",
                        "script": script,
                        "dry_run": False
                    }
                
                # Execute script
                execution_result = await connector.execute_script(script)
                
                result = {
                    "execution_id": execution_id,
                    "status": "success",
                    "message": "Script executed successfully",
                    "dry_run": False,
                    "script": script,
                    "result": execution_result,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Log execution
            await self._log_execution(
                execution_id=execution_id,
                router_id=router_id,
                script=script,
                user_id=user_id,
                result=result
            )
            
            # Add to history
            self.execution_history.append({
                "execution_id": execution_id,
                "timestamp": datetime.now().isoformat(),
                "router_id": router_id,
                "user_id": user_id,
                "script": script,
                "status": result["status"]
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing script: {e}")
            return {
                "execution_id": execution_id,
                "status": "error",
                "error": str(e),
                "dry_run": dry_run
            }
    
    async def _validate_script(self, script: str) -> Dict[str, Any]:
        """Validate RouterOS script syntax and safety"""
        validation_result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }
        
        # Check for dangerous commands
        dangerous_commands = [
            "/system/reset",
            "/system/reboot",
            "/system/shutdown",
            "/file/remove",
            "/ip/route/remove",
            "/interface/remove"
        ]
        
        script_lower = script.lower()
        for cmd in dangerous_commands:
            if cmd in script_lower:
                validation_result["warnings"].append(
                    f"Potentially dangerous command detected: {cmd}"
                )
        
        # Check script syntax (basic validation)
        if not script.strip():
            validation_result["valid"] = False
            validation_result["errors"].append("Script is empty")
        
        # Use AI Brain for advanced validation
        if self.ai_brain:
            try:
                # Ask AI to validate script
                validation_prompt = f"""???? ?? ??? ????? ????? RouterOS ??????:
{script}

???:
1. ??? ?????? (Syntax)
2. ??????
3. ?? ????? ??????"""
                
                # This would use AI Brain for validation
                # For now, we'll rely on basic validation
                
            except Exception as e:
                logger.error(f"AI validation error: {e}")
        
        if validation_result["errors"]:
            validation_result["valid"] = False
        
        return validation_result
    
    async def _create_snapshot(
        self,
        router_id: str,
        connector: MikroTikConnector
    ) -> Dict:
        """Create a snapshot of router configuration"""
        try:
            # Get current configuration
            config = await connector.execute_command("/export")
            
            snapshot = {
                "router_id": router_id,
                "timestamp": datetime.now().isoformat(),
                "config": config,
                "system_resource": await connector.execute_command("/system/resource/print"),
                "interfaces": await connector.execute_command("/interface/print"),
                "ip_addresses": await connector.execute_command("/ip/address/print")
            }
            
            return snapshot
            
        except Exception as e:
            logger.error(f"Error creating snapshot: {e}")
            return {
                "router_id": router_id,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    async def rollback(
        self,
        execution_id: str,
        router_id: str,
        connector: MikroTikConnector
    ) -> Dict[str, Any]:
        """Rollback to a previous snapshot"""
        if execution_id not in self.snapshots:
            return {
                "status": "error",
                "error": "Snapshot not found"
            }
        
        snapshot = self.snapshots[execution_id]
        
        try:
            # Restore configuration from snapshot
            if "config" in snapshot:
                # Import configuration
                await connector.execute_command("/import", {"file-name": snapshot["config"]})
            
            return {
                "status": "success",
                "message": "Rollback completed successfully",
                "execution_id": execution_id
            }
            
        except Exception as e:
            logger.error(f"Error during rollback: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _log_execution(
        self,
        execution_id: str,
        router_id: str,
        script: str,
        user_id: Optional[str],
        result: Dict
    ):
        """Log execution to database"""
        try:
            # TODO: Save to database using ExecutionLog model
            logger.info(
                f"Execution logged: {execution_id} | "
                f"Router: {router_id} | "
                f"User: {user_id} | "
                f"Status: {result['status']}"
            )
        except Exception as e:
            logger.error(f"Error logging execution: {e}")
    
    async def get_execution_history(
        self,
        router_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get execution history"""
        history = self.execution_history
        
        if router_id:
            history = [h for h in history if h.get("router_id") == router_id]
        
        return history[-limit:]
    
    async def execute_with_ai(
        self,
        router_id: str,
        user_message: str,
        connector: MikroTikConnector,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute command based on natural language input using AI
        """
        if not self.ai_brain:
            return {
                "status": "error",
                "error": "AI Brain is not available"
            }
        
        try:
            # Process message with AI
            ai_response = await self.ai_brain.process_chat_message(
                message=user_message,
                user_id=user_id or "system",
                context={"router_id": router_id}
            )
            
            # Extract actions
            actions = ai_response.get("actions", [])
            
            if not actions:
                return {
                    "status": "no_action",
                    "message": ai_response.get("message", "No action required"),
                    "ai_response": ai_response
                }
            
            # Execute first action
            action = actions[0]
            if action.get("type") == "routeros_script":
                script = action.get("script", "")
                
                # Generate script if not provided
                if not script:
                    script = await self.ai_brain.generate_routeros_script(
                        intent=ai_response.get("intent", "general"),
                        parameters={"user_message": user_message}
                    )
                
                # Execute script (dry run first)
                result = await self.execute_script(
                    router_id=router_id,
                    script=script,
                    connector=connector,
                    dry_run=True,
                    require_confirmation=True,
                    user_id=user_id
                )
                
                return {
                    "status": "success",
                    "ai_response": ai_response,
                    "execution_result": result,
                    "script": script
                }
            
            return {
                "status": "unknown_action",
                "message": "Unknown action type",
                "ai_response": ai_response
            }
            
        except Exception as e:
            logger.error(f"Error in AI execution: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
