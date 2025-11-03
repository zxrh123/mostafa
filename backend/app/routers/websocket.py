from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["Realtime"], prefix="")


@router.websocket("/ws/ai")
async def ai_chat_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            payload = await websocket.receive_text()
            await websocket.send_text(
                f"AI Core received: {payload}. (Realtime processing requires backend workers to be active.)"
            )
    except WebSocketDisconnect:
        return
