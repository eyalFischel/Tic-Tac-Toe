from pydantic import BaseModel, validator

class Play(BaseModel):
    nickname: str
    position: int  # Position on the board (0-8 for Tic-Tac-Toe)
    
    @validator("position")
    def validate_position(cls, position):
        if position < 0 or position > 8:
            raise ValueError("Position must be between 0 and 8.")
        return position
    
class Player(BaseModel):
    nickname: str
    symbol: str = "X"  # Default symbol for player

    @validator("symbol")
    def validate_symbol(cls, symbol):
        if symbol not in ["X", "O"]:
            raise ValueError("Symbol must be either 'X' or 'O'.")
        return symbol

class PlayerStats(BaseModel):
    player: Player
    wins: int = 0
    losses: int = 0
    draws: int = 0

class GameState(BaseModel):
    room_id: str
    board: str = "         "  # 9 spaces for Tic-Tac-Toe
    turn: str = "X" 
    players: dict[str, Player] = {}
    players_stats: dict[str, PlayerStats] = {}

    def reset(self):
        self.board = "         "
        self.turn = "X"
        self.players.clear()
    
    def add_player(self, player: Player):
        if player.symbol in [p.symbol for p in self.players.values()]:
            raise ValueError("Symbol already taken by another player.")

        if player.nickname not in self.players and len(self.players) < 2:
            self.players[player.nickname] = player
            self.players_stats[player.nickname] = PlayerStats(player=player)
        else:
            raise ValueError("Player already exists in the game or the room is already full.")
    
    def play(self, play: Play):
        if play.nickname not in self.players:
            raise ValueError("Player not found in the game.")
        
        if self.turn != self.players[play.nickname].symbol:
            raise ValueError("It's not your turn.")
        
        if self.board[play.position] != " ":
            free_positions = [i for i, c in enumerate(self.board) if c == " "]
            raise ValueError(f"Position already taken. Choose another position: {free_positions}")
        
        # Update the board
        board_list = list(self.board)
        board_list[play.position] = self.players[play.nickname].symbol
        self.board = "".join(board_list)
        
        # Switch turn
        self.turn = "O" if self.turn == "X" else "X"

    
    def check_status_game(self):
        for nickname, player in self.players.items():
            if self._check_for_win(nickname):
                self.players_stats[nickname].wins += 1

                for other in self.players.values():
                    if other != player:
                        self.players_stats[other.nickname].losses += 1
                return {"status": "win", "winner": player.nickname}
        
        if " " not in self.board:
            for player in self.players.values():
                self.players_stats[player.nickname].draws += 1
            return {"status": "draw"}

        return {"status": "ongoing", "next_turn": self.turn}

    def _check_for_win(self, nickname: str):
        player_symbol = self.players[nickname].symbol

        # Rows
        for pos in [0, 3, 6]:
            if list(self.board[pos:pos+3]) == [player_symbol] * 3:
                return True

        # Columns
        for pos in range(3):
            if [self.board[pos], self.board[pos+3], self.board[pos+6]] == [player_symbol] * 3:
                return True

        # Diagonals
        if [self.board[0], self.board[4], self.board[8]] == [player_symbol] * 3:
            return True
        if [self.board[2], self.board[4], self.board[6]] == [player_symbol] * 3:
            return True

        return False
