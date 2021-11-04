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
        #ghost의 position들을 구하는 것이다.
        ghostpos = successorGameState.getGhostPositions()
        #ghost의 distance를 구해서 list로 만들기
        ghost_distance = [((newPos[0]-ghost[0])**2 + (newPos[1]-ghost[1])**2)**0.5 for ghost in ghostpos]
        #getwalls 함수를 통해 맵의 높이와 너비를 가져온다.
        layout = currentGameState.getWalls()
        maxlength = layout.height -2 + layout.width -2
        #남은 food까지의 distance를 구한다.(newfood에서 aslist를 이용)
        food_distance = [((newPos[0]-food[0])**2 + (newPos[1]-food[1])**2)**0.5 for food in newFood.asList()]
        #distance 비교를 위해 food distance, ghost distance 첫번째를 모두 무한으로 두고, minimum인 food distance와 ghost distance를 구한다.
        min_food_distance = float('inf')
        for food in food_distance:
            min_food_distance = min(min_food_distance, food)
        min_ghost_distance = float('inf')
        for ghost in ghost_distance:
            min_ghost_distance = min(ghost, min_ghost_distance)
        #score을 다시 설정한다.
        score = 0
        #food를 먹으면 10점
        if currentGameState.getFood()[newPos[0]][newPos[1]]:
            score += 10
        #ghost와의 거리가 3보다 떨어지면 -500점
        if min_ghost_distance < 3:
            score -= 500
        #이를 바탕으로 score 체계를 다시 짜본다.
        score = score + 3.0/min_food_distance + min_ghost_distance/maxlength
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
        #score, action으로 result가 나오고, 이 중에서 action을 return한다.
        return result[1]

    def cal_value(self, state, agentIndex, depth):
        #state에서 승패가 결정되거나 depth가 꽉 찼다면 멈춘다.
        if state.isWin() or state.isLose() or depth == self.depth:
            return state.getScore(), ""
        #Pacman의 index가 0이므로 maximum score 구해준다.
        if agentIndex == 0:
            return self.maximum_score(state, agentIndex, depth)
        #다를 때는 ghost의 index이므로 minimum score을 구해준다.
        else:
            return self.minimum_score(state, agentIndex, depth)

    def maximum_score(self, state, agentIndex, depth):
        #움직일 수 있는 action들과 value 값인 v(일단 -무한대를 넣어준다 - 극한), 아직 비어있는 max_action을 만들어준다.
        legalactions = state.getLegalActions(agentIndex)
        v = float("-inf")
        max_actions = ""
        #legalactions(움직일 수 있는 action들) 중에서 action을 선택
        for action in legalactions:
            #agentindex로 봤을 때 이게 pacman인 경우
            #successor의 state와 agentindex(pacman이니까 0), depth+1로 value를 구해 now_value에 저장
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), 0, depth+1)[0]
            #아니면 pacman이 아닌 경우니 successor의 state와 index의 증가, depth를 통해 value를 구함
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)[0]
            #원래 value와 구한 value의 대소를 비교하여 maximum score을 구하는 과정을 거침
            if now_value > v:
                v = now_value
                max_actions = action

        return v, max_actions

    def minimum_score(self, state, agentIndex, depth):
        #움직일 수 있는 action들과 value 값인 v(일단 무한대를 넣어준다 - 극한), 아직 비어있는 min_action을 만들어준다.
        legalactions = state.getLegalActions(agentIndex)
        v = float("inf")
        min_actions = ""
        #legalactions(움직일 수 있는 action들) 중에서 action을 선택
        for action in legalactions:
            #successor의 state와 agentindex(pacman이니까 0), depth+1로 value를 구해 now_value에 저장
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), 0, depth+1)[0]
            #아니면 pacman이 아닌 경우니 successor의 state와 index의 증가, depth를 통해 value를 구함
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth)[0]
            #원래 value와 구한 value의 대소를 비교하여 minimum score을 구하는 과정을 거침
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
        #score, action으로 result가 나오고, 이 중에서 action을 return한다.
        return result[1]

    def cal_value(self, state, alpha, beta, agentIndex, depth):
        #state에서 승패가 결정되거나 depth가 꽉 찼다면 멈춘다.
        if state.isWin() or state.isLose() or depth == self.depth:
            return state.getScore(), ""
        #Pacman의 index가 0이므로 maximum score 구해준다.
        if agentIndex == 0:
            return self.maximum_score(state, alpha, beta, agentIndex, depth)
        #다를 때는 ghost의 index이므로 minimum score을 구해준다.
        else:
            return self.minimum_score(state, alpha, beta, agentIndex, depth)

    def maximum_score(self, state, alpha, beta, agentIndex, depth):
        #움직일 수 있는 action들과 value 값인 v(일단 -무한대를 넣어준다 - 극한), 아직 비어있는 max_action을 만들어준다.
        legalactions = state.getLegalActions(agentIndex)
        v = float("-inf")
        max_actions = ""
        #legalactions(움직일 수 있는 action들) 중에서 action을 선택
        for action in legalactions:
            #agentindex로 봤을 때 이게 pacman인 경우
            #successor의 state와 agentindex(pacman이니까 0), depth+1로 value를 구해 now_value에 저장
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, 0, depth+1)[0]
            #아니면 pacman이 아닌 경우니 successor의 state와 index의 증가, depth를 통해 value를 구함
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, agentIndex + 1, depth)[0]
            #원래 value와 구한 value의 대소를 비교하여 maximum score을 구하는 과정을 거침
            if now_value > v:
                v = now_value
                max_actions = action
            #alpha 값을 update해줌 - alpha는 max의 best option
            alpha = max(alpha, v)
            #beta와 비교하여 value가 beta보다 크면 pruning 과정 실행
            if v > beta:
                return v, max_actions
        return v, max_actions

    def minimum_score(self, state, alpha, beta, agentIndex, depth):
        #움직일 수 있는 action들과 value 값인 v(일단 무한대를 넣어준다 - 극한), 아직 비어있는 min_action을 만들어준다.
        legalactions = state.getLegalActions(agentIndex)
        v = float("inf")
        min_actions = ""
        #legalactions(움직일 수 있는 action들) 중에서 action을 선택
        for action in legalactions:
            #successor의 state와 agentindex(pacman이니까 0), depth+1로 value를 구해 now_value에 저장
            if agentIndex == state.getNumAgents()-1:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, 0, depth+1)[0]
            #아니면 pacman이 아닌 경우니 successor의 state와 index의 증가, depth를 통해 value를 구함
            else:
                now_value = self.cal_value(state.generateSuccessor(agentIndex, action), alpha, beta, agentIndex + 1, depth)[0]
            #원래 value와 구한 value의 대소를 비교하여 minimum score을 구하는 과정을 거침
            if now_value < v:
                v = now_value
                min_actions = action
            #beta 값을 update해줌 - beta는 min의 best option
            beta = min(beta, v)
            #alpha 값과 비교하여 value가 alpha보다 작으면 pruning 과정 실행
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
