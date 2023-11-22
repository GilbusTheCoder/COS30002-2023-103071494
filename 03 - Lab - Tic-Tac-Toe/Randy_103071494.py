# & Project: TicHackToe
# & Author: Thomas Horsley - 103071494
# & Date: 08/03/23

# * IMPORTANT
# * As there's so many comments contained in these files, I'd 110% recommend installing the
# * colorful comments VSCode extension to aid in readability.

#! ======================================================================================== !#
#!                                        Overview

# ^ This is Randy, Randy is pretty unpredictable and has the mental capacity of a red brick.
# ^ Randy will chose moves at random but will always put a piece in the middle of the board.

# ^ Funnily enough though, these 10 lines of code are better than Jeremy. It's a bit sad ik but
# ^ I'm pretty sure this guy cheats.

from random import randrange


class RandomAI:
    def __init__(self):
        self.move: int = None

    def makeMove(self) -> int:
        move = randrange(9)
        self.move = move
        return self.move
