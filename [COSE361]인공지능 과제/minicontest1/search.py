# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # "*** YOUR CODE HERE ***"
    moveque = util.Stack()      #moveque는 expanded되는 node와 함께 path, direction 등을 담는 stack이나 queue로 설정했다. 이는 search method가 달라지게 되면 형태가 달라질 것이다. 현재는 DFS라 depth를 중요시하기 때문에 한 방향으로만 push와 pop이 가능한 stack을 이용했다.
    moveque.push( (problem.getStartState(), [], []) )   #(좌표, direction list, path(좌표들로 구성된 list)) 순으로 push할 예정이다.
    while not moveque.isEmpty():    #moveque가 비어있지 않을 경우에만 성립
        previous = moveque.pop()    #previous는 moveque의 가장 위에 존재하는 상태로, 바로 전에 방문한 상태라 하여 previous라 칭했다.
        if problem.isGoalState(previous[0]) == True:    #previous가 goal일 때
            return path     #3번째 path를 return한다.
        successors = problem.getSuccessors(previous[0])     #다음으로 방문할 node들을 successor이라 칭했고, 이는 바로 전 node에서 비롯되므로 previous[0]를 써줬다.
        for i in successors:
            if not i[0] in previous[2]:     #다음으로 방문할 노드 중에 전에 방문했던 노드가 있으면 안되므로, 전에 방문했던 노드를 제외한 다음 방문 노드에 한해서 식을 진행하고자 path에 포함되지 않는 successor만 골라냈다.
                moveque.push((i[0], previous[1] + [i[1]], previous[2] + [previous[0]]))     #차례로 successor의 노드, 다음 direction을 추가한 direction list, 전 노드를 추가한 path list가 있다.
                path = previous[1] + [i[1]]     #총 path를 구하기 위해 path라는 변수를 하나 추가해서 따로 설정해두었다.


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    moveque = util.Queue()  #이번에는 전과 다르게 push와 pop되는 요소의 방향이 정 반대인 queue를 사용했다. depth보단 breadth를 우선시하기 위한 구조를 선택했다.
    moveque.push( (problem.getStartState(), [], []) )   #위와 동일한 요소를 push한다.
    visited = []    #이번엔 탐색했던 노드를 제외하기 위해 visited라는 요소를 따로 만들어줬다.
    while not moveque.isEmpty():
        previous = moveque.pop()
        if not previous[0] in visited:  #탐색했던 노드에 전의 node가 없으면 추가해주는 방식을 이용했다. 탐색하지 않은 노드에 한해서 식을 진행하기 위해 DFS의 식을 if문 안에 넣어줬다.
            visited.append(previous[0])
            if problem.isGoalState(previous[0]) == True:
                return previous[1]  #path를 return해주는 것이다.
            successors = problem.getSuccessors(previous[0])
            for i in successors: 
                if not i[0] in previous[2]:
                    moveque.push((i[0], previous[1] + [i[1]], previous[2] + [previous[0]]))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    moveque = util.PriorityQueue()  #cost라는 개념이 들어갔기 때문에, cost가 적은 것부터 반환해주는 priorityqueue를 이용했다.
    moveque.push( (problem.getStartState(), [], 0),0)   #기존 요소들에 마지막에 path 대신 cost를 넣어줬고, 괄호 밖에 또 cost를 넣어서 cost가 작은 것부터 반환시키기 위해 이런 구조를 짜봤다.
    visited = []
    while not moveque.isEmpty():
        previous = moveque.pop()
        if not previous[0] in visited:
            visited.append(previous[0])
            if problem.isGoalState(previous[0]) == True:
                return previous[1]
            successors = problem.getSuccessors(previous[0])
            for i in successors: 
                moveque.push((i[0], previous[1] + [i[1]], previous[2] + i[2]),previous[2]+i[2])     #역시 cost도 넣어줘야 하기 때문에 괄호 마지막과 바깥에 cost 정보를 넣어줌으로 인해 cost가 작은 것부터 pop 받게 된다.
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    moveque = util.PriorityQueue()  #역시 동일하게 priorityqueue가 이용된다.
    moveque.push( (problem.getStartState(), [], 0),heuristic(problem.getStartState(), problem))     #heuristic이 이용되기 시작하여 f 값이 작은 순서대로 탐색해야 하기 때문에 마지막 cost 부분에 heuristic을 이용
    visited = []
    while not moveque.isEmpty():
        previous = moveque.pop()
        if not previous[0] in visited:
            visited.append(previous[0])
            if problem.isGoalState(previous[0]) == True:
                return previous[1]
            successors = problem.getSuccessors(previous[0])
            for i in successors: 
                moveque.push((i[0], previous[1] + [i[1]], previous[2] + i[2]),previous[2]+i[2]+heuristic(i[0], problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
