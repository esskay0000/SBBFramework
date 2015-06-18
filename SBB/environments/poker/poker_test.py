import sys
import socket

# import random
# import numpy
# from ..default_opponent import DefaultOpponent
# from ...config import Config

# class PokerRandomOpponent(DefaultOpponent):
#     def __init__(self):
#         super(PokerRandomOpponent, self).__init__("random")
#         self.seed_ = random.randint(0, Config.RESTRICTIONS['max_seed'])

#     def initialize(self):
#         self.random_generator_ = numpy.random.RandomState(seed=self.seed_)

#     def execute(self, point_id, inputs, valid_actions, is_training):
#         return self.random_generator_.choice(valid_actions)

#     def __str__(self):
#         return self.opponent_id +":"+str(self.seed_)

#     def __repr__(self):
#         return self.opponent_id +":"+str(self.seed_)

class MatchState():
    def __init__(self, message):
        self.position = None
        self.hand_number = None
        self.rounds = None
        self.cards = None
        self._decode_message(message)

    def _decode_message(self, message):
        splitted = message.split(":")
        self.position = splitted[1]
        self.hand_number = splitted[2]
        self.rounds = splitted[3].split("/")
        self.cards = splitted[4].split("/")

    def is_current_player_to_act(self):
        if len(self.rounds) == 1: # since the game uses reverse blinds
            if len(self.rounds[0]) % 2 == 0:
                current_player = 1
            else:
                current_player = 0
        else:
            if len(self.rounds[-1]) % 2 == 0:
                current_player = 0
            else:
                current_player = 1
        if int(self.position) == current_player:
            return True
        else:
            return False

    def __str__(self):
        msg = "\n"
        msg += "position: "+str(self.position)+"\n"
        msg += "hand_number: "+str(self.hand_number)+"\n"
        msg += "rounds: "+str(self.rounds)+"\n"
        msg += "cards: "+str(self.cards)+"\n"
        return msg

class PokerPlayer():

    def __init__(self, port):
        self.socket = socket.socket()
        self.socket.connect(("localhost", port))

    def initialize(self):
        pass

    def execute(self):
        self.socket.send("VERSION:2.0.0\r\n")
        message = self.socket.recv(1000)
        while message:
            message = message.replace("\r\n", "")
            print "message: "+str(message)
            for msg in message.split("MATCHSTATE"):
                if msg:
                    print "msg: "+str(msg)
                    match_state = MatchState(msg)
                    if match_state.is_current_player_to_act():
                        send_msg = "MATCHSTATE"+msg+":c\r\n"
                        self.socket.send(send_msg)
                        print "send_msg: "+str(send_msg)
                    else:
                        print "nothing to do"
            message = self.socket.recv(1000)
        self.finalize()

    def finalize(self):
        self.socket.close()

if __name__ == "__main__":
    port = int(sys.argv[1])
    PokerPlayer(port).execute()