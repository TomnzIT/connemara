# 🐎 connemara

## ⚠️ Disclaimer

The use of the Connemara tool is strictly for ethical purposes and by using this software, you agree that you have permission from the machine owner to control and execute commands on it. Unauthorized access to remote systems is illegal and unethical. Please use this tool responsibly.

## Features

- Reverse shell for command execution.
- Screenshot capture and automated GIF creation.
- File upload and download capabilities.
- Prank mode for demonstration purposes (fake Windows update screen).
- Robust WebSocket communication.

## Installation

To install Connemara, you'll need Python 3.6+ and the following packages:

```sh
pip install websockets pyautogui imageio chardet asyncio
git clone https://github.com/TomnzIT/connemara.git
cd connemara
```

## Usage

To start the server, run the `server.py` script:
```sh
python server.py
```

To start the client, run the `client.pyw` script on the victim machine:
```sh
python client.pyw
```
To transform the client script into a executable file:
```sh
pip install pyinstaller
pyinstaller client.pyw --onefile
```
