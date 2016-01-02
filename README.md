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

## Develop

Open `agent.py` and implement `LearningAgent`. Follow the `TODO`s in there for further instructions.
