from opponent_model import OpponentModel
from poker_point import PokerPoint
from match_state import MatchState

class PokerConfig():
    """
    
    """

    CONFIG = {
        'ranks': ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'],
        'suits': ['s', 'd', 'h', 'c'],
        'inputs': PokerPoint.INPUTS+MatchState.INPUTS+['chips']+OpponentModel.INPUTS,
        'action_mapping': {0: 'f', 1: 'c', 2: 'r'},
        'acpc_path': "SBB/environments/poker/ACPC/",
        'available_ports': [],
        'small_bet': 10,
        'big_bet': 20,
        'positions': 2,
        'hand_strength_labels': { # TODO: refactor, cuidado com PokerConfig.CONFIG['hand_strength_labels'].keys()
            0: 0.9,  # >= (10%)
            1: 0.7,  # >= (20%)
            2: 0.4,  # >= (30%)
            3: 0.4,  # < (40%)
        },
        'rule_based_opponents': ['loose_agressive', 'loose_passive', 'tight_agressive', 'tight_passive'],
        'point_cache_size': 50,
    }