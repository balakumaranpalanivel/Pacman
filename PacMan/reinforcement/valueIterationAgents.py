# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.policy = util.Counter()
        states = self.mdp.getStates()
        
        # for state in states:
        #     self.values[state] = 0

        # http://artint.info/html/ArtInt_227.html
        #print "States: {0}".format(states)
        #print "Values: {0}".format(self.values)
        #print "Discount: {0}".format(self.discount)

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # New value function list
        new_values = util.Counter()
        new_policy = util.Counter()
        for i in xrange(self.iterations):
            for state in states:
                if self.mdp.isTerminal(state):
                    new_values[state] = 0
                    new_policy[state] = None
                else:
                    q_value_list = []
                    feasible_actions = self.mdp.getPossibleActions(state)
                    for current_action in feasible_actions:
                        current_q_value = self.computeQValueFromValues(state, current_action)
                        q_value_list.append(current_q_value)   
                    new_values[state] = max(q_value_list)
                    new_policy[state] = feasible_actions[q_value_list.index(new_values[state])]
            self.values = new_values.copy()

        for state in states:
            if self.mdp.isTerminal(state):
                new_policy[state] = None
            else:
                q_value_list = []
                feasible_actions = self.mdp.getPossibleActions(state)
                for current_action in feasible_actions:
                    current_q_value = self.computeQValueFromValues(state,
                    current_action)
                    q_value_list.append(current_q_value)   
                new_values[state] = max(q_value_list)
                new_policy[state] = feasible_actions[q_value_list.index(new_values[state])]
        self.policy = new_policy.copy()

        print "Values: {0}".format(self.values)
        print "Policy: {0}".format(self.policy)

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0
        transition_funcion = self.mdp.getTransitionStatesAndProbs(state, action)
        for transition in transition_funcion:
            next_state = transition[0]
            probablity = transition[1]
            reward = self.mdp.getReward(state, action, next_state)
            discount = self.discount
            previous_value = self.values[next_state]
            q_value += probablity * (reward + (discount*previous_value))
        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        return self.policy[state]

        if self.mdp.isTerminal(state):
            return None
        else:
            action_dict = util.Counter()
            bestval = -99999999999
            bestaction = 0
            all_actions = self.mdp.getPossibleActions(state)
            for action in all_actions:

                transitions = self.mdp.getTransitionStatesAndProbs(state, action)
                value = 0
                for transition in transitions:
                    value += transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount * self.values[transition[0]])
                if value > bestval:
                    bestaction = action
                    bestval = value
            print ("-------")
            print ("Policy: {0}".format(self.policy[state]))
            print ("Best Action: {0}".format(bestaction))
            print ("-------")
            return bestaction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
