import gymnasium as gym
from gymnasium.spaces import Discrete
import random

class RandomWalkEnv(gym.Env):
    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(self, num_states=5, start_state=2):
        """
        The Random Walk Environment is a custom Gymnasium environment that simulates a simple random walk process.
        The agent starts in a predefined state and moves randomly to adjacent states (left or right) at each timestep.
        The states are arranged in a row, with terminal states at both ends.
        The rightmost terminal state rewards the agent with +1, while all other transitions have a reward of 0.
        The environment is ideal for experiments in reinforcement learning or Markov Reward Processes (MRPs), focusing on stochastic state transitions without actions.
        """

        # Set the number of states and the starting state
        self.num_states = num_states
        self.start_state = start_state

        # Action space: move left (0) or right (1)
        self.action_space = Discrete(2)  # 0: left, 1: right

        # Observation space: state is represented as a single integer (state index)
        self.observation_space = Discrete(num_states)

        # Set the current state to the start state
        self.state = self.start_state
        self.state_letters = [chr(65 + i) for i in range(self.num_states)]  # A, B, C, D, E


    def step(self, action):
        # Perform the random walk step (ignoring action, random choice between left/right)
        direction = random.choice([-1, 1])  # -1 for left, +1 for right
        self.state += direction

        # Check if we've reached the terminal state
        if self.state < 0:
            done = True
            reward = 0  # Left terminal state, no reward
            self.state = 0  # Resetting to minimum valid state for observation
        elif self.state >= self.num_states:
            done = True
            reward = 1  # Right terminal state, reward of +1
            self.state = (
                self.num_states - 1
            )  # Resetting to max valid state for observation
        else:
            done = False
            reward = 0  # All other states, no reward

        observation = self.state_letters[self.state]

        return observation, reward, done, False, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Reset to the start state
        self.state = self.start_state
        observation = self.state_letters[self.state]
        
        return observation, {}

    def render(self):
        # Simple rendering: Print the state as a letter corresponding to its position
        state_str = "".join(self.state_letters)
        current_pos = max(0, min(self.state, self.num_states - 1))

        # Adding bold formatting and brackets around the current state
        display_str = (
            state_str[:current_pos]
            + "\033[1m["
            + self.state_letters[current_pos]
            + "]\033[0m"
            + state_str[current_pos + 1 :]
        )
        print(display_str)
