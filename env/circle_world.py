from enum import Enum

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

from utils.entity_lite import EntityLite

class CircleWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, radius=5, duck_speed=1, wolf_speed=2):
        self.radius = radius
        self.window_size = 512
        self.duck_speed = duck_speed
        self.wolf_speed = wolf_speed

        self.observation_space = spaces.Dict(
            {
                "duck": spaces.Box(-radius, radius, shape=(2,), dtype=np.float64),
                "wolf": spaces.Box(-radius, radius, shape=(2,), dtype=np.float64),
            }
        )

        self.duck = entity_lite.EntityLite()
        self.wolf = EntityLite()

        self.action_space = spaces.Box(
            low = -self.duck_speed,
            high = self.duck_speed,
            shape = (2,),
            dtype=np.float64
        )
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def _get_obs(self):
        return {
                "duck": self.duck.pos,
                "wolf": self.wolf.pos,
            }
    
    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self.duck.pos - self.wolf.pos, ord=1
            )
        }
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.duck.pos = np.array([0.0, 0.0], dtype=np.float64)
        self.wolf.pos = np.array([0.0, 0.0], dtype=np.float64)
        self.wolf.set_direction = 0.0

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        ax, ay = action

        self.duck.move(ax=ax, ay=ay, max_distance=self.duck_speed)
        self.wolf.wolf_move(self.duck.pos, np.array([0,0]), self.radius, self.wolf_speed)


        

        