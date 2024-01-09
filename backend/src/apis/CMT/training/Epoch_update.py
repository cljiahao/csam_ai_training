# epoch_metrics_updater.py
import asyncio
import json

async def send_epoch_updates(websocket, epoch_metrics):
    try:
        await websocket.accept()
        for metric in epoch_metrics:
            await websocket.send_text(json.dumps(metric))
            await asyncio.sleep(0.1)  # Small delay to simulate real-time updates
    except Exception as e:
        print(f"Error in WebSocket communication: {e}")
    finally:
        await websocket.close()