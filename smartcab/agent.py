import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import math
from collections import namedtuple
import pprint

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.previous_reward = 0
        self.previous_action = None

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.previous_reward = 0
        self.previous_action = None
        self.state = None

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        ## currently using two states called random and initiated
        if(self.state == None):
            self.state = 'Random'
        #print 'environment state:'
        # {'light': 'green', 'oncoming': None, 'right': None, 'left': None}
        current_env_state = self.env.sense(self)
        action = None

        possible_actions = []
        if(current_env_state['light'] == 'red'):
            if(current_env_state['oncoming'] != 'left' and current_env_state['left'] != 'forward'):
                possible_actions = ['right']
        else:
            # traffic ligh is gree and now check for oncoming
            #if no oncoming 
            if(current_env_state['oncoming'] == 'forward'):
                possible_actions = [ 'forward','right']
            else:
                possible_actions = ['right','forward']
        
        # TODO: Select action according to your policy
        if possible_actions != [] and self.state == 'Random':
            action_int =  random.randint(0,len(possible_actions)-1)
            action = possible_actions[action_int]
        elif possible_actions != [] and self.state == 'Initiated':
            action = self.previous_action
            


        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward

        if(action != None):
            if(reward > self.previous_reward):
                self.state = 'Initiated'
                self.previous_action = action
                self.previous_reward = reward
            else:
                self.state = 'Random'
                self.previous_action = action
                self.previous_reward = reward

        
        

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

class QLearningAgent(Agent):
    """An agent that learns to drive in the smartcab world using Q learning"""

    def __init__(self, env):
        super(QLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        ##initialize q table here
        self.qDict = dict()
        self.alpha    = 0.1
        self.epsilon  = 0.5 ##initial probability of flipping the coin
        self.gamma    = 0.9
        self.discount = self.gamma
        self.previous_state = None
        self.state = None
        self.previous_action = None
        self.deadline = self.env.get_deadline(self)

    def flipCoin(self, p ):
        r = random.random()
        return r < p

    def setEpsilon(self):
        if self.getCurrentDeadline() < 10:
            self.epsilon = 0.05

    def getCurrentDeadline(self):
        return self.env.get_deadline(self)

    def reset(self, destination=None):
        """
        resets the current values of the agent
        """
        self.planner.route_to(destination)
        self.previous_state = None
        self.state = None
        self.previous_action = None
        self.epsilon = 0.5

    def getLegalActions(self, state):
        """
        returns the legal action from the current state
        """
        current_env_state = self.env.sense(self)
        possible_actions = []
        if(current_env_state['light'] == 'red'):
            if(current_env_state['oncoming'] != 'left' and current_env_state['left'] != 'forward'):
                possible_actions = ['right', None]
        else:
                # traffic ligh is gree and now check for oncoming
                #if no oncoming 
            if(current_env_state['oncoming'] == 'forward'):
                possible_actions = [ 'forward','right']
            else:
                possible_actions = ['right','forward','left']

        return possible_actions

    ##gets the q value for a particulat state and action
    def getQValue(self, state, action):
        """
        input: (state,action)
        output: Q value for the (state,action)

        returns 0 if the value is not present in the dictionary.
        """
        return self.qDict.get((state, action), 0)  ##return the value from the qDict, default to 0 if the key isnt in the dict

    def getValue(self, state):
        """
         Returns max_action Q(state,action)

         where the max is over legal actions.  Note that if
         there are no legal actions, which is the case at the
         terminal state, you should return a value of 0.0.
        """
        legalActions = self.getLegalActions(state) 
        bestQValue = - 999999999
        ## If there are no legal actions simply return 0
        if not legalActions:
            return 0.0
        else:
            #search all possible actions
            for action in legalActions:
                #for each action check if the q value for the action is greater than minus infinity
                if(self.getQValue(state, action) > bestQValue):
                    bestQValue = self.getQValue(state, action)

            return bestQValue

    def getPolicy(self, state):
        """
        Compute the best action to take in a state.

        input: state
        output: best possible action(policy maps states to action)

        Working:
        From all the legal actions, return the action that has the bestQvalue.
        if two actions are tied, flip a coin and choose randomly between the two.

        """
        legalActions = self.getLegalActions(state)  
        bestAction = None
        bestQValue = - 999999999
        for action in legalActions:
            if(self.getQValue(state, action) > bestQValue):
                bestQValue = self.getQValue(state, action)
                bestAction = action
            if(self.getQValue(state, action) == bestQValue):
                if(self.flipCoin(.5)):
                    bestQValue = self.getQValue(state, action)
                    bestAction = action
        return bestAction

    def makeState(self, state):
        """
        This function makes a state and returns 

        input: State
        ouput: Named State tuple

        This is useful for creating the q dictionary.
        """
        State = namedtuple("State", ["light","oncoming","right","left"])
        return State(light = state['light'],oncoming = state['oncoming'],
                            right = state['right'], left = state['left'])

    def update(self, t):
        """
        This is the overridden mehtod that basically peforms the necessary update
        """
        
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        self.setEpsilon()

        ## this is my current state
        self.state = self.makeState(self.env.sense(self))

        ##get the current best action based on q table
        action = self.getAction(self.state)

        ##perform the action and now get the reward
        reward = self.env.act(self, action)

        ## in case of initial configuration don't update the q table, else update q table
        if self.previous_state!= None:
            self.updateQTable(self.previous_state,self.previous_action,self.state,reward)

        # store the previous action and state so that we can update the q table on the next iteration
        self.previous_action = action
        self.previous_state = self.state
        
        # pretty print q table (optional)
        # pprint.pprint(self.qDict)
        print "QLearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


    def getAction(self, state):
        """
        Compute the action to take in the current state. 

        Working:
        epsilon of the time, choose a random action from all legal actions,
        else choose the action given by the policy

        TODO:
        implement a dealine specific epsilon. Exploit when time limit is reached
        """
    # Pick Action
        legalActions = self.getLegalActions(state)  
        action = None
        print legalActions
        if (self.flipCoin(self.epsilon)):
            print "random choice"
            action = random.choice(legalActions)
        else:
            print "policy choice"
            action = self.getPolicy(state)
        return action

    def updateQTable(self, state, action, nextState, reward):
        """
         The parent class calls this to observe a
         state = action => nextState and reward transition.
         You should do your Q-Value update here
     
         NOTE: You should never call this function,
         it will be called on your behalf
        """
    
        if((state, action) not in self.qDict): ##if the (state, action) tuple is not in the dictionary, set the tuple's value to 0 within the dict
            self.qDict[(state, action)] = 0
        self.qDict[(state, action)] = self.qDict[(state, action)] + self.alpha*(reward + self.discount*self.getValue(nextState) - self.qDict[(state, action)]) ##set the previous state's qValue to itself plus alpha*(reward + gamma*value of next state - old q value)

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(QLearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
