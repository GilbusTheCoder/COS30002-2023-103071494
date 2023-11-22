
# & Project: Task04<Spike> -- Goal Oriented Behaviour
# &  Author: Thomas Horsley -- 103071494
# &    Date: 16/03/23

# * IMPORTANT
# * As there's so many comments contained in these files, I'd 110% recommend installing the
# * colorful comments VSCode extension to aid in readability.


class Agent:
    goals = {"Hunger": 3, "Thirst": 2, "Attention": 6}

    actions = {
        "eat snack": {"Hunger": -2},
        "eat meal": {"Hunger": -4},
        "drink water": {"Thirst": -3},
        "drink puddle": {"Thirst": -1},
        "receive attention": {"Attention": -2},
    }

    def __init__(self):
        #self.printActions()
        self.runUntilSatisfied()

    # Todo: Function prints all the available actions to the agent
    def printActions(self):
        actions = self.actions
        for actionName, goalAffect in actions.items():
            print(f"{actionName}: {str(goalAffect)}")

    def printGoals(self):
        goals = self.goals

        print("GOALS: ")
        for name, insistenceVal in goals.items():
            print(f"\t {name}, {insistenceVal}")

    # Todo: Takes and action from the list of actions and applies the goal
    # todo: modifier value to the goals insistence.
    def applyAction(self, action):
        actions = self.actions

        # ? Applies the actions insistence modifier to all the goal insistence
        # ? values contained within the agent.
        for goalReference, insistenceModifier in actions[action].items():
            self.goals[goalReference] = max(
                self.goals[goalReference] + insistenceModifier, 0
            )  # ?              Clamp the minimum values to 0 ^^^.

    # Todo: Takes an action and a goal and returns a measure (as int) of the
    # todo: actual value that action has on the agents outcome.
    # ? The larger the utility value the more beneficial the action is.
    def getActionUtility(self, action, goal):
        actions = self.actions
        if goal in actions[action]:
            return -actions[action][goal]

    # Todo: Will return the best possible action choice relative to the current
    # todo: most insistent goal.
    def chooseAction(self):
        goals = self.goals
        actions = self.actions
        bestAction = None
        bestUtility = 100

        # ? Check if there are goals and actions available
        assert len(goals) > 0, "Err: Cannot find goals dict."
        assert len(actions) > 0, "Err: Cannot find actions dict."

        # ? Very cool line of code Clinton.
        insistentGoal, insistentGoalValue = max(goals.items(), key=lambda item: item[1])

        # ? Check through each action in our actions dict
        # ? If the most insistent goal is contained within the actions dict
        # ? check if the current best action is none
        for actionName, actionModifier in actions.items():
            if bestAction is None:
                if insistentGoal in actionModifier:
                    bestAction = actionName
                    bestUtility = self.getActionUtility(bestAction, insistentGoal)
                    
                    try:
                        bestUtility = int(bestUtility)
                    except:
                        print("Err: bestUtility is not of type <int>.")

            else:
                if insistentGoal in actionModifier:
                    currentUtility = self.getActionUtility(bestAction, insistentGoal)
                    try:
                        currentUtility = int(currentUtility)
                        if currentUtility > bestUtility:
                            bestAction = actionName
                            bestUtility = currentUtility
                    except:
                        print("Err: currentUtility is not of type <int>.")

        return bestAction

    # Todo: Runs a simple check to see if the AI's needs have been satisfied
    def checkIsSatisfied(self) -> bool:
        goals = self.goals
        insistenceSum = 0
        for goalName, goalInsistence in goals.items():
            insistenceSum += goalInsistence

        if insistenceSum > 0:
            return True
        else:
            return False

    # Todo: Loop until the AI has satisfied all of their needs
    def runUntilSatisfied(self):
        running = True

        while running == True:
            self.printGoals()

            action = self.chooseAction()
            print(f"BEST_ACTION: {action}")

            self.applyAction(action)
            self.printGoals()

            running = self.checkIsSatisfied()

        print(">> Finito <<")
