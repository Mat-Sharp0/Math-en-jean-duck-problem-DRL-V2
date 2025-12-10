from enum import Enum

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

import utils.entity

class CircleWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, radius=5):
        self.radius = radius
        self.window_size = 512

        self.observation_space = spaces.Dict(
            {
                "duck": spaces.Box(-radius, radius, shape=(2,), dtype=np.float64),
                "wolf": spaces.Box(-radius, radius, shape=(2,), dtype=np.float64),
                "dist_border": spaces.Box(0, radius, shape=(1,), dtype=np.float64),
                "dist_wolf": spaces.Box(0, 2*radius, shape=(1,), dtype=np.float64),
            }
        )