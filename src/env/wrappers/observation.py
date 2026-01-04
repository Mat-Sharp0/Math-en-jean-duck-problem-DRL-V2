import gymnasium as gym
import numpy as np
from gymnasium import spaces

class RelativeObservationWrapper(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, shape=(4,), dtype=np.float32
        )

    def observation(self, obs):
        duck = obs["duck"]
        wolf = obs["wolf"]
        return np.concatenate([duck, wolf - duck]).astype(np.float32)
