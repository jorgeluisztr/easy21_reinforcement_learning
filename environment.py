import numpy as np

class easy21():

    def __init__(self):
        self.deck = np.arange(1,11)
        self.color = np.arange(1,4)
        self.playersum = np.random.choice(self.deck)
        self.dealerobserved = np.random.choice(self.deck)
        self.dealersum = self.dealerobserved
        self.end_game = False
        self.result = "unknown"

    def state(self):
        return self.playersum, self.dealerobserved

    def hit(self):
        if np.random.choice(self.color) < 3:
            return np.random.choice(self.deck)
        else:
            return -np.random.choice(self.deck)

    def is_game_end(self):
        self.end_game = True

    def turn(self, action):
        if action == 1:
            self.playersum = self.playersum + self.hit()
            if self.playersum < 1 or self.playersum > 21:
                self.is_game_end()
                self.result = "lose"
                return self.state(), -1
            else:
                return self.state(), 0
        else:
            while not self.end_game:
                if self.dealersum < 1 or self.dealersum >21:
                    self.is_game_end()
                    self.result = "win"
                    return self.state(), 1
                else:
                    if self.dealersum < 17:
                        self.dealersum = self.dealersum + self.hit()
                    if self.dealersum > 16 and self.dealersum < 22:
                        if self.dealersum < self.playersum:
                            self.is_game_end()
                            self.result = "win"
                            return self.state(), 1
                        elif self.dealersum == self.playersum:
                            self.is_game_end()
                            self.result = "draw"
                            return self.state(), 0
                        else:
                            self.is_game_end()
                            self.result = "lose"
                            return self.state(), -1