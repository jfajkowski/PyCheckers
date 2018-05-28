import yaml

from elements import Color
from strategies import RandomGameStrategy, MinMaxGameStrategy, AlphaBetaGameStrategy, ManualGameStrategy
from heuristics import light_pieces_dark_pieces_difference_heuristic, dark_pieces_light_pieces_difference_heuristic, light_pieces_maximizing_heuristic, dark_pieces_maximizing_heuristic


def read_players():
    with open('../game_config.yaml', 'r') as f:
        game_config = yaml.load(f)

        return read_light_player(game_config), read_dark_player(game_config)


def read_light_player(game_config):
    return read_player("light_player", Color.LIGHT_PIECE, game_config)


def read_dark_player(game_config):
    return read_player("dark_player", Color.DARK_PIECE, game_config)


def read_player(player_name, color, game_config):
    player = None
    strategy = game_config[player_name]["strategy"]

    if strategy == 'manual':
        player = ManualGameStrategy(color)
    elif strategy == 'random':
        player = RandomGameStrategy(color)
    else:
        heuristic = get_heuristic_from_string(game_config[player_name]["heuristic"])
        depth = int(game_config[player_name]["depth"])

        if strategy == 'alpha_beta':
            player = AlphaBetaGameStrategy(color, heuristic, depth)
        elif strategy == 'min_max':
            player = MinMaxGameStrategy(color, heuristic, depth)
        else:
            print("wrong strategy error")

    return player


def get_heuristic_from_string(heuristic_string):
    if heuristic_string == 'dark_pieces_maximizing':
        return dark_pieces_maximizing_heuristic
    elif heuristic_string == 'light_pieces_maximizing':
        return light_pieces_maximizing_heuristic
    elif heuristic_string == 'dark_pieces_light_pieces_difference':
        return dark_pieces_light_pieces_difference_heuristic
    elif heuristic_string == 'light_pieces_dark_pieces_difference':
        return light_pieces_dark_pieces_difference_heuristic
    else:
        print("wrong heuristic error")
