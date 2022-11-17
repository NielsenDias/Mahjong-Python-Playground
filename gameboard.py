import random


# 1x - Man
# 2x - Pin
# 3x - Sou
# 4x - Wind (1: East, 3: South, 5: West, 7: North)
# 5x - Dragon (1: White, 3: Green, 5: Red)
class GameBoard:
    def __init__(self) -> None:
        self.tile_case = []
        for j in range(4):
            for i in range(9):
                self.tile_case.append(i+11)
                self.tile_case.append(i+21)
                self.tile_case.append(i+31)
                if i%2 == 0 and i < 8:
                    self.tile_case.append(i+41)
                if i%2 == 0 and i < 6:
                    self.tile_case.append(i+51)
        self.wall = False
        self.dead_wall = False
        self.player_turn = 0
        self.player_0 = False
        self.player_1 = False
        self.player_2 = False
        self.player_3 = False
        self.all_players = []

    def __str__(self) -> str:
        return f"Wall({0 if type(self.wall) != list else len(self.wall)}): {self.wall}\nDead Wall: {self.dead_wall}\nPlayer Turn: {self.player_turn}\nPlayer East: {self.player_0}\nPlayer South: {self.player_1}\nPlayer West: {self.player_2}\nPlayer North: {self.player_3}\n"

    def setup_board(self):
        self.wall = list(self.tile_case)
        random.shuffle(self.wall)
        self.dead_wall = {"dora_indicator":[self.wall.pop(0)],
                          "kan_draw":[self.wall.pop(0) for _ in range(4)],
                          "kan_dora":[self.wall.pop(0) for _ in range(4)],
                          "ura_dora":[self.wall.pop(0) for _ in range(5)]}
        self.player_0 = {"closed":sorted([self.wall.pop(0) for _ in range(13)]),"open":[],"discard":[],"drawn":[self.wall.pop(0)]}
        self.player_1 = {"closed":sorted([self.wall.pop(0) for _ in range(13)]),"open":[],"discard":[],"drawn":[]}
        self.player_2 = {"closed":sorted([self.wall.pop(0) for _ in range(13)]),"open":[],"discard":[],"drawn":[]}
        self.player_3 = {"closed":sorted([self.wall.pop(0) for _ in range(13)]),"open":[],"discard":[],"drawn":[]}
        self.all_players = [self.player_0,self.player_1,self.player_2,self.player_3]
    
    def check_actions(self):
        if self.all_players[self.player_turn]["drawn"] != []:
            # riichi, kan, tsumo
            return ["discard"]
        else:
            # ron, kan, pon, chi
            self.player_turn = self.player_turn + 1 if self.player_turn != 3 else 0
            return []

    def update(self,tsumo=False,ron=False,kan=False,pon=False,chi=False,discard=False):
        if type(discard) != bool:
            if type(discard) == int and discard <= len(self.all_players[self.player_turn]["closed"]):
                self.all_players[self.player_turn]["discard"].append(self.all_players[self.player_turn]["closed"].pop(discard))
                self.all_players[self.player_turn]["closed"].append(self.all_players[self.player_turn]["drawn"].pop(0))
                self.all_players[self.player_turn]["closed"].sort()
            elif discard == "drawn":
                self.all_players[self.player_turn]["discard"].append(self.all_players[self.player_turn]["drawn"].pop(0))
            possible_actions = self.check_actions()
            if possible_actions == []:
                self.all_players[self.player_turn]["drawn"].append(self.wall.pop(0))
                return self.player_turn, self.check_actions()
            else:
                return self.player_turn, possible_actions


if __name__ == "__main__":
    board = GameBoard()
    print(board)
    board.setup_board()
    print(board)
    board.update(discard=0)
    print(board)
    board.update(discard=0)
    print(board)
    board.update(discard=0)
    print(board)
    board.update(discard=0)
    print(board)
    board.update(discard=0)
    print(board)
    board.update(discard=0)
    print(board)
    board.update(discard=0)
    print(board)