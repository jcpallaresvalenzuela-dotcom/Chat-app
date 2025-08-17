from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Configurar el motor de plantillas apuntando a ./templates
templates = Jinja2Templates(directory="templates")

# Estado en memoria (no persistente)
connections = {}      # username -> WebSocket (máx 2)
last_messages = {}    # username -> str
MAX_PLAYERS = 2


# ---------------------------
# Rutas HTTP
# ---------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Renderiza templates/index.html
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------------------
# Helpers
# ---------------------------
def snapshot_state():
    """Genera snapshot con el último mensaje de cada jugador"""
    players = sorted(
        [{"name": name, "last": last_messages.get(name, "")} for name in connections.keys()],
        key=lambda x: x["name"]
    )
    while len(players) < 2:
        players.append({"name": f"player{chr(65+len(players))}", "last": "—"})
    return {"type": "state", "players": players[:2]}


async def broadcast_state():
    """Envía el estado a todos los clientes conectados"""
    state = snapshot_state()
    dead = []
    for name, ws in connections.items():
        try:
            await ws.send_json(state)
        except Exception:
            dead.append(name)
    # Limpieza
    for name in dead:
        ws = connections.pop(name, None)
        if ws:
            try:
                await ws.close()
            except Exception:
                pass


# ---------------------------
# WebSocket
# ---------------------------
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    username = websocket.query_params.get("username", "").strip()
    if not username:
        await websocket.accept()
        await websocket.send_json({"type": "error", "message": "Username requerido"})
        await websocket.close()
        return

    username = username[:20]

    # Capacidad máxima 2
    if len(connections) >= MAX_PLAYERS:
        await websocket.accept()
        await websocket.send_json({"type": "error", "message": "Sala llena (2/2). Intenta más tarde."})
        await websocket.close()
        return

    # Evitar duplicados simples
    base = username
    i = 2
    while username in connections:
        username = f"{base}-{i}"
        i += 1

    await websocket.accept()
    connections[username] = websocket
    last_messages.setdefault(username, "")

    await broadcast_state()

    try:
        while True:
            data = await websocket.receive_text()
            import json
            try:
                payload = json.loads(data)
            except Exception:
                payload = {"type": "msg", "text": data}

            if payload.get("type") == "msg":
                text = str(payload.get("text", ""))[:500]
                last_messages[username] = text
                await broadcast_state()
    except WebSocketDisconnect:
        pass
    finally:
        ws = connections.pop(username, None)
        if ws:
            try:
                await ws.close()
            except Exception:
                pass
        await broadcast_state()
