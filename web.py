import asyncio
import websockets

# Function to send message to Streamlit app
async def send_message(message):
    try:
        async with websockets.connect("ws://localhost:8501/ws") as websocket:
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Connection to Streamlit app closed unexpectedly")

# WebSocket server coroutine
async def handle_message(websocket, path):
    async for message in websocket:
        if message.startswith("speed"):
            # Extract speed value from the message
            speed = float(message.split(":")[1])
            print(f"Received speed: {speed}")
            # Send speed value to the Streamlit app
            await send_message(f"speed:{speed}")
        elif message.startswith("slices"):
            # Extract number of slices value from the message
            num_slices = int(message.split(":")[1])
            print(f"Received number of slices: {num_slices}")
            # Send number of slices to the Streamlit app
            await send_message(f"slices:{num_slices}")
        elif message == "run_motor":
            # Send "run_motor" command to the Streamlit app
            print("Received 'run_motor' command")
            await send_message("run_motor")
        else:
            print(f"Unsupported message: {message}")

# Start WebSocket server
start_server = websockets.serve(handle_message, "localhost", 8765)

# Run the event loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
