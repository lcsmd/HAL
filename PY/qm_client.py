import socket
import json
from typing import Any, Dict, Optional
from config import config

class QMClient:
    def __init__(self):
        self.host = config.qm_server.host
        self.port = config.qm_server.port
        self.socket = None
    
    def connect(self):
        """Connect to OpenQM server"""
        if not self.socket:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
    
    def disconnect(self):
        """Disconnect from OpenQM server"""
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def execute_command(self, command: str) -> str:
        """Execute a TCL command on the OpenQM server"""
        try:
            self.connect()
            # Format command for TCL
            formatted_cmd = f"{command}\n"
            self.socket.send(formatted_cmd.encode())
            
            # Read response
            response = ""
            while True:
                chunk = self.socket.recv(4096).decode()
                if not chunk:
                    break
                response += chunk
                if response.endswith(">"):  # TCL prompt
                    break
            
            return response.strip()
        
        except Exception as e:
            print(f"Error executing command: {e}")
            return ""
        
        finally:
            self.disconnect()
    
    def read_record(self, filename: str, key: str) -> Optional[Dict[str, Any]]:
        """Read a record from an OpenQM file"""
        cmd = f'READ {filename} "{key}"'
        response = self.execute_command(cmd)
        try:
            return json.loads(response)
        except:
            return None
    
    def write_record(self, filename: str, key: str, data: Dict[str, Any]) -> bool:
        """Write a record to an OpenQM file"""
        json_data = json.dumps(data)
        cmd = f'WRITE {json_data} TO {filename} "{key}"'
        response = self.execute_command(cmd)
        return "Error" not in response
