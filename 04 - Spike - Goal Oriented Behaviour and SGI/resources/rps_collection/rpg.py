'''Rock Paper ShotGun

Clinton Woodward, 2010, cwoodward@swin.edu.au

Please don't share this code without permission.

--------------------------------------------------------------------------------

This is an unbalanced version of the basic rock-paper-scissors game.

See the basic balanced game first for more details.

             |  Rock  |  Paper  | ShotGun
    ---------+--------+---------+----------
    Rock     |  Tie   |   Loss  |   Loss
    ---------+--------+---------+----------
    Paper    |  Win   |   Tie   |   Loss
    ---------+--------+---------+----------
    ShotGun  |  Win   |   Win   |   Tie
    ---------+--------+---------+----------

    * Cell values are for the "row" result


This simulation demonstrates the effect of unbiased and biased player strategies
in an un-balanced game.

Selecting a "dominant" strategy will result in more wins for a player,
regardless of other player choices (unlike a balanced game).

Alternatively, if the game was modified to include a "dominated" strategy, the
result would be more losses for the player.

The Lesson: In an unbalanced game, select a dominant strategy and win!

2019-03-15 Updated for python 3

'''

#===============================================================================

# What are the strategy choices?
choices = ('rock','paper','shotgun')

# Keep a dictionary of each strategy and strategies they dominate (as a list).
# 'dominates': 'dominated'
dominate = {
    'rock':    [],
    'paper':   ['rock'],
    'shotgun': ['rock','paper']
}

# Represent the game rules as a dictionary, where the "key" is a tuple of
# player choices (player1, player2), and the "value" is the win-tie-result for
# each player (again, as a tuple).
rules = {}
for a in choices:
    for b in choices:
        if a == b:
            rules[(a,b)] = ('tie','tie')
        elif b in dominate[a]:
            rules[(a,b)] = ('win','loss')
        else: # a in dominate[b]
            rules[(a,b)] = ('loss','win')

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
        p1_result, p2_result = rules[(p1,p2)]
        # Keep the results for later
        results['Player 1'][p1_result] += 1
        results['Player 2'][p2_result] += 1
        print('.', end=' ')
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
    return (random.choice(choices), 'paper')

def two_biased_player():
    return ('paper','shotgun')

#===============================================================================

if __name__ == '__main__':
    print('Unbiased Players::')
    play_games(uniform_players, 1000)
    print('One Biased Player (p2=paper)::')
    play_games(one_biased_player, 1000)
    print('Two Biased Players (p1=paper, p2=shotgun)::')
    play_games(two_biased_player, 1000)
