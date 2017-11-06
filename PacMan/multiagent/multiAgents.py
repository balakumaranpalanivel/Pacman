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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print "Scores: {0}".format(scores)
        # print "Moves: {0}".format(legalMoves)

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

        The code below extracts some useful information from t  he state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # # Useful information you can extract from a GameState (pacman.py)
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
        # # print "Action: {0}".format(action)
        
        # score = successorGameState.getScore()
        # # print "Current Score: {0}".format(score)

        # newPos = successorGameState.getPacmanPosition()
        # # print "Next Position: {0}".format(newPos)

        # newFood = successorGameState.getFood()
        # # print newFood
        # posx, posy = newPos
        # isFood = newFood[posx+1][posy+1]
        # # if isFood:
        # #   print "333333333333333333333333333333333"
        # # print "Food at Position: {0}".format(isFood)

        # newGhostStates = successorGameState.getGhostStates()
        # # print "New Ghost States: {0}".format(newGhostStates)

        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print "New Scared Times: {0}".format(newScaredTimes)

        # print ""

        score = 0
        # find the number of remaining food        
        # current_food_count = 0
        # for item in current_food:
        #   current_food_count += item.count(True)
        
        # succesor_food_count = 0
        # for item in succesor_food:
        #   succesor_food_count += item.count(True)

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        current_food_count =  currentGameState.getNumFood()
        succesor_food_count = successorGameState.getNumFood()

        # number of food reduces or remains the same
        # if succesor_food_count < current_food_count:
        #   score += 1
        # elif succesor_food_count == current_food_count:
        #   score += 0.5

        # Distance to ghost is big
        new_ghost_states = successorGameState.getGhostStates()

        new_pacman_position = successorGameState.getPacmanPosition()
        new_position_distance = 0

        current_pacman_position = currentGameState.getPacmanPosition()
        current_position_distance = 0

        for ghost_state in new_ghost_states:
          ghost_position = ghost_state.getPosition()
          new_position_distance += manhattanDistance(
            ghost_position, new_pacman_position)
          current_position_distance += manhattanDistance(
            ghost_position, current_pacman_position)

        # size of the board
        if new_position_distance < 3:
          if new_position_distance < current_position_distance:
            score += -2
          elif new_position_distance == current_position_distance:
            score += 0.5
          else:
            score += 1

        current_food = currentGameState.getFood()
        successor_food = successorGameState.getFood()
        closest_food = 1000

        # find the closest food
        for i in range(0, successor_food.width):
          for j in range(0, len(successor_food[i])):
            if currentGameState.hasFood(i, j):
              current_food = manhattanDistance(new_pacman_position, (i,j))
              if current_food < closest_food:
                closest_food = current_food

        if closest_food < (new_position_distance/2) and action is not Directions.STOP:
          score += 5

        if closest_food != 0:
          score += 1/closest_food
        
        distance_to_food_list = []
        "*** YOUR CODE HERE ***"
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
    # PACMAN
    def max_value(self, game_state, depth):
      
      # Terminal States return score
      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)
      
      # print "self.depth: {0}".format(self.depth)
      # game_state.dept

      max_score = -999999
      return_action = Directions.STOP

      pacman_legal_actions = game_state.getLegalActions(0)
      for action_taken in pacman_legal_actions:
        successor_state = game_state.generateSuccessor(0, action_taken)
        return_value = self.min_value(successor_state, depth, 1)
        current_score, action_text = return_value
        if current_score >= max_score:
          max_score = current_score
          return_action  = action_taken

      return (max_score, return_action)

    def min_value(self, game_state, depth, ghost_index):

      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)

      # print "self.depth: {0}".format(self.depth)

      min_score = 999999

      return_action = Directions.STOP

      number_of_agents = game_state.getNumAgents()

      for action_taken in game_state.getLegalActions(ghost_index):
        successor_state = game_state.generateSuccessor(ghost_index, action_taken)
        
        if ghost_index == number_of_agents-1:
          return_value = self.max_value(successor_state, depth-1)
        else:
          return_value = self.min_value(successor_state, depth, ghost_index+1)
        current_score, action_text = return_value

        if current_score <= min_score:
          min_score = current_score
          return_action = action_taken

      return (min_score, return_action)

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        
        score, action = self.max_value(gameState, self.depth)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    # PACMAN
    def max_value(self, game_state, depth, alpha, beta):
      
      # Terminal States return score
      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)
      
      # print "self.depth: {0}".format(self.depth)
      # game_state.dept

      max_score = -999999
      return_action = Directions.STOP

      pacman_legal_actions = game_state.getLegalActions(0)
      for action_taken in pacman_legal_actions:
        successor_state = game_state.generateSuccessor(0, action_taken)
        return_value = self.min_value(successor_state, depth, 1, alpha, beta)
        current_score, action_text = return_value
        if current_score >= max_score:
          max_score = current_score
          return_action  = action_taken
        
        if current_score > beta:
          return (max_score, return_action)
        alpha = max(alpha, max_score)

      return (max_score, return_action)

    def min_value(self, game_state, depth, ghost_index, alpha, beta):

      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)

      # print "self.depth: {0}".format(self.depth)

      min_score = 999999

      return_action = Directions.STOP

      number_of_agents = game_state.getNumAgents()

      for action_taken in game_state.getLegalActions(ghost_index):
        successor_state = game_state.generateSuccessor(ghost_index, action_taken)
        
        if ghost_index == number_of_agents-1:
          return_value = self.max_value(successor_state, depth-1, alpha, beta)
        else:
          return_value = self.min_value(successor_state, depth, ghost_index+1, alpha, beta)
        current_score, action_text = return_value

        if current_score <= min_score:
          min_score = current_score
          return_action = action_taken

        if current_score < alpha:
          return (min_score, return_action)
        beta = min(beta, min_score)

      return (min_score, return_action)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -(float("inf"))
        beta = float("inf")
        score, action = self.max_value(gameState, self.depth, alpha, beta)
        return action

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

