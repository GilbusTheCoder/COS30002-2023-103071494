# & Project: TicHackToe
# & Author: Thomas Horsley - 103071494
# & Date: 08/03/23

# * IMPORTANT
# * As there's so many comments contained in these files, I'd 110% recommend installing the
# * colorful comments VSCode extension to aid in readability.
# *
# * Additionally, much of this files code is either copied or refactored from the
# * tictactoe_cli_oo.py file which is credited to the Swinburne University COS30002.

#! ========================================================================================#
#!                                        Overview

from Jeremy_103071494 import WeightedAI
from Randy_103071494 import RandomAI


class GameManager(object):
    winConditions = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def __init__(self):
        self.board = [" "] * 9
        self.winner = None
        self.gameRunning = True
        self.gameTurn = 0

        self.move = None
        self.players = {"x": "Randy (Random)", "o": "Jeremy (Weighted)"}
        self.currentPlayer = "x"

        self.weightedAI = WeightedAI(self.players, self.winConditions, self.board)
        self.randomAI = RandomAI()

        self.initializeGame()

    #! ==================================================================================== !#
    #!                          Display & Tutorial Functionality

    # Todo: Performs setup and tutorial
    def initializeGame(self):
        self.tutorial()
        self.renderBoard()

    # Todo: Prints a tutorial and provides commands for more information
    def tutorial(self):
        # ? Presents startup screen and game tutorial information
        tutorialScript = """
        *************** Welcome to TicTacToe vs Ai ***************
        The legal moves correspond to the grid displayed below.
        if you're unsure of win conditions, type --help.

        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8    

        Input --help or press enter to continue: 
        """

        print(tutorialScript)
        self.showWinCondition()

    # Todo: Present all the win conditions in string format when asked
    def showWinCondition(self):
        winConditions = self.winConditions
        self.doShowWinConditions = input()

        if self.doShowWinConditions == "--help":
            print("******** Win Conditions *********\n")
            print(
                "By gaining all tiles listed in any one of the following sets the player will win!"
            )
            print("%s, %s, %s, %s" % tuple(winConditions[:4]))
            print("%s, %s, %s, %s" % tuple(winConditions[4:]))

    #! ==================================================================================== !#
    #!                          Legality checks and Red Tape

    def checkMoveLegal(self):
        # ? Allowed moves are 0-8, Cell must be empty
        # ? Return True if move is legal
        # ? Return False with err if move is int but position taken
        # ? Return False with err if move is illegal and dumb

        try:
            self.move = int(self.move)
            if self.board[self.move] == " ":
                return True
            else:
                print("Position %s is already taken!" % self.move)
                return False
        except Exception:
            print(
                "%s is an illegal move! Please enter an empty cell with integer value in range 0-8."
                % self.move
            )
            return False

    def resultCheck(self):
        board = self.board
        winConditions = self.winConditions

        # ? Check to see if any of our win conditions match the board state
        # ? return the winner if the win condition is met
        # ? return tie if there's no spaces left and no winner determined
        # ? return false if the game is ongoing

        for row in winConditions:
            if board[row[0]] == board[row[1]] == board[row[2]] != " ":
                return board[row[0]]

        if " " not in board:
            return "tie"

        return None

    def showGameResult(self):
        # ? The winner will be the current player at the end of the game
        # ? Therefore cases only needed for tie and win condition

        print("=" * 27)
        if self.winner == "tie":
            print("**** TIE! ****")
        else:
            print("The winner is: %s!!!" % self.players[self.winner])

        print("=" * 27)
        print("******** Game Over ********")

        #! ==================================================================================== !#
        #!                                Input Functionality

        # def getHumanInput(self):
        # ? Prompt and return human user input
        # return input(">>>> Enter value between 0-8: ")
        # ? Randy's turn!

    def getAiRandInput(self):
        return self.randomAI.makeMove()

    def getAiWeightedInput(self):
        # ? Time for Jeremy to do something
        aiBoard = self.board
        return self.weightedAI.makeMove(aiBoard)

    #! ==================================================================================== !#
    #!                             Update and Render Logic

    # Todo: Get each of the player's next moves and store them in the move var
    def processInput(self):

        if self.currentPlayer == "x":
            self.gameTurn += 1
            self.move = self.getAiRandInput()
        else:
            self.move = self.getAiWeightedInput()

    # Todo: If the current move is legal, update the board position at that move with the current
    # todo: player's key
    def updateBoard(self):
        # ? Check if the occurring position results in a win
        # ? Swap current player.
        if self.checkMoveLegal():
            self.board[self.move] = self.currentPlayer
            self.winner = self.resultCheck()

            # ? Will unconditionally swap the current player
            if self.currentPlayer == "x":
                self.currentPlayer = "o"
            else:
                self.currentPlayer = "x"

        else:
            print("Something went wrong, try again.")

    # Todo: Prints the values held within the board,
    def renderBoard(self):
        # ? Takes a reference to the game turn and the game board
        # ? Is updated and called each game turn
        board = self.board
        gameTurn = self.gameTurn

        print("\nBoard: Turn %s \n" % gameTurn)
        print("    %s | %s | %s" % tuple(board[:3]))
        print("   -----------")
        print("    %s | %s | %s" % tuple(board[3:6]))
        print("   -----------")
        print("    %s | %s | %s" % tuple(board[6:]))

        if self.winner == None:
            print("The current player is: %s" % self.players[self.currentPlayer])
