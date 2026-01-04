import gymnasium as gym

class DistanceRewardWrapper(gym.Wrapper):
    def __init__(self, env, scale=0.02):
        super().__init__(env)
        self.scale = scale

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)

        distance = info.get("distance", 0.0)
        reward += self.scale * distance

        return obs, reward, terminated, truncated, info
