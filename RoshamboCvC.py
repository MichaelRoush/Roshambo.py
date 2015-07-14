import random

class WeightedRandom:
	def __init__(self):
		random.seed()
	def GetWeightedChoice(self, choiceDict): #Expecting something like {"ROCK":0, "PAPER":1, "SCISSORS":2} for choiceDict
		sumOfWeights = sum(choiceDict.values())
		rand = random.uniform(0,sumOfWeights)
		for c , w in choiceDict.items():
			if w > rand:
				return c
			rand -= w
	def GetUnweightedChoice(self, choiceList):
		return random.choice(choiceList)

class Decision:
	def __init__(self):
		self.trackerDict = {}
		self.weightedChoice = WeightedRandom()
		self.state = ("NULL",'N')
	def Update(self, newState, playerChoice):
		if not self.state == ("NULL", 'N'):
			if not self.state in self.trackerDict:
				self.trackerDict[self.state] = {"ROCK":0, "PAPER":0, "SCISSORS":0}
			self.trackerDict[self.state][playerChoice] += 1
		self.state = newState
	def PrintTrackerDict(self):
		print(self.trackerDict)
	def choice(self, choiceList):
		if self.state != ("NULL", 'N') and self.state in self.trackerDict:
			playerChoice = self.weightedChoice.GetWeightedChoice(self.trackerDict[self.state])
			if playerChoice == "ROCK":
				return "PAPER"
			elif playerChoice == "PAPER":
				return "SCISSORS"
			elif playerChoice == "SCISSORS":
				return "ROCK"
		return self.weightedChoice.GetUnweightedChoice(choiceList)
	def GetState(self):
		return self.state

class Hand:
	def __init__(self, choiceMaker):
		self.asciiDict = {"ROCK": ["  ___  ", " /,  \ ", "|   , |", " \___/ "], "PAPER": ["  ____ ", " /   / ", " \   \ ", " /___/ "], "SCISSORS": ["       ", " {]_[} ", "  )o(  ", " (/^\) "]}
		self.score = [0,0]
		self.choiceMaker = choiceMaker
		self.playerChoiceMaker = Decision()
	def Throw(self):
		compChoice = self.choiceMaker.choice(["ROCK", "PAPER", "SCISSORS"])
		playerChoice = self.playerChoiceMaker.choice(["ROCK", "PAPER", "SCISSORS"])
		if input("Continue (Y/N): ").upper() == "N":
			return False
		if playerChoice != "ROCK" and playerChoice != "PAPER" and playerChoice != "SCISSORS" and playerChoice != "EXIT" and playerChoice != "PRINTDICT":
			print("{0} is not a valid choice.".format(playerChoice))
			return True
		if playerChoice == "PRINTDICT":
			self.choiceMaker.PrintTrackerDict()
			return True
		if playerChoice == "EXIT":
			return False
		print()
		print("  YOU        COM")
		print("{0}    {1}".format(self.asciiDict[playerChoice][0], self.asciiDict[compChoice][0]))
		print("{0}    {1}".format(self.asciiDict[playerChoice][1], self.asciiDict[compChoice][1]))
		print("{0} vs {1}".format(self.asciiDict[playerChoice][2], self.asciiDict[compChoice][2]))
		print("{0}    {1}".format(self.asciiDict[playerChoice][3], self.asciiDict[compChoice][3]))
		print()
		result = ''
		if compChoice == "ROCK":
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
		self.choiceMaker.Update((playerChoice, result), playerChoice)
		self.playerChoiceMaker.Update((compChoice, result), compChoice)
		if result == 'D':
			print("The hand is a draw!")
		elif result == 'W':
			print("You win!")
			self.score[0] += 1
		elif result == 'L':
			print("The computer wins!")
			self.score[1] += 1
		print("Current score - Player: {0}, Computer: {1}".format(self.score[0],self.score[1]))
		return True

if __name__ == "__main__":
	decider = Decision()
	game = Hand(decider)
	while True:
		if game.Throw() == False:
			break
