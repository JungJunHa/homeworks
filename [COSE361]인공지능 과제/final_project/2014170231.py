# baselineTeam.py
# ---------------
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


# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions, Actions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.
  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    self.atefood = 0
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    # gameState를 기반으로 다음에 올 state를 구한다.
    nextState = self.getSuccessor(gameState, random.choice(bestActions)) 
    Successorstate = nextState.getAgentState(self.index)
    foodLeft = len(self.getFood(gameState).asList())

    # 만약 여기 successor이 팩맨이 아니라면, 집으로 무사히 귀환을 했거나 죽었다는 말이 된다.
    if not Successorstate.isPacman:
      #이렇게 죽었거나 귀환했으면, 머금고 있던 food(atefood)를 초기화해준다.
      self.atefood = 0   

    # 여기서 atefood를 업데이트 시켜줄 때, 처음 food의 갯수에서 나중에 남은 food의 갯수를 빼서 먹었던 food의 갯수를 구한다.
    eatenfood = len(self.getFood(gameState).asList()) - len(self.getFood(nextState).asList())
    self.atefood += eatenfood

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist

      return bestAction

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveReflexAgent(DummyAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    features['successorScore'] = -len(foodList)#self.getScore(successor)

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]

    # Compute distance to the nearest food

    myPos = successor.getAgentState(self.index).getPosition()
    features['ClosestFood'] = min([self.getMazeDistance(myPos, food) for food in foodList])

    #상대편을 돌아다니는 pacman agent와 상대(ghost) 사이의 거리들을 구하기 위해 거리에 관련된 list를 만든다.
    all_ghost_distance = []
    if len(ghosts) > 0:
      for ghost in ghosts:
        all_ghost_distance.append(self.getMazeDistance(myPos, ghost.getPosition()))

    # ghost가 존재할 경우
    for ghost in ghosts:
      if ghost.scaredTimer == 0 and len(ghosts) > 0:
        # 가장 가까운 ghost와의 distance를 feature에 추가한다.
        features['ghostDistance'] = min(all_ghost_distance)
        #만약 이 거리가 너무 멀다면, 영향이 없다 생각하고 0으로 설정해준다.
        if features['ghostDistance'] > 3:
          features['ghostDistance'] = 0
      #ghost가 없을 경우
      elif ghost.scaredTimer == 0 and len(ghosts) == 0:
        features['ghostDistance'] = 0

    # 최대한 안전하게 플레이하는 방향으로, 1개 이상 먹었을 경우 집으로 돌아갈 수 있게 집까지의 거리 gobackhome을 인수로 추가해준다.
    if self.atefood >= 1:
      features['gobackhome'] = min([self.getMazeDistance(myPos, self.start)])

    # 또한 상대가 우리 진영에 있으면 먹이를 먹는 것보다 다시 home으로 돌아와서 defense를 하는 쪽으로 행동하게 만든다.
    if invaders:
      features['invaderDistance'] = min([self.getMazeDistance(myPos, a.getPosition()) for a in invaders])
    
    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'ClosestFood': -1, 'ghostDistance': -10, 'gobackhome': -10, 'stop': -100,'invaderDistance':-10, 'reverse': -2}

class DefensiveReflexAgent(DummyAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)

    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    # ghost가 존재할 경우
    if len(ghosts) > 0:
      #invader이 0이라는 소리는 상대가 아직 내 영역에 들어오지 않았다는 것이다.
      #그러므로 상대가 혹시 내 영역으로 들어올 것을 예방하여 ghost와 가까운 곳으로 이동해서 기다리게 만든다.
      if len(invaders) == 0:
        features['ghostDistance'] = min([self.getMazeDistance(myPos, a.getPosition()) for a in ghosts])
      #그러나, invader이 존재한다면 상대가 내 영역에 들어왔다는 소리가 되므로, ghostDistance는 0으로 맞추고 invader에 집중한다.
      else:
        features['ghostDistance'] = 0

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'ghostDistance': -10, 'stop': -100, 'reverse': -2}
