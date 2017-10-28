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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***" 
   # stack to hold the fringe
    lifo_fringe = util.Stack()
    current_state = problem.getStartState()
    
    # Add a list along with the state to store the list of actions to get to
    # the current_state
    lifo_fringe.push((current_state, []))
    visited_position = []
    
    while not lifo_fringe.isEmpty():
        current_state, action_to_state = lifo_fringe.pop()
        visited_position.append(current_state)
        # print "Current State and action: {0},{1}".format(current_state, action_to_state)
        # check if current node is the goal
        if problem.isGoalState(current_state):
            return action_to_state

        list_of_successors = problem.getSuccessors(current_state)
        # print "List of Successors: {0}".format(list_of_successors)
        # list_of_successors.reverse()
        # print "List of Successors Reverse: {0}".format(list_of_successors)
        if [] != list_of_successors:
            for item in list_of_successors:
                new_state, direction, cost = item
                if new_state not in visited_position:
                    # print "Item Being Pushed: {0},{1}".format(new_state, action_to_state + [direction])
                    lifo_fringe.push((new_state, action_to_state + [direction]))
                    # Push for every co-ordinate ?
                    #break

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Queue to hold the fringe
    lifo_fringe = util.Queue()
    current_state = problem.getStartState()
    
    # Add a list along with the state to store the list of actions to get to
    # the current_state
    lifo_fringe.push((current_state, []))
    visited_position = [current_state]
    
    while not lifo_fringe.isEmpty():
        current_state, action_to_state = lifo_fringe.pop()

        # check if current node is the goal
        if problem.isGoalState(current_state):
            return action_to_state

        list_of_successors = problem.getSuccessors(current_state)
        if [] != list_of_successors:
            for item in list_of_successors:
                new_state, direction, cost = item
                if new_state not in visited_position:
                    visited_position.append(new_state)
                    lifo_fringe.push((new_state, action_to_state + [direction]))
    return []

def uniformCostSearch(problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Priority Queue to hold the open set
    priority_queue_open = util.PriorityQueue()

    current_state = problem.getStartState()
    
    # Add the current_state to the open priority_queue
    priority_queue_open.push((current_state, 0, []), 0)
    dict_to_check_minimum = {current_state:0}
    visited_position = []
    while not priority_queue_open.isEmpty():
        current_state, cost_to_current_state, action_to_state = priority_queue_open.pop()
        visited_position.append(current_state)

        # check if current node is the goal
        if problem.isGoalState(current_state):
            return action_to_state

        list_of_successors = problem.getSuccessors(current_state)
        if [] != list_of_successors:
            for item in list_of_successors:
                new_state, direction, incremental_cost = item
                if new_state not in visited_position:
                    cost_to_new_state = incremental_cost + cost_to_current_state
                    if new_state in dict_to_check_minimum.keys():
                        if dict_to_check_minimum[new_state] > cost_to_new_state:
                            priority_queue_open.push((new_state, cost_to_new_state, action_to_state + [direction]),
                                                cost_to_new_state)
                            dict_to_check_minimum[new_state] = cost_to_new_state                        
                    else:
                        priority_queue_open.push((new_state, cost_to_new_state, action_to_state + [direction]),
                                             cost_to_new_state)
                        dict_to_check_minimum[new_state] = cost_to_new_state
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    priority_queue_open = util.PriorityQueue()
    priority_queue_open.push((problem.getStartState(), [], 0), 0)
    
    current_state, action_to_state, cost_to_current_state = priority_queue_open.pop()
    visited_position = [(current_state, 0)]
    while (not problem.isGoalState(current_state)):

        list_of_successors = problem.getSuccessors(current_state)

        for item in list_of_successors:
            new_state, direction, incremental_cost = item
            total_cost = cost_to_current_state + incremental_cost

            is_visited = False
            for i in range( len(visited_position) ):
                state_visited, cost_visted = visited_position[i]
                if (new_state == state_visited) and (total_cost >= cost_visted):
                    is_visited=True

            if (not is_visited):
                total_cost=problem.getCostOfActions(action_to_state+[direction])
                priority_queue_open.push((new_state,action_to_state+[direction],total_cost),total_cost+heuristic(new_state,problem))
                visited_position.append((new_state,total_cost))

        current_state, action_to_state, cost_to_current_state = priority_queue_open.pop()
    
    return  action_to_state

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
