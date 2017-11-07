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
      The code below extracts some useful information from the state, like the
      remaining food (newFood) and Pacman position after moving (newPos).
      newScaredTimes holds the number of moves that each ghost will remain
      scared because of Pacman having eaten a power pellet.
      Print out these variables to see what you're getting, then combine them
      to create a masterful evaluation function.
      """
      # Useful information you can extract from a GameState (pacman.py)
      successorGameState = currentGameState.generatePacmanSuccessor(action)
      new_pacman_position = successorGameState.getPacmanPosition()

      # High score for next state if pacman is winning
      if successorGameState.isWin():
          return 999999

      # The state is more favourable if the ghost is more than 3 moves away from
      # the current position of pacman
      ghost_position = currentGameState.getGhostPosition(1)
      ghost_distance = util.manhattanDistance(ghost_position, new_pacman_position)
      if ghost_distance > 3:
        score = ghost_distance * 2
      else:
        score = 2

      # Ensuring pacman always does not go for the closest food despite nearby
      # dangers
      current_food = currentGameState.getFood()
      successor_food = successorGameState.getFood()
      closest_food = 999999
      for food in successor_food.asList():
        current_food = manhattanDistance(food, new_pacman_position)
        if current_food < closest_food:
          closest_food = current_food
      score -= 3 * closest_food

      # But to make sure the food is getting reduced. make pacman take a
      # move favourable to reduction of total number of food instead of 
      # always going for the closest food
      if (currentGameState.getNumFood() > successorGameState.getNumFood()):
          score += 100
      if action == Directions.STOP:
          score -= 3

      # # Make pacman consuder 
      # capsule_list = currentGameState.getCapsules()
      # if new_pacman_position in capsule_list:
      #     score += 150

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

    """
    @desc: Implements the Max agent value computation
    """
    def max_value(self, game_state, depth):
      
      # Terminal States return score
      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)

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

    """
    @desc: Implements the Min agent value computation
    """
    def min_value(self, game_state, depth, ghost_index):

      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)

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
        score, action = self.max_value(gameState, self.depth)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    # PACMAN
    """
    @desc:  Implements the Max agent value computation
            with alpha-beta pruning
    """
    def max_value(self, game_state, depth, alpha, beta):
      
      # Terminal States return score
      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)

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

    """
    @desc:  Implements the Min agent value computation
            with alpha-beta pruning
    """
    def min_value(self, game_state, depth, ghost_index, alpha, beta):

      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)

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
        alpha = -(float("inf"))
        beta = float("inf")
        score, action = self.max_value(gameState, self.depth, alpha, beta)
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    # PACMAN
    """
    @desc: Implements the Max agent value computation
    """
    def max_value(self, game_state, depth):
      
      # Terminal States return score
      if game_state.isWin() or game_state.isLose() or depth == 0:
        return (scoreEvaluationFunction(game_state), Directions.STOP)

      max_score = -999999
      return_action = Directions.STOP

      pacman_legal_actions = game_state.getLegalActions(0)
      for action_taken in pacman_legal_actions:
        successor_state = game_state.generateSuccessor(0, action_taken)
        current_score = self.chance_value(successor_state, depth, 1)
        if current_score >= max_score:
          max_score = current_score
          return_action  = action_taken

      return (max_score, return_action)

    """
    @desc: Implements the Chance agent value computation
    """
    def chance_value(self, game_state, depth, ghost_index):
      
      if game_state.isWin() or game_state.isLose() or depth == 0:
        return scoreEvaluationFunction(game_state)

      return_action = Directions.STOP
      number_of_agents = game_state.getNumAgents()
      chance_value = 0

      list_legal_actions = game_state.getLegalActions(ghost_index)
      for action in list_legal_actions:
        successor_state = game_state.generateSuccessor(ghost_index, action)
        if ghost_index == number_of_agents - 1:
          value, text = self.max_value(successor_state, depth-1)
          chance_value += value
        else:
          chance_value += self.chance_value(successor_state, depth, ghost_index+1)
        
      return chance_value/len(list_legal_actions)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        score, action = self.max_value(gameState, self.depth)
        return action

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

