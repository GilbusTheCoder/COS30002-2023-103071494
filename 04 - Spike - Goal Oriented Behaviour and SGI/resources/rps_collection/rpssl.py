'''Rock Paper Scissors Spock Lizard

Clinton Woodward, 2010, cwoodward@swin.edu.au

Please don't share this code without permission.

--------------------------------------------------------------------------------

Paper-Rock-Scissors-Spock-Lizard
    * Cell values are for the "row" result

             |  Rock  |  Paper  | Scissors | Spock  | Lizard
    ---------+--------+---------+----------+--------+----------
    Rock     |  Tie   |   Loss  |   Win    |  Loss  |  Win
    ---------+--------+---------+----------+--------+----------
    Paper    |  Win   |   Tie   |   Loss   |  Win   |  Loss
    ---------+--------+---------+----------+--------+----------
    Scissors |  Loss  |   Win   |   Tie    |  Loss  |  Win
    ---------+--------+---------+----------+--------+----------
    Spock    |  Win   |   Loss  |   Win    |  Tie   |  Loss
    ---------+--------+---------+----------+--------+----------
    Lizard   |  Loss  |   Win   |   Loss   |  Win   |  Tie
    ---------+--------+---------+----------+--------+----------

See http://www.samkass.com/theories/RPSSL.html
Still a balanced game. :)

Spock: vaporizes Rock, disproved by Paper, smashes Scissors, poisoned by Lizard
Lizard: smashed by Rock, eats Paper, decapitated by Scissors, poisons Spock

Note: There are a lot less "tie" results (only 1/5 of the total results).

The Lesson:
* More strategy options increases the number of outcomes -- less "tie" results.
  (In this case, only 1/5 of the total results will be ties in random games.)



2019-03-15 Updated for python 3

'''
#===============================================================================


# What are the strategy choices?
choices = ('rock', 'paper', 'scissors', 'spock', 'lizard')

# Keep a dictionary of each strategy and strategies they dominate (as a list).
# 'dominator': ['dominated',...]
dominate = {
    'rock':     ['scissors', 'lizard'],
    'paper':    ['rock',     'spock'],
    'scissors': ['paper',    'lizard'],
    'spock':    ['lizard',   'rock'],
    'lizard':   ['spock',    'paper'],
}

# Represent the game rules as a dictionary, where the "key" is a tuple of
# player choices (player1, player2), and the "value" is the win-tie-result for
# each player (again, as a tuple).
rules = {}
for a in choices:
    for b in choices:
        if a == b:
            rules[(a, b)] = ('tie', 'tie')
        elif b in dominate[a]:
            rules[(a, b)] = ('win', 'loss')
        else: # a in dominate[b]
            rules[(a, b)] = ('loss', 'win')

#===============================================================================

def play_games(player_choices, rounds=1):
    results = {
        'Player 1': { 'win': 0, 'tie': 0, 'loss': 0 },
        'Player 2': { 'win': 0, 'tie': 0, 'loss': 0 },
    }

    for i in range(rounds):
        # Each player makes a choice
        p1, p2 = player_choices()
        # Play the game (look up the results)
        p1_result, p2_result = rules[(p1, p2)]
        # Keep the results for later
        results['Player 1'][p1_result] += 1
        results['Player 2'][p2_result] += 1
        print('.', end="")
    # Show the final results
    print()
    print('Player 1:', results['Player 1'])
    print('Player 2:', results['Player 2'])
    print()


#===============================================================================

import random

def uniform_players():
    return (random.choice(choices), random.choice(choices))

def one_biased_player():
    return (random.choice(choices), 'scissors')

def two_biased_players():
    return ('paper', 'scissors')

def mostly_biased_players():
    if random.random() > 0.5:
        p1 = 'paper'
    else:
        p1 = random.choice(choices)

    if random.random() > 0.7:
        p2 = 'scissors'
    else:
        p2 = random.choice(choices)

    return (p1, p2)

#===============================================================================

if __name__ == '__main__':
    print('Unbiased Players::')
    play_games(uniform_players, 1000)
    print('One Biased Player::')
    play_games(one_biased_player, 1000)
    print('Two Biased Players::')
    play_games(two_biased_players, 1000)
    print('Mostly Biased Players::')
    play_games(mostly_biased_players, 1000)
