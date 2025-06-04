import asyncio
import websockets
import json

async def client(task_id: str):
    uri = f"ws://localhost:8000/ws/{task_id}"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket. Listening for notifications...")
        
        async def receiver():
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                print(f"[Notification] Status: {data.get('status')}, Task ID: {data.get('task_id')}")
                if data.get('status') == 'PROGRESS':
                    print(f"Progress: {data.get('progress')}%, Current word: {data.get('current_word')}")
                elif data.get('status') == 'COMPLETED':
                    print(f"Execution time: {data.get('execution_time')}s")
                    print("Results:")
                    for r in data.get('results', []):
                        print(f" - Word: {r['word']}, Distance: {r['distance']}")

        async def sender():
            while True:
                command = input("Enter command (or 'exit' to quit): ")
                if command == "exit":
                    print("Closing connection...")
                    await websocket.close()
                    break
            
                await websocket.send(command)

        await asyncio.gather(receiver(), sender())

if __name__ == "__main__":
    import sys
    task_id = "test123" 
    asyncio.run(client(task_id))
