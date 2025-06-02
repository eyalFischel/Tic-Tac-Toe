import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.reddisManager import RedisManager
from models import Player, GameState, Play


app = FastAPI()
redis = RedisManager(redis_url="redis://localhost:6379")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
from pydantic import BaseModel

class Player(BaseModel):
    nickname: str
    wins: int = 0
    losses: int = 0
    draws: int = 0
    symbol: str = "X"  # Default symbol for player

class GameState(BaseModel):
    room_id: str
    board: str = "         "  # 9 spaces for Tic-Tac-Toe
    turn: str = "X"  # Default starting player
    players: dict[str, Player] = {}

    def reset(self):
        self.board = "         "
        self.turn = "X"
        self.players.clear()
    
    def add_player(self, player: Player):
        if player.nickname not in self.players and len(self.players) < 2:
            self.players[player.nickname] = player
        else:
            raise ValueError("Player already exists in the game or the room is already full.")


"""

@app.get("/")
async def root():
    return {"message": "Welcome to the Tic-Tac-Toe API!"}

@app.get("/help")
async def help():
    return {
        "message": "This is the Tic-Tac-Toe API. Use the endpoints to manage game rooms, players, and game states.",
        "endpoints": {
            "/": "Welcome message",
            "/help": "API documentation",
            "/rooms/{room_id}": "Get game state for a specific room",
            "/rooms": "Get all existing game rooms",
            "/rooms/create": "Create a new game room",
            "/rooms/{room_id}/join": "Join a game room",
            "/rooms/{room_id}/leave": "Leave a game room",
            "/rooms/{room_id}/play": "Make a move in the game",
            "/stats/{nickname}": "Get player statistics"
        }
    }

@app.get("/rooms/{room_id}")
async def get_game_state(room_id: str):
    try:
        game_state = await redis.get(room_id)
        if game_state:
            return json.loads(game_state)
        return {"error": "Room not found"}, 404
    except Exception as error:
        return {"Error while fetching game state": str(error)}, 500

@app.get("/rooms")
async def get_all_rooms():
    try:
        keys = await redis.get_all_keys()  
        rooms = []
        for key in keys:
            game_state = await redis.get(key)
            if game_state:
                rooms.append(json.loads(game_state))
        return {"rooms": rooms}
    except Exception as error:
        return {"Error while fetching rooms": str(error)}, 500

@app.post("/rooms/create")
async def create_room(room_id: str):
    try:
        if not await redis.exists(room_id):
            game_state = GameState(room_id=room_id)
            await redis.set(room_id, game_state.model_dump_json())
            return {"message": "Room created successfully", "room_id": room_id}
        return {"error": "Room already exists"}, 400
    except Exception as error:
        return {"Error while creating room": str(error)}, 500

@app.post("/rooms/{room_id}/join")
async def join_room(room_id: str, player: Player):
    try:
        if not await redis.exists(room_id):
            return {"error": "Room does not exist"}, 404
        
        game_state_json = await redis.get(room_id)
        game_state = GameState.model_validate_json(game_state_json)

        game_state.add_player(player)
        await redis.set(room_id, game_state.model_dump_json())
        
        return {"message": "Player joined successfully", "room_id": room_id}
    except ValueError as ve:
        return {"ValueError error": str(ve)}, 400
    except Exception as error:
        return {"Error while joining room": str(error)}, 500

@app.post("/rooms/{room_id}/leave")
async def leave_room(room_id: str, nickname: str):
    try:
        if not await redis.exists(room_id):
            return {"error": "Room does not exist"}, 404
        
        game_state_json = await redis.get(room_id)
        game_state = GameState.model_validate_json(game_state_json)
        
        if nickname in game_state.players:
            del game_state.players[nickname]
            await redis.set(room_id, game_state.model_dump_json())
            return {"message": "Player left successfully", "room_id": room_id}
        return {"error": "Player not found in the room"}, 404
    except Exception as error:
        return {"Error while leaving room": str(error)}, 500

@app.post("/rooms/{room_id}/play")
async def play_move(room_id: str, play: Play):
    try:
        if not await redis.exists(room_id):
            return {"error": "Room does not exist"}, 404
        
        game_state_json = await redis.get(room_id)
        game_state = GameState.model_validate_json(game_state_json)
        
        game_state.play(play)
        status = game_state.check_status_game()

        if status["status"] == "win":
            game_state.reset()  # Reset the game state after a win
            return {"message": "Game over, resetting the game", "room_id": room_id, "winner": play.nickname}
        elif status["status"] == "draw":
            game_state.reset()
            return {"message": "Game over, it's a draw, resetting the game", "room_id": room_id}
        elif status["status"] == "ongoing":  
            await redis.set(room_id, game_state.model_dump_json())
            return {"message": "Move played successfully", "room_id": room_id, "board": game_state.board}
        
    except Exception as error:
        return {"Error while playing move": str(error)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)