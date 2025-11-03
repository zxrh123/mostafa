"""
Helper utilities
"""

from typing import Dict, Any
import json


def format_routeros_script(script: str) -> str:
    """Format RouterOS script for display"""
    lines = script.split('\n')
    formatted = []
    indent = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted.append('')
            continue
        
        # Decrease indent on closing braces
        if stripped.startswith('}'):
            indent = max(0, indent - 1)
        
        formatted.append('  ' * indent + stripped)
        
        # Increase indent on opening braces
        if stripped.endswith('{'):
            indent += 1
    
    return '\n'.join(formatted)


def validate_ip_address(ip: str) -> bool:
    """Validate IP address format"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def sanitize_routeros_command(command: str) -> str:
    """Sanitize RouterOS command"""
    # Remove dangerous characters
    dangerous_chars = [';', '&&', '||', '`', '$']
    for char in dangerous_chars:
        command = command.replace(char, '')
    
    return command.strip()
