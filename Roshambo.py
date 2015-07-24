#Simple Roshambo (Rock-Paper-Scissors) program, with AI
#By Michael Roush
#7-24-2015
#Python 3.4.0

#~~~NOTES~~~
#A lot of this was written so as to support further complexity,
#such as allowing for a game with X different choices instead of 3,
#or making a better AI for making choices. However, there is still
#a decent bit of code that would have to be rewritten in order to do so.
#Sorry about that.
#Peace.
#
#--Michael

import random

class WeightedRandom:                               #Class for getting random choices
    def __init__(self):
        random.seed()

    def GetWeightedChoice(self, choiceDict):        #Gets a random choice, taking into account a weight of each option. Expects a dictionary of (choice, weight) tuples.
        sumOfWeights = sum(choiceDict.values())     #Gets total value of all weights
        randTarget = random.uniform(0,sumOfWeights) #Picks a random number between 0 and the sum of all the weights
        for c , w in choiceDict.items():            #This is where the weighted choice actually happens.
            if w > randTarget:                      #  The function iterates over the choices in choiceDict.
                return c                            #  If the weight (w) of the choice (c) is greater than the target, it returns that choice.
            randTarget -= w                         #  Otherwise, it decreases the target by the weight of the current choice.

    def GetUnweightedChoice(self, choiceList):      #Gets a random choice
        return random.choice(choiceList)

class Decision:                                     #This class is the AI
    def __init__(self):
        self.trackerDict = {}
        self.weightedChoice = WeightedRandom()
        self.state = ("NULL",'N')
    
    def Update(self, newState, playerChoice):       #Updates the weights of the choices for the indicated state
        if not self.state == ("NULL", 'N'):         #Makes sure not in an invalid state
            if not self.state in self.trackerDict:  #If a weight list for the current state does not exist, creates it
                self.trackerDict[self.state] = {"ROCK":0, "PAPER":0, "SCISSORS":0}
            self.trackerDict[self.state][playerChoice] += 1     #Increase the weight for the indicated choice for the current state
        self.state = newState
    
    def PrintTrackerDict(self):                    #Prints the collection of state/weight lists
        print(self.trackerDict)                    #   Useful for debugging or getting an insight into the AI's decision making process.
                                                   #   Probably not actually needed, but I'm used to C# and always writing getter/setter functions
    
    def choice(self, choiceList):                   #Makes a choice by looking at the current state and its choices
        if self.state != ("NULL", 'N') and self.state in self.trackerDict:  #Checks to make sure it has an entry for the current state.
            playerChoice = self.weightedChoice.GetWeightedChoice(self.trackerDict[self.state])  #Makes a prediction of what the player will throw
            if playerChoice == "ROCK":              #Following lines just throw the hand that beats the predicted player choice
                return "PAPER"
            elif playerChoice == "PAPER":
                return "SCISSORS"
            elif playerChoice == "SCISSORS":
                return "ROCK"
        return self.weightedChoice.GetUnweightedChoice(choiceList)
    
    #def GetState(self):                            #Getter for state, probably not needed
    #    return self.state

class Hand:                                         #Class for actually getting player input and running the AI
    def __init__(self, choiceMaker):
        self.asciiDict = {"ROCK": ["  ___  ", " /,  \ ", "|   , |", " \___/ "], "PAPER": ["  ____ ", " /   / ", " \   \ ", " /___/ "], "SCISSORS": ["       ", " {]_[} ", "  )o(  ", " (/^\) "]}
        self.score = [0,0]
        self.choiceMaker = choiceMaker
    
    def Throw(self):                                #The game actually takes place here
        compChoice = self.choiceMaker.choice(["ROCK", "PAPER", "SCISSORS"]) #Calls the AI to make a choice
        playerChoice = input("Choose Rock, Paper, or Scissors (or Exit to quit): ").upper() #Gets player input
        if playerChoice != "ROCK" and playerChoice != "PAPER" and playerChoice != "SCISSORS" and playerChoice != "EXIT" and playerChoice != "QUIT":#Input error checking
            print("{0} is not a valid choice.".format(playerChoice))
            return True
        #if playerChoice == "PRINTDICT":            #Used for debugging or looking at the AI's "brain."
        #    self.choiceMaker.PrintTrackerDict()    #Need to add an option to error checking for this to be usable
        #    return True
        if playerChoice == "EXIT" or playerChoice == "QUIT":    #Quits. Duh.
            return False
        print()                                     #Formatting output, go!
        print("  YOU        COM")
        print("{0}    {1}".format(self.asciiDict[playerChoice][0], self.asciiDict[compChoice][0]))
        print("{0}    {1}".format(self.asciiDict[playerChoice][1], self.asciiDict[compChoice][1]))
        print("{0} vs {1}".format(self.asciiDict[playerChoice][2], self.asciiDict[compChoice][2]))
        print("{0}    {1}".format(self.asciiDict[playerChoice][3], self.asciiDict[compChoice][3]))
        print()
        if compChoice == "ROCK":                    #The next forever is checking all possible game states. I should probably come up with a more compact way to do this.
            if playerChoice == "ROCK":
                result = 'D'
            elif playerChoice == "PAPER":
                result = 'W'
            elif playerChoice == "SCISSORS":
                result = 'L'
        elif compChoice == "PAPER":
            if playerChoice == "PAPER":
                result = 'D'
            elif playerChoice == "SCISSORS":
                result = 'W'
            elif playerChoice == "ROCK":
                result = 'L'
        elif compChoice == "SCISSORS":
            if playerChoice == "SCISSORS":
                result = 'D'
            elif playerChoice == "ROCK":
                result = 'W'
            elif playerChoice == "PAPER":
                result = 'L'
        self.choiceMaker.Update((playerChoice, result), playerChoice)   #Makes the AI actually learn
        if result == 'D':                           #Makes updates to score and prints message based on result
            print("The hand is a draw!")
        elif result == 'W':
            print("You win!")
            self.score[0] += 1
        elif result == 'L':
            print("The computer wins!")
            self.score[1] += 1
        print("Current score - Player: {0}, Computer: {1}".format(self.score[0],self.score[1])) #Prints the score
        return True                                 #Returns True to continue playing

if __name__ == "__main__":
    decider = Decision()                            #Instantiate the AI
    game = Hand(decider)                            #Create a game with the AI
    while True:                                     #Starts the game, Python version of Do-While loop plays until Throw returns false (which only happens on exit input)
        if game.Throw() == False:
            break
