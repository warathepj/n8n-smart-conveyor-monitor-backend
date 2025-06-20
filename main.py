import asyncio
import websockets
import json

async def handler(websocket, path=None):
    print(f"Client connected from {websocket.remote_address}")
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")
            # Process the received data as needed
            # For example, you could store it in a database,
            # or trigger other actions based on the data.
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Client {websocket.remote_address} disconnected gracefully.")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client {websocket.remote_address} disconnected with error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def main():
    # Start the WebSocket server on localhost, port 8765
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
