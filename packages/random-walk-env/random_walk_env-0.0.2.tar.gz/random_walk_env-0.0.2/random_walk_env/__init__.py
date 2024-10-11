from gymnasium.envs.registration import register

register(
    id="random_walk_env/RandomWalk-v0",
    entry_point="random_walk_env.envs:RandomWalkEnv",
)
