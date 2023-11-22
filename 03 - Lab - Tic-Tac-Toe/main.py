from gameManager_103071494 import GameManager

if __name__ == "__main__":
    game = GameManager()

    while game.gameRunning and not game.winner:
        game.processInput()
        game.updateBoard()
        game.renderBoard()

    game.showGameResult()
