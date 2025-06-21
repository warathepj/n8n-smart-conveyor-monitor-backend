import asyncio
import websockets
import json
from httpx import AsyncClient # Using httpx for async http requests
from db import MongoDBManager
from datetime import datetime
from chart import create_chart

db_manager = MongoDBManager()

latest_data = None  # Global variable to store the latest data

async def save_data_periodically():
    while True:
        await asyncio.sleep(5)
        if latest_data:
            document = {
                "timestamp": datetime.utcnow(),
                "metadata": {
                    "client_address": latest_data["client_address"],
                    "client_port": latest_data["client_port"]
                },
                "currentRate": latest_data.get("currentRate"),
                "totalProduced": latest_data.get("totalProduced")
            }
            db_manager.get_collection().insert_one(document)
            print("Data saved to MongoDB (periodic).")


async def handler(websocket, path=None):
    global latest_data
    print(f"Client connected from {websocket.remote_address}")
    async with AsyncClient() as client:
        try:
            async for message in websocket:
                data = json.loads(message)
                print(f"Received: {data}")

                # Prepare data for MongoDB insertion
                latest_data = {
                    "client_address": websocket.remote_address[0],
                    "client_port": websocket.remote_address[1],
                    "currentRate": data.get("currentRate"),
                    "totalProduced": data.get("totalProduced")
                }
                document = {
                    "timestamp": datetime.utcnow(),
                    "metadata": {
                        "client_address": websocket.remote_address[0],
                        "client_port": websocket.remote_address[1]
                    },
                    "currentRate": data.get("currentRate"),
                    "totalProduced": data.get("totalProduced")
                }
                db_manager.get_collection().insert_one(document)
                print("Data saved to MongoDB.")
                create_chart()

                if data.get("currentRate") == 0:
                    print("stop")
                    await client.post("http://localhost:5678/webhook/1c9a12a3-2af2-4a5b-9981-05880e995cbb", json={"status": "stop", "rate": data.get("currentRate"), "totalProduced": data.get("totalProduced")})
                    await asyncio.sleep(20) # Delay for 20 seconds
                elif 10 <= data.get("currentRate") <= 50:
                    print("too slow")
                    await client.post("http://localhost:5678/webhook/1c9a12a3-2af2-4a5b-9981-05880e995cbb", json={"status": "too slow", "rate": data.get("currentRate"), "totalProduced": data.get("totalProduced")})
                    await asyncio.sleep(20) # Delay for 20 seconds
                elif data.get("currentRate") > 60:
                    print("too fast")
                    await client.post("http://localhost:5678/webhook/1c9a12a3-2af2-4a5b-9981-05880e995cbb", json={"status": "too fast", "rate": data.get("currentRate"), "totalProduced": data.get("totalProduced")})
                    await asyncio.sleep(20) # Delay for 20 seconds
        except websockets.exceptions.ConnectionClosedOK:
            print(f"Client {websocket.remote_address} disconnected gracefully.")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Client {websocket.remote_address} disconnected with error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            db_manager.close_connection()


async def main():
    # Start the WebSocket server on localhost, port 8765
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        asyncio.create_task(save_data_periodically())  # Start the periodic saving task
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
