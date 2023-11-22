# The 3 most prominent states of my dog have been wrapped in this script

# Variables
isGameRunning = True
gameTime = 0
gameTimeMax = 100

isAlive = True
states = ["receiving attention", "inhaling food", "drinking obnoxiously", "resting"]
currentState = "receiving attention"

happiness = 10  # High happiness is good
thirst = 10  # Low thirst is bad
hunger = 10  # Low hunger is bad


while isGameRunning and isAlive:
    gameTime += 1

    # Attention Grabbing: Gains happiness, Loses thirst and hunger
    if currentState == "receiving attention":
        print("**Drool**")
        happiness += 2
        thirst -= 1
        hunger -= 2

        if hunger < 4:
            currentState = "inhaling food"
        if thirst < 4:
            currentState = "drinking obnoxiously"
        if happiness > 12:
            currentState = "resting"

    # Eating: gains happiness and hunger, loses thirst
    elif currentState == "inhaling food":
        print("**Wet Schmack and the occasional growl**")
        happiness += 1
        hunger += 4
        thirst -= 1

        if thirst < 4:
            currentState = "drinking obnoxiously"
        if hunger > 12:
            currentState = "resting"

    # Drinking: gains thirst, loses happiness and hunger
    elif currentState == "drinking obnoxiously":
        print("**SMACK SMACK SMACK**")
        happiness -= 1
        hunger -= 1
        thirst += 4

        if happiness < 6:
            currentState = "receiving attention"
        if hunger < 4:
            currentState = "inhaling food"
        if thirst > 12:
            currentState = "resting"

    # Idle: Just sleeps
    elif currentState == "resting":
        print("**snore snore snore**")
        happiness -= 1
        hunger -= 2
        thirst -= 1

        if happiness < 6:
            currentState = "receiving attention"
        if hunger < 4:
            currentState = "inhaling food"
        if thirst < 6:
            currentState = "drinking obnoxiously"

    # Catch broken logic
    else:
        print("something goofed")

    # Terminates the loop after the maxGameTime is reached
    if gameTime > gameTimeMax:
        isGameRunning = False

print("-*-*-* Finished *-*-*-")
