#!/usr/bin/env python3
"""
Simple MCP server for notifications without fastmcp dependency
"""

import json
import sys
import os
import subprocess
from typing import Any

def send_notification(title: str, message: str, sound: str = None):
    """Send a notification with optional sound"""
    # Play sound if specified
    if sound and os.path.exists(sound):
        subprocess.run(['afplay', sound], check=False)
    
    # Send notification
    script = f'''
    display notification "{message}" with title "{title}"
    '''
    subprocess.run(['osascript', '-e', script], check=False)
    
    return {"success": True, "message": f"Notification sent: {title}"}

def handle_request(request):
    """Handle MCP request"""
    if request.get("method") == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "send_notification":
            title = arguments.get("title", "Claude Notification")
            message = arguments.get("message", "")
            sound = arguments.get("sound")
            
            # Use environment sounds if available
            if sound == "start":
                sound = os.environ.get("CLAUDE_START_SOUND", "/System/Library/Sounds/Ping.aiff")
            elif sound == "complete":
                sound = os.environ.get("CLAUDE_COMPLETE_SOUND", "/System/Library/Sounds/Glass.aiff")
            elif sound == "frog":
                sound = "/System/Library/Sounds/Frog.aiff"
            
            result = send_notification(title, message, sound)
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": result
            }
    
    return {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "error": {"code": -32601, "message": "Method not found"}
    }

def main():
    """Main server loop"""
    # Send server info
    server_info = {
        "protocolVersion": "2024-11-01",
        "capabilities": {
            "tools": {
                "send_notification": {
                    "description": "Send a notification with optional sound",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "message": {"type": "string"},
                            "sound": {"type": "string", "enum": ["start", "complete", "frog", "none"]}
                        },
                        "required": ["message"]
                    }
                }
            }
        }
    }
    
    print(json.dumps(server_info))
    sys.stdout.flush()
    
    # Read and handle requests
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main()