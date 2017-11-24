# -*- coding: utf-8 -*-
# mentioning utf encodig instead of ascii to mention 
#
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

        # New variable to hold the policy of each state
        self.policy = util.Counter()
        states = self.mdp.getStates()

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # New value function list
        
        """
            Formulas referenced from here
            http://artint.info/html/ArtInt_227.html
            S is the set of all states 
            A is the set of all actions 
            P is state transition function specifying P(s'|s,a) 
            R is a reward function R(s,a,s') 
        """

        """
            Computing the new value function for succesive iterations
            based on the following equation
            Vk[s] = maxa ∑s' P(s'|s,a) (R(s,a,s')+ γVk-1[s'])
            V[S] value function
        """
        new_values = util.Counter()
        for i in xrange(self.iterations):
            for state in states:
                if self.mdp.isTerminal(state):
                    new_values[state] = 0                    
                else:
                    q_value_list = []
                    feasible_actions = self.mdp.getPossibleActions(state)
                    for current_action in feasible_actions:
                        current_q_value = self.computeQValueFromValues(state, current_action)
                        q_value_list.append(current_q_value)   
                    new_values[state] = max(q_value_list)
            self.values = new_values.copy()
            
        """
            Computing the policy of each of the state based on the following
            equation
            π[s] = argmaxa ∑s' P(s'|s,a) (R(s,a,s')+ γVk[s'])
            π[S] approximately optimal policy
        """
        new_values = util.Counter()
        for state in states:
            if self.mdp.isTerminal(state):
                self.policy[state] = None
            else:
                q_value_list = []
                feasible_actions = self.mdp.getPossibleActions(state)
                for current_action in feasible_actions:
                    current_q_value = self.computeQValueFromValues(state,
                    current_action)
                    q_value_list.append(current_q_value)   
                new_values[state] = max(q_value_list)
                self.policy[state] = feasible_actions[q_value_list.index(new_values[state])]

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

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
