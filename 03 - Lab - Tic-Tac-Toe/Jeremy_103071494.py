# & Project: TicHackToe
# & Author: Thomas Horsley - 103071494
# & Date: 08/03/23

# * IMPORTANT
# * As there's so many comments contained in these files, I'd 110% recommend installing the
# * colorful comments VSCode extension to aid in readability.

#! ======================================================================================== !#
#!                                        Overview

# ^ This AI's name is Jeremy. Jeremy is fat. This is because Jeremy was designed with a
# ^ weighting system in mind. Jeremy is also designed to be a bit of a brainlet for fun
# ^ purposes.

# ^ Jeremy prioritizes corner moves over others as he believes opening as many lines to
# ^ a win condition as possible is the best way to play. Jeremy will consider the game-state
# ^ after it's move in order to prevent the player from winning (most the time ;p).

import random
from random import randrange


class WeightedAI:
    # ^ Generally the AI prefers corners however if there's none available it doesn't care
    # ^ This AI has 4 states, each correlate with specific behaviors (4th is default).
    __boardCornerElements = [0, 2, 6, 8]
    __lossConditions = [
        # ? Row check
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (3, 5),
        (4, 5),
        (6, 7),
        (6, 8),
        (7, 8),
        # ? Column Check
        (0, 3),
        (0, 6),
        (3, 6),
        (1, 4),
        (1, 7),
        (4, 7),
        (2, 5),
        (2, 8),
        (5, 8),
        # ? Diagonal Check
        (0, 4),
        (0, 8),
        (4, 8),
        (2, 4),
        (2, 6),
        (4, 6),
    ]

    __states = {
        0: "about to lose",  # ? "about to lose",
        1: "corners free",  # ? "corners free",
        2: "default",  # ? "no corners free",
    }

    def __init__(self, players: dict, winConditions: tuple, initialBoard: list):
        self.players = players
        self.winConditions = list(winConditions)
        self.gameBoard = initialBoard

        self.decisionBoard = self.gameBoard
        self.currentLossCondition = None
        self.move = None

        self.currentState = self.__states.get(1)
        self.canMakeSavingThrow = True
        self.isAboutToLose = False
        self.isCornerFree = True

    #! ==================================================================================== !#
    #!                              Update and Move Logic

    # ^ Called on update function in gameManager to pass the current game-state to the AI
    # ^ in order for the AI to copy it and privately do logic on that board.
    # ^ Then return a move.

    # Todo: Based on the current state of the board, return a move relative to that board state.
    def makeMove(self, board: list):
        self.gameBoard = board
        self.decisionBoard = self.gameBoard

        self.currentState = self.evaluatePosition()
        # ^ Using a dictionary of game-states in order to control the AI's priorities.

        if self.currentState is self.__states.get(2):
            self.move = self.makeRandomMove()

        if self.currentState is self.__states.get(1):
            self.move = self.makeCornerMove()

        if self.currentState is self.__states.get(0):
            self.move = self.makeSavingMove()

        self.removeLossConditionOnMove()
        return self.move

    # Todo: Returns a saving move the AI will make when threatened with losing
    def makeSavingMove(self) -> int:
        self.move = self.evaluateOnlyMove()
        return self.move

    # Todo: Returns a random number as a move
    def makeRandomMove(self) -> int:
        self.move = randrange(9)
        return self.move

    # Todo: Returns a Corner move
    def makeCornerMove(self) -> int:
        freeCorners = self.generateCornerMoves()
        self.move = random.choice(freeCorners)
        self.move = int(self.move)
        return self.move

    #! ==================================================================================== !#
    #!                                 The Evaluation Station

    # Todo: Checks a bunch of things to do with the game-state and returns the most
    # todo: pressing issue
    def evaluatePosition(self) -> str:
        # ? Start by evaluating if AI is going to eat it next turn
        # ? If not then check for corners
        # ? If no corners make a random move for now
        currentState = self.__states.get(2)

        self.checkIfCornersAreFree()
        self.checkStateForLoss()

        if self.isCornerFree is True:
            currentState = self.__states.get(1)

        if self.isAboutToLose is True and self.canMakeSavingThrow is True:
            currentState = self.__states.get(0)
            self.canMakeSavingThrow = False

        return currentState

    #! ==================================================================================== !#
    #!                                 About to Lose Logic

    # Todo: Checks the losing position against current
    def checkStateForLoss(self) -> bool:
        losingPosition = self.returnLossConditionIndex()

        # ? if this throws an error turn the losing condition into a set
        if losingPosition != 30:
            losingCondition = self.__lossConditions[losingPosition]
            if self.currentLossCondition <= list(losingCondition):
                self.isAboutToLose = True
                return self.isAboutToLose
            else:
                self.isAboutToLose = False

            return self.isAboutToLose

        return False

    # Todo: Checks each position for a lose condition and updates AI if a
    # todo: loss condition is found. Returns the index of the loss condition
    # todo: for comparison.
    def returnLossConditionIndex(self) -> int:
        loseConditions = self.__lossConditions
        decisionBoard = self.decisionBoard

        for conditionSet, condition in enumerate(loseConditions):
            if decisionBoard[condition[0]] == decisionBoard[condition[1]] == "x":
                self.currentLossCondition = list(loseConditions[conditionSet])
                # ? set the AI's current loss condition to the tuple at
                # ? loseConditions[index]

                return conditionSet
            else:
                self.currentLossCondition = None

        return 30
        # ? Makeshift error code. Will remove if remember, but lets
        # ? not hold our breath

    # Todo: Run through the loss conditions and remove the loss condition equal
    # todo: to the current loss condition. This is done for the same reason as
    # todo: the win conditions.

    # Todo: Return the modified version of self.lossConditions
    def removeLossConditionOnMove(self) -> list:
        lossConditions = self.__lossConditions
        removedConditions = []
        iterableMove = [self.move]

        for conditionIndex, condition in enumerate(lossConditions):
            if set(iterableMove).issubset(condition):
                removedConditions.append(lossConditions[conditionIndex])

        self.__lossConditions = list(set(lossConditions).difference(removedConditions))
        return self.__lossConditions

    # Todo: Return the position of the player move which would cause the loss
    # todo: the loss condition.
    def evaluateOnlyMove(self) -> int:
        # * I have the current loss condition tuple stored
        # * I have the win conditions of the game as tuple

        # ? Compare the current loss condition with each of the win conditions.
        # ? If the loss condition is a subset of a win condition then cache
        # ? the win condition in a list remove the elements common with the loss
        # ? condition.

        # ? Remove the winCondition and the lossCondition from the AI's list
        # ? as the AI's move will automatically prevent those positions from
        # ? occurring.
        # ? Return loss position as int

        lossCondition = self.currentLossCondition
        winConditions = self.winConditions

        for condition in winConditions:
            if set(lossCondition).issubset(condition):
                winCondition = list(condition)
                # ? ^^^ Track this value to remove the contained loss conditions

                for position in winCondition[:]:
                    if position in lossCondition:
                        winCondition.remove(position)
                return int(winCondition[0])

    #! ==================================================================================== !#
    #!                               Corner Preference Logic

    # Todo: Check if corners are available and return array of all the free corners
    def generateCornerMoves(self) -> list:
        # ^ Checks the corners elements of the board for a space and returns a list
        # ^ of equally valid positions
        availableCorners = []

        for position, move in enumerate(self.gameBoard):
            if position in self.__boardCornerElements and move == " ":
                availableCorners.append(position)

        return availableCorners

    def selectCornerMove(self) -> int:
        availableMoves = self.generateCornerMoves()
        move = random.choice(availableMoves, k=len(availableMoves))
        move = move
        return move

    # Todo: Check to see if corners are free. Will take the available corners every update
    # todo: will return true if corners are free and false if not.
    def checkIfCornersAreFree(self) -> bool:
        availableCorners = self.generateCornerMoves()

        if len(availableCorners) > 0:
            self.isCornerFree = True
            return self.isCornerFree
        else:
            self.isCornerFree = False
            return self.isCornerFree
