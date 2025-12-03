HAL Voice Assistant - Windows Client
=====================================

INSTALLATION
------------

1. Copy these files to your Windows PC:
   - hal_client_standalone.py
   - START_HAL.bat
   - README.txt (this file)

2. Put them in any folder, for example:
   C:\HAL\
   or
   C:\Users\YourName\Desktop\HAL\

3. Make sure Python 3.x is installed:
   - Download from: https://www.python.org/downloads/
   - Or check if installed: open CMD and type: python --version

USAGE
-----

Method 1 (Easy):
  Double-click: START_HAL.bat

Method 2 (Command Line):
  Open Command Prompt
  cd C:\HAL  (or wherever you put the files)
  python hal_client_standalone.py

FIRST RUN
---------

The first time you run it, it will install the "websockets" library.
This is normal and only happens once.

After that, just double-click START_HAL.bat to connect to HAL.

CONFIGURATION
-------------

If your HAL server is on a different IP address:

1. Edit hal_client_standalone.py in Notepad
2. Find this line (near the top):
   GATEWAY_URL = 'ws://10.1.34.103:8768'
3. Change the IP address to your server's IP
4. Save and run again

TROUBLESHOOTING
---------------

Connection Refused:
  - Make sure HAL server is running
  - Make sure Voice Gateway is running on server
  - Check IP address in script
  - Check firewall (port 8768 must be open)

Module Not Found:
  - Run: pip install websockets
  - Or: python -m pip install websockets

Python Not Found:
  - Install Python 3.x from python.org
  - Make sure "Add to PATH" is checked during installation

EXAMPLE SESSION
---------------

You: what time is it
HAL: The current time is 12:45:30

You: what is the date
HAL: Today is Tuesday, December 3rd, 2025

You: hello
HAL: Hello! How can I help you today?

You: quit
Goodbye!

SUPPORT
-------

For help, contact your HAL system administrator.

Server Location: 10.1.34.103:8768
