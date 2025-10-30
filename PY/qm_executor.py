"""
QM Command Executor using QMClient
Executes QM commands and returns formatted output
"""

import sys
import qmclient

def execute_command(command):
    """Execute a QM command and return output"""
    try:
        # Connect to QM
        qm = qmclient.QMClient()
        qm.connect('localhost', 4243, 'HAL', '', '')
        
        # Execute command
        qm.execute(command)
        
        # Get output
        output = []
        while True:
            line = qm.read_line()
            if line is None:
                break
            output.append(line)
        
        # Disconnect
        qm.disconnect()
        
        return '\n'.join(output)
        
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qm_executor.py <command>")
        sys.exit(1)
    
    command = ' '.join(sys.argv[1:])
    result = execute_command(command)
    print(result)
