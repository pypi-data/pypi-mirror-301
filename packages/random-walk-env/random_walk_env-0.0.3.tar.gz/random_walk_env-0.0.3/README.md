## Random Walk
This environment reflects the Markov Reward Process (MRP) defined in Example 6.2 Random Walk of the book Reinforcement Learning An Introduction (2nd Ed) by Richard S. Sutton and 
Andrew G. Barto.  
The Random Walk Environment is a custom Gymnasium environment that simulates a simple random walk process. The agent starts in a predefined state and moves randomly to adjacent states (left or right) at each timestep. The states are arranged in a row, with terminal states at both ends. The rightmost terminal state rewards the agent with +1, while all other transitions have a reward of 0. The environment is ideal for experiments in reinforcement learning or Markov Reward Processes (MRPs), focusing on stochastic state transitions without actions.

## Installation
```
pip install random-walk-env
```

## Use with gymnasium

```{shell}
import random_walk_env
import gymnasium as gym

env = gym.make('random_walk_env/RandomWalk-v0')
```

