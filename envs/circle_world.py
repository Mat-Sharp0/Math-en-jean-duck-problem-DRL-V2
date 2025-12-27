import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces
from utils.entity import Duck, Wolf


class CircleWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(
        self,
        render_mode=None,
        radius=5.0,
        duck_speed=1.0,
        wolf_speed=2.0,
        catch_radius=0.1,
        max_steps=500,
    ):
        super().__init__()

        # Parameters
        self.radius = radius
        self.duck_speed = duck_speed
        self.wolf_speed = wolf_speed
        self.catch_radius = catch_radius
        self.max_steps = max_steps

        # State
        self.steps = 0
        self.duck = Duck()
        self.wolf = Wolf(np.array([0.0, -self.radius], dtype=np.float64))

        # Spaces
        self.observation_space = spaces.Dict(
            {
                "duck": spaces.Box(
                    low=-1.0, high=1.0, shape=(2,), dtype=np.float32
                ),
                "wolf": spaces.Box(
                    low=-1.0, high=1.0, shape=(2,), dtype=np.float32
                ),
            }
        )

        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(2,), dtype=np.float32
        )

        # Rendering
        self.render_mode = render_mode
        self.window_size = 512
        self.window = None
        self.clock = None

    # =========================
    # Helpers
    # =========================

    def _get_obs(self):
        return {
            "duck": (self.duck.pos / self.radius).astype(np.float32),
            "wolf": (self.wolf.pos / self.radius).astype(np.float32),
        }

    def _get_info(self):
        return {
            "distance": float(
                np.linalg.norm(self.duck.pos - self.wolf.pos)
            )
        }

    # =========================
    # Gym API
    # =========================

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.steps = 0
        self.duck.pos = np.zeros(2, dtype=np.float32)
        self.wolf.pos = np.array([0.0, -self.radius], dtype=np.float64)

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        self.steps += 1

        terminated = False
        truncated = False
        reward = -0.001

        # Scale and clip action
        action = np.clip(action, -1.0, 1.0)
        action = action * self.duck_speed

        # Move agents
        self.duck.move(ax=action[0], ay=action[1], max_distance=self.duck_speed)
        self.wolf.wolf_move(
            self.duck.pos, np.zeros(2), self.wolf_speed
        )

        info = self._get_info()

        # Terminal conditions
        duck_dist = np.linalg.norm(self.duck.pos)
        wolf_dist = np.linalg.norm(self.duck.pos - self.wolf.pos)

        if duck_dist >= self.radius:
            terminated = True
            if wolf_dist > self.catch_radius:
                reward += 1.0
                info["result"] = "win"
            else:
                reward -= 1.0
                info["result"] = "lose"

        elif self.steps >= self.max_steps:
            truncated = True
            info["result"] = "timeout"

        observation = self._get_obs()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, truncated, info

    # =========================
    # Rendering
    # =========================

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size, self.window_size)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))

        center = self.window_size // 2
        scale = self.window_size / (2 * self.radius)

        def to_screen(pos):
            return (pos * scale + center).astype(int)

        pygame.draw.circle(canvas, (0, 0, 0), (center, center), int(self.radius * scale), 2)
        pygame.draw.circle(canvas, (255, 0, 0), to_screen(self.wolf.pos), 8)
        pygame.draw.circle(canvas, (0, 0, 255), to_screen(self.duck.pos), 8)

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return np.transpose(
                pygame.surfarray.array3d(canvas), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
