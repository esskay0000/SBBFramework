import random
import copy
import numpy
from collections import defaultdict
from default_environment import DefaultEnvironment, DefaultPoint, reset_points_ids
from reinforcement_environment import ReinforcementEnvironment, ReinforcementPoint
from ..core.team import Team
from ..core.diversity_maintenance import DiversityMaintenance
from ..core.pareto_dominance_for_points import ParetoDominanceForPoints
from ..core.pareto_dominance_for_teams import ParetoDominanceForTeams
from ..utils.helpers import round_value, flatten, accumulative_performances, rank_teams_by_accumulative_score
from ..config import Config

# TODO
from tictactoe.tictactoe_match import TictactoeMatch
from tictactoe.tictactoe_opponents import TictactoeRandomOpponent, TictactoeSmartOpponent

class ReinforcementEnvironmentForSockets(ReinforcementEnvironment):
    """
    
    """

    def __init__(self):
        # TODO: ler de um arquivo configuravel? (e o CONFIG tambem)
        # super(ReinforcementEnvironmentForSockets, self).__init__(total_actions, total_inputs, total_labels, coded_opponents_for_training, coded_opponents_for_validation, point_class)
        
        # atualizar testes para usar setUp e tearDown

        total_actions = 9 # spaces in the board
        total_inputs = 9 # spaces in the board (0, 1, 2 as the states, 0: no player, 1: player 1, 2: player 2)
        total_labels = 1 # since no labels are being used, group everything is just one label
        coded_opponents = [TictactoeRandomOpponent, TictactoeSmartOpponent]
        point_class = ReinforcementPoint
        super(ReinforcementEnvironmentForSockets, self).__init__(total_actions, total_inputs, total_labels, coded_opponents, coded_opponents, point_class)
        self.total_positions_ = 2
        self.action_mapping_ = {
            '[0,0]': 0, '[0,1]': 1, '[0,2]': 2,
            '[1,0]': 3, '[1,1]': 4, '[1,2]': 5,
            '[2,0]': 6, '[2,1]': 7, '[2,2]': 8,
        }

    def _play_match(self, team, opponent, point, mode, match_id):
        """
        
        """
        # send message:
        # team? acessado por uma port?
        # opponent? acessado por uma port?
        # point?
        # <mode: mode> (uso interno + para debug)
        # <match_id: match_id> (para debug)

        # enquanto match nao terminar:

        if mode == Config.RESTRICTIONS['mode']['training']:
            is_training = True
        else:
            is_training = False
        outputs = []
        for position in range(1, self.total_positions_+1):
            if position == 1:
                first_player = opponent
                is_training_for_first_player = False
                second_player = team
                is_training_for_second_player = is_training
                sbb_player = 2
            else:
                first_player = team
                is_training_for_first_player = is_training
                second_player = opponent
                is_training_for_second_player = False
                sbb_player = 1

            # AQUI: iniciar o app no socket?
            match = TictactoeMatch(player1_label = first_player.__repr__(), player2_label = second_player.__repr__())
            
            opponent.initialize(point.seed_)
            while True:
                player = 1

                # AQUI
                inputs = match.inputs_from_the_point_of_view_of(player)

                # AQUI
                valid_actions = match.valid_actions()

                action = first_player.execute(point.point_id_, inputs, valid_actions, is_training_for_first_player)
                if action is None:
                    action = random.choice(valid_actions)

                if is_training_for_first_player:
                    first_player.action_sequence_['coding2'].append(str(action))
                    first_player.action_sequence_['coding4'].append(str(action))

                # AQUI
                match.perform_action(player, action)

                # AQUI
                if match.is_over():
                    # AQUI
                    result = match.result_for_player(sbb_player)
                    outputs.append(result)
                    team.action_sequence_['coding3'].append(int(result*2))
                    break
                player = 2

                # AQUI
                inputs = match.inputs_from_the_point_of_view_of(player)

                # AQUI
                valid_actions = match.valid_actions()

                action = second_player.execute(point.point_id_, inputs, valid_actions, is_training_for_second_player)
                if action is None:
                    action = random.choice(valid_actions)
                if is_training_for_second_player:
                    second_player.action_sequence_['coding2'].append(str(action))
                    second_player.action_sequence_['coding4'].append(str(action))

                # AQUI
                match.perform_action(player, action)

                # AQUI
                if match.is_over():
                    # AQUI
                    result = match.result_for_player(sbb_player)
                    outputs.append(result)
                    team.action_sequence_['coding3'].append(int(result*2))
                    break
        return numpy.mean(outputs)

    def metrics(self):
        msg = ""
        msg += "\n### Environment Info:"
        msg += "\ntotal inputs: "+str(self.total_inputs_)
        msg += "\ntotal actions: "+str(self.total_actions_)
        msg += "\nactions mapping: "+str(self.action_mapping_)
        msg += "\npositions: "+str(self.total_positions_)
        return msg