# Train a smartcab how to drive
Reinforcement Learning Project for Udacity's Machine Learning Nanodegree.

## Install

This project requires Python 2.7 with the pygame library installed:

https://www.pygame.org/wiki/GettingStarted

## The Current Features

This project currentl uses two types of agent:

- The frst type of agent is what I call a random/initiated type of agent. It takes action in the direction of more reward. It also switched back to random mode when It finds that it performs bad when it is initiated mode.

- The second type of agent uses Q-learning method to learn the true values of each state and perform actions accordingly.

The following line can be used to toggle between the Qlearning agent and The normal learning agent:
```
    a = e.create_agent(QLearningAgent)  # create agent
```

## How to run the program

Make sure you are in the top-level `smartcab` directory. Then run:

```python smartcab/agent.py```

OR:

```python -m smartcab.agent```

## Task 1

### Implement a basic driving agent

Download smartcab.zip, unzip and open the template Python file agent.py (do not modify any other file). Perform the following tasks to build your agent, referring to instructions mentioned in README.md as well as inline comments in agent.py.

Also create a project report (e.g. Word or Google doc), and start addressing the questions indicated in italics below. When you have finished the project, save/download the report as a PDF and turn it in with your code.

Implement the basic driving agent, which processes the following inputs at each time step:

- Next waypoint location, relative to its current location and heading,
- Intersection state (traffic light and presence of cars), and,
- Current deadline value (time steps remaining)

And produces some random move/action `(None, 'forward', 'left', 'right')`. Don’t try to implement the correct strategy! That’s exactly what your agent is supposed to learn.

Run this agent within the simulation environment with enforce_deadline set to False (see run function in agent.py), and observe how it performs. In this mode, the agent is given unlimited time to reach the destination. The current state, action taken by your agent and reward/penalty earned are shown in the simulator.

In your report, mention what you see in the agent’s behavior. Does it eventually make it to the target location?

### Implementing the basic driving agent

I went on to create the initial driving agent with a greedy approach in mind. I felt it could do better than complete randomness. My initial go at the basic driving agent is present in `agent.py` and is called as the `LearningAgent`.

### Working of naive driving agent

It implements a naive greedy strategy and picks a random legal action to go ahead. Once it performs this action, it later checks if this action gives it a good reward or no. If it gives a bad reward, it simply performs a random action in the next move, else it performs an initiated action. In terms of a rough algorithm this is what it actually performs:

```
States :=> 'Random', 'Initiated'

Initally:
	State :=> Random
	lastAction => None
	lastReward => None

While Cab has not Reached Destination do:
	if State == Random:
		actionPerformed :=> Pick a Random Legal Action
							 from ['Forward','Left',
								Right', None]

		Perform Action and set reward variable
	else if State == Initiated:
		actionPerformed => lastAction

	# Update State
	If reward > lastReward
		State = Initiated	
	else
		State = Random

	# Set Last Action performed and last reward gained
	Set:
		lastAction :=> actionPerformed
		lastReward :=> reward

```

The algorithm works in a very naive way by finding a path that maximises the reward and follows it. In the above pseudocode, the algorithm only perfoms legal action and hence does not pick a negative reward.

### How well does it perform ? 

I ran test trials of 10 with enforced deadline and the following table represents the tabular results of each trial:

Trial #       | Result 
------------- | -------------
1             | Primary agent could not reach destination within deadline!
2 			  | Primary agent could not reach destination within deadline!
3 			  | Primary agent could not reach destination within deadline!
4 			  | Primary agent could not reach destination within deadline!
5 			  | Primary agent could not reach destination within deadline!
6 			  | Primary agent could not reach destination within deadline!
7 			  | Primary agent has reached destination!
8 			  | Primary agent could not reach destination within deadline!
9 			  | Primary agent could not reach destination within deadline!
10 			  | Primary agent could not reach destination within deadline!

As you can see, the naive agent was able to only reach the destination once out of 10 test runs.



## Task 2

### Implement Q-Learning

Implement the Q-Learning algorithm by initializing and updating a table/mapping of Q-values at each time step. Now, instead of randomly selecting an action, pick the best action available from the current state based on Q-values, and return that.

Each action generates a corresponding numeric reward or penalty (which may be zero). Your agent should take this into account when updating Q-values. Run it again, and observe the behavior.

What changes do you notice in the agent’s behavior?

Enhance the driving agent

Apply the reinforcement learning techniques you have learnt, and tweak the parameters (e.g. learning rate, discount factor, action selection method, etc.), to improve the performance of your agent. Your goal is to get it to a point so that within 100 trials, the agent is able to learn a feasible policy - i.e. reach the destination within the allotted time, with net reward remaining positive.

Report what changes you made to your basic implementation of Q-Learning to achieve the final version of the agent. How well does it perform?

Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties?


