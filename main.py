import asyncio
import websockets
import json
from httpx import AsyncClient # Using httpx for async http requests

async def handler(websocket, path=None):
    print(f"Client connected from {websocket.remote_address}")
    async with AsyncClient() as client:
        try:
            async for message in websocket:
                data = json.loads(message)
                print(f"Received: {data}")
                if data.get("currentRate") == 0:
                    print("stop")
                    await client.post("http://localhost:5678/webhook/1c9a12a3-2af2-4a5b-9981-05880e995cbb", json={"status": "stop", "rate": data.get("currentRate")})
                    await asyncio.sleep(20) # Delay for 10 seconds
                elif 10 <= data.get("currentRate") <= 50:
                    print("too slow")
                    await client.post("http://localhost:5678/webhook/1c9a12a3-2af2-4a5b-9981-05880e995cbb", json={"status": "too slow", "rate": data.get("currentRate")})
                    await asyncio.sleep(20) # Delay for 10 seconds
                elif data.get("currentRate") > 60:
                    print("too fast")
                    await client.post("http://localhost:5678/webhook/1c9a12a3-2af2-4a5b-9981-05880e995cbb", json={"status": "too fast", "rate": data.get("currentRate")})
                    await asyncio.sleep(20) # Delay for 10 seconds
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
