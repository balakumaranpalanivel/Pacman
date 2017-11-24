# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    """
        MY_EXPLANATION
        Answer: Decreasing the noise value to 0.01

        Increasing or decreasing the discount will not have effect on the overall
        policy of leading the agent towards "west" in the initial stages. Because
        the discount value has more effect on the intial stages owing to 
        (gamma*discount) 
        Hence I decided to reduce the noise value.
    """
    answerDiscount = 0.9
    answerNoise = 0.01
    return answerDiscount, answerNoise

def question3a():
    """
        What Have I done ?
        I have give a negative living reward so that the agent will quickly try
        to find a exit state
        I have kept a less discount value so that it will not increase the value
        for a given state and encourage living
        Noise is kept to zero so that unexpected movements are not taken. This is
        essential to make sure that the agent doesnt end up in the cliff while
        taking the risky route
    """
    answerDiscount = 0.5 
    answerNoise = 0
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    """
        What Have I done ?
        Having the same situation as question (3a) for discount and living reward
        Adding Noise increases the chances of ending on the wrong states which
        makes the agent chose a longer path (safer path) but go for the closest
        exit state
    """
    answerDiscount = 0.5
    answerNoise = 0.1
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    """
        What Have I done?
        Having the same situaion as question (3a) for discout and noise
        But encouraging the agent to live by awarding a positive living reward
    """
    answerDiscount = 0.5
    answerNoise = 0
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    """
        What Have I done?
        Having the same situation as question (3b) for discount and noise
        But encouraging the agent to live by awarding a positive living reward
    """
    answerDiscount = 0.5 
    answerNoise = 0.1
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    """
        What Have I done?
        Awarding a extremely high living reward to encourage the agent to never
        exit the board
    """
    answerDiscount = 0.5
    answerNoise = 0.0
    answerLivingReward = 1000
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    answerEpsilon = None
    answerLearningRate = None
    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
