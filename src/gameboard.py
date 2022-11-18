import random
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
from mahjong.shanten import Shanten

shanten = Shanten()
calculator = HandCalculator()

# 1-35 Man (111122223333...)
# 36-71 Pin
# 72-107 Sou
# 108-123 Wind (108: East, 112: South, 116: West, 120: North)
# 124-135 Dragon (124: White, 128: Green, 132: Red)
class GameBoard:
    def __init__(self) -> None:
        self.tile_case = [i for i in range(136)]
        self.wall = False
        self.dead_wall = False
        self.player_turn = 0
        self.last_discard_turn = False
        self.player_0 = False
        self.player_1 = False
        self.player_2 = False
        self.player_3 = False
        self.all_players = []
        self.current_possible_actions = []

    def __str__(self) -> str:
        return f"Wall({0 if type(self.wall) != list else len(self.wall)}): {self.wall}\nDead Wall: {self.dead_wall}\nPlayer Turn: {self.player_turn}\nPlayer East: {self.player_0}\nPlayer South: {self.player_1}\nPlayer West: {self.player_2}\nPlayer North: {self.player_3}\n"

    def setup_board(self) -> None:
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
        self.current_possible_actions = self.check_actions()
        return True, self.player_turn, self.current_possible_actions
    
    def check_actions(self) -> list:
        if self.all_players[self.player_turn]["drawn"] != []:
            actions_return = ["discard"]
            complete_hand = self.all_players[self.player_turn]["closed"]+self.all_players[self.player_turn]["open"]+self.all_players[self.player_turn]["drawn"]
            complete_hand = TilesConverter.to_34_array(complete_hand)
            if self.all_players[self.player_turn]["open"] == [] and shanten.calculate_shanten(complete_hand) == 0:
                actions_return.append("riichi")
            if shanten.calculate_shanten(complete_hand) == -1:
                actions_return.append("tsumo")
            # TODO: Check for kan
            return actions_return
        else:
            # TODO: Check for ron, kan, pon, chi
            self.player_turn = self.last_discard_turn + 1 if self.last_discard_turn != 3 else 0
            return ["draw"]

    def update(self, response: str, tile_indexes: list = []) -> tuple:
        if response not in self.current_possible_actions:
            print(self.current_possible_actions)
            print(response)
            return False, self.player_turn, self.current_possible_actions

        match response:
            case "discard":
                if len(tile_indexes) == 1 and type(tile_indexes[0]) == int and tile_indexes[0] <= len(self.all_players[self.player_turn]["closed"]):
                    self.all_players[self.player_turn]["discard"].append(self.all_players[self.player_turn]["closed"].pop(tile_indexes[0]))
                    self.all_players[self.player_turn]["closed"].append(self.all_players[self.player_turn]["drawn"].pop(0))
                    self.all_players[self.player_turn]["closed"].sort()
                elif len(tile_indexes) == 0:
                    self.all_players[self.player_turn]["discard"].append(self.all_players[self.player_turn]["drawn"].pop(0))
                else:
                    return False, self.player_turn, self.current_possible_actions
                self.last_discard_turn = self.player_turn
                self.current_possible_actions = self.check_actions()
                if self.current_possible_actions == ["draw"]:
                    self.all_players[self.player_turn]["drawn"].append(self.wall.pop(0))
                    self.current_possible_actions = self.check_actions()
                return True, self.player_turn, self.current_possible_actions
            case "kan":
                pass
            case "pon":
                pass
            case "chi":
                pass
            case "ron":
                pass
            case "tsumo":
                pass
            case "riichi":
                pass
            case _:
                return False, self.player_turn, self.current_possible_actions


if __name__ == "__main__":
    board = GameBoard()
    # print(board)
    # r = board.setup_board()
    # print(r)
    # print(board)
    # r = board.update(response="discard")
    # print(r)
    # print(board)
    # r = board.update(response="discard",tile_indexes=[0])
    # print(r)
    # print(board)

    for i in range(100000):
        r = board.setup_board()
        # if 'tsumo' in r[2]:
        if r[2] != ['discard']:
            print(r)
            print(board)
            print(TilesConverter.to_one_line_string(board.player_0["closed"]+board.player_0["open"]+board.player_0["drawn"]))
            break


    # tiles = TilesConverter.string_to_136_array(man='123234', pin='11', sou='345', honors='777')
    # # tiles = TilesConverter.string_to_136_array(honors='11144555666777')
    # win_tile = TilesConverter.string_to_136_array(pin='1')[0]
    # # melds = [Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(honors='11'))]
    # print(tiles)
    # print(win_tile)
    # # print(melds)
    # result = calculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True,player_wind=26+2,round_wind=26+1))
    # print(result.han, result.fu)
    # print(result.cost['main'], result.cost['additional'])
    # print(result.yaku)
    # for fu_item in result.fu_details:
    #     print(fu_item)