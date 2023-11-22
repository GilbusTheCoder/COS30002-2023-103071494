"""Rock Paper Scissors/Shotgun + Memory AI Bot

Clinton Woodward, 2010, cwoodward@swin.edu.au

Please don't share this code without permission.

--------------------------------------------------------------------------------

Create PlayerBot's which are each asked for their "move" choice, and are then
notified about the game result.


The Lesson:
 * Against a biased player, use "memory" to select dominant strategy.
 * Memory can be either the other players move, or simply the outcome.
 * Stored knowledge of known "dominant" strategies is better than "discovery"
   of dominant strategy (but only if such knowledge is available!)


2019-03-15 Updated for python 3

"""

# ===============================================================================

choices = ("rock", "paper", "scissors")
# 'dominates': 'dominated'
dominate = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

# Represent the game rules as a dictionary, where the "key" is a tuple of
# player choices (player1, player2), and the "value" is the win-tie-result for
# each player (again, as a tuple).
rules = {}
for a in choices:
    for b in choices:
        if a == b:
            rules[(a, b)] = ("tie", "tie")
        elif dominate[a] == b:
            rules[(a, b)] = ("win", "loss")
        else:  # dominate[b] == a
            rules[(a, b)] = ("loss", "win")

# ===============================================================================


def play_games(player1, player2, rounds=1):
    results = {
        "Player 1": {"win": 0, "tie": 0, "loss": 0},
        "Player 2": {"win": 0, "tie": 0, "loss": 0},
    }

    for i in range(rounds):
        p1_move = player1.move()
        p2_move = player2.move()
        # Play the game (look up the results)
        p1_result, p2_result = rules[(p1_move, p2_move)]
        # Notify each player of the result
        player1.notify(p1_result, p2_move)
        player2.notify(p2_result, p1_move)
        # Keep the results for later
        results["Player 1"][p1_result] += 1
        results["Player 2"][p2_result] += 1
    # Show the final results
    print("Player 1:", results["Player 1"])
    print("Player 2:", results["Player 2"])
    print()


# ===============================================================================


import random


class BotPlayer(object):
    def __init__(self):
        self.last_move = random.choice(choices)
        self.last_result = ""
        self.opp_move = ""

    def notify(self, result, opp_move):
        self.last_result = result
        self.opp_move = opp_move


#    def move(self):
#        pass


class RandomBot(BotPlayer):
    """Simple uniform random move each time"""

    def move(self):
        return random.choice(choices)


class RandomBiasBot(BotPlayer):
    """Select an initial random move and stick to it"""

    def __init__(self):
        super(RandomBiasBot, self).__init__()
        #self.last_move = random.choice(choices) # ? Don't think this line is necessary

    def move(self):
        return self.last_move


class OutcomeMemoryBot(BotPlayer):
    """Remember game outcome and our last move - select dominant strategy."""

    def move(self):
        # Loss? Tie? (or first move)
        if self.last_result in ["loss", "tie", ""]:
            self.last_move = random.choice(choices)
            return self.last_move
        # Return the new move, or we won last time, so return it...
        return self.last_move


class OpponentMemoryBot(BotPlayer):
    """Remember the opponents move - select dominant strategy."""

    def move(self):
        if self.last_result == "":
            self.last_move = random.choice(choices)
        elif self.last_result in ["loss", "tie"]:
            # find a dominant strategy for the opponents last move
            for key, values in dominate.items():
                if self.opp_move in values:
                    self.last_move = key
                    break
        # Return new move, or
        return self.last_move


class RandomRepeaterBot(BotPlayer):
    def __init__(self):
        super(RandomRepeaterBot, self).__init__()
        self.count_limit = 0
        self.count = 0

    def move(self):
        # make a choice and use it for a random number of times
        self.count += 1
        if self.count > self.count_limit:
            self.count = 0
            self.count_limit = random.randrange(0, 10)  # [0 ... 9]
            self.last_move = random.choice(choices)
        return self.last_move


class RandomBotBot(BotPlayer):
    """Select a random bot strategy to try... from a pool."""

    def __init__(self):
        self.bots = [
            RandomRepeaterBot(),
            OutcomeMemoryBot(),
            OpponentMemoryBot(),
            RandomBiasBot(),
        ]

    def notify(self, result, opp_move):
        for bot in self.bots:
            bot.last_result = result
            bot.opp_move = opp_move

    def move(self):
        bot = random.choice(self.bots)
        return bot.move()


# ===============================================================================

if __name__ == "__main__":

    print("Unbiased Players::")
    play_games(RandomBot(), RandomBot(), 1000)
    print("One Biased Player::")
    play_games(RandomBot(), RandomBiasBot(), 1000)
    print("Two Biased Players::")
    play_games(RandomBiasBot(), RandomBiasBot(), 1000)

    print("BiasedBot vs OutcomeMemoryBot::")
    play_games(RandomBiasBot(), OutcomeMemoryBot(), 1000)
    print("BiasedBot vs OpponentMemoryBot::")
    play_games(RandomBiasBot(), OpponentMemoryBot(), 1000)

    print("RandomRepeater vs OutcomeMemoryBot::")
    play_games(RandomRepeaterBot(), OutcomeMemoryBot(), 1000)
    print("Random Repeater vs OpponentMemoryBot::")
    play_games(RandomRepeaterBot(), OpponentMemoryBot(), 1000)

    print("OutcomeMemoryBotMemoryBot vs OpponentMemoryBot::")
    play_games(OutcomeMemoryBot(), RandomBotBot(), 1000)
