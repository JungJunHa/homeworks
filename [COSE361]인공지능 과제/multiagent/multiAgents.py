# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghostpos = successorGameState.getGhostPositions()
        # print(ghostpos)
        ghost_distance = [((newPos[0]-ghost[0])**2 + (newPos[1]-ghost[1])**2)**0.5 for ghost in ghostpos]
        layout = currentGameState.getWalls()
        maxlength = layout.height -2 + layout.width -2
        # print(ghost_distance)
        # for distance in ghost_distance:
        #     if distance <5:
        # print(newFood)
        food_distance = [((newPos[0]-food[0])**2 + (newPos[1]-food[1])**2)**0.5 for food in newFood.asList()]
        # print(newFood.asList())
        min_food_distance = float('inf')
        for food in food_distance:
            min_food_distance = min(min_food_distance, food)
        min_ghost_distance = float('inf')
        for ghost in ghost_distance:
            min_ghost_distance = min(ghost, min_ghost_distance)
        score = 0
        if currentGameState.getFood()[newPos[0]][newPos[1]]:
            score += 10
        if min_ghost_distance < 3:
            score -= 500
        # print(min_food_distance)
        # print(min_ghost_distance)
        score = score + 3.0/min_food_distance + min_ghost_distance/maxlength
        # print(score)
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        result = self.cal_value(state, 0, 0)

        return result[1]

    def cal_value(self, state, agentIndex, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return state.getScore(), ""
        if agentIndex == 0:
            return self.maximum_score(state, agentIndex, depth)
        else:
            return self.minimum_score(state, agentIndex, depth)

    def maximum_score(self, state, agentIndex, depth):
        
        legalactions = state.getLegalActions(agentIndex)
        v = float("-inf")
        max_actions = ""

        for action in legalactions:
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), 0, depth+1)[0]
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)[0]

            if now_value > v:
                v = now_value
                max_actions = action

        return v, max_actions

    def minimum_score(self, state, agentIndex, depth):
        
        legalactions = state.getLegalActions(agentIndex)
        v = float("inf")
        min_actions = ""

        for action in legalactions:
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), 0, depth+1)[0]
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)[0]

            if now_value < v:
                v = now_value
                min_actions = action

        return v, min_actions

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        result = self.cal_value(state, float('-inf'), float('inf'), 0, 0)

        return result[1]

    def cal_value(self, state, alpha, beta, agentIndex, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return state.getScore(), ""
        if agentIndex == 0:
            return self.maximum_score(state, alpha, beta, agentIndex, depth)
        else:
            return self.minimum_score(state, alpha, beta, agentIndex, depth)

    def maximum_score(self, state, alpha, beta, agentIndex, depth):
        
        legalactions = state.getLegalActions(agentIndex)
        v = float("-inf")
        max_actions = ""

        for action in legalactions:
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, 0, depth+1)[0]
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, agentIndex + 1, depth)[0]

            if now_value > v:
                v = now_value
                max_actions = action
            alpha = max(alpha, v)

            if v > beta:
                return v, max_actions
        return v, max_actions

    def minimum_score(self, state, alpha, beta, agentIndex, depth):
        
        legalactions = state.getLegalActions(agentIndex)
        v = float("inf")
        min_actions = ""

        for action in legalactions:
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, 0, depth+1)[0]
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, agentIndex + 1, depth)[0]

            if now_value < v:
                v = now_value
                min_actions = action
            beta = min(beta, v)

            if v < alpha:
                return v, min_actions
        return v, min_actions

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
