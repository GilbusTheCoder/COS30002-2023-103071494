'''Rock Paper Scissors

Clinton Woodward, 2010, cwoodward@swin.edu.au

Please don't share this code without permission.

--------------------------------------------------------------------------------

Paper-Rock-Scissors is a simple example of game balance of three elements. Each
element -- rock, paper or scissors -- is dominated by one element, and dominates
the other, resulting in a "balanced" system. This can be expressed as a simple
matrix where rows are compared to columns.

             |  Rock  |  Paper  | Scissors
    ---------+--------+---------+----------
    Rock     |  Tie   |   Loss  |   Win
    ---------+--------+---------+----------
    Paper    |  Win   |   Tie   |   Loss
    ---------+--------+---------+----------
    Scissors |  Loss  |   Win   |   Tie
    ---------+--------+---------+----------

    * Cell values are for the "row" result

The game is played among two or more players, where the "winner" is the single
dominant player. If there are multiple equal and dominant players they compete
in elimination rounds until there is only one player remaining.

In a competition of players, each making uniform random choices in each round
of competition, then all players have the same balanced chance of winning and
losing. If one player uses a "biased" strategy against uniform random opponent,
the result is still balanced. If, however, both players choose different
biased strategies, the result is no longer balanced.

This simulation demonstrates the effect of unbiased and biased player strategies
in a balanced game.

The Lesson: In a balanced game...
 * all players with random strategy result in uniform random results
 * a biased strategy, against a random opponent, results in random results
 * a biased strategy, against a biased opponent, have biased results.


2019-03-15 Updated for python 3

'''
#===============================================================================

# What are the strategy choices?
choices = ('rock', 'paper', 'scissors')

# Keep a dictionary of each strategy and the strategy they dominate.
# 'dominates': 'dominated'
dominate = {
    'rock':     'scissors',
    'paper':    'rock',
    'scissors': 'paper'
}

# Represent the game rules as a dictionary, where the "key" is a tuple of
# player choices (player1, player2), and the "value" is the win-tie-result for
# each player (again, as a tuple).
rules = {}
for a in choices:
    for b in choices:
        if a == b:
            rules[(a, b)] = ('tie', 'tie')
        elif dominate[a] == b:
            rules[(a, b)] = ('win', 'loss')
        else: # dominate[b] == a
            rules[(a, b)] = ('loss', 'win')

#===============================================================================

def play_games(player_choices, rounds=1):
    results = {
        'Player 1': { 'win': 0, 'tie': 0, 'loss': 0 },
        'Player 2': { 'win': 0, 'tie': 0, 'loss': 0 },
    }

    for i in range(rounds):
#        print('--------------------------------------------------------------')
        # Each player makes a choice
        p1, p2 = player_choices()
        # Play the game (look up the results)
        p1_result, p2_result = rules[(p1,p2)]
        # Show the result
#        print('Player 1: %s, %s' % (p1, p1_result))
#        print('Player 2: %s, %s' % (p2, p2_result))
        # Keep the results for later
        results['Player 1'][p1_result] += 1
        results['Player 2'][p2_result] += 1
        print('.', end='')
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

def two_biased_player():
    return ('paper', 'scissors')

#===============================================================================

if __name__ == '__main__':
    print('Unbiased Players::')
    play_games(uniform_players, 1000)
    print('One Biased Player::')
    play_games(one_biased_player, 1000)
    print('Two Biased Players::')
    play_games(two_biased_player, 1000)
