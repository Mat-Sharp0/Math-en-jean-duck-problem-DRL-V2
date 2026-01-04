from enum import Enum

import numpy as np
from stable_baselines3 import PPO, TD3, SAC
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.noise import NormalActionNoise

from src.env.circle_world import CircleWorldEnv
from src.env.wrappers.reward import DistanceRewardWrapper
from src.env.wrappers.observation import RelativeObservationWrapper

class Algo(Enum):
    PPO = "PPO"
    TD3 = "TD3"
    SAC = "SAC"

def make_env(render_mode=None, reward_scale:float=0.02):
    env = CircleWorldEnv(render_mode=render_mode)
    env = DistanceRewardWrapper(env, scale=reward_scale)
    env = RelativeObservationWrapper(env)
    return env


def train_model(
    tensorboard_log:str,
    model_path:str,
    algo: Algo = Algo.PPO,
    n_envs: int = 8,
    total_timesteps: int = 500_000,
    learning_rate: float = 3e-4,
    gamma: float = 0.99,
    n_steps: int = 2048,
    batch_size: int = 64,
    reward_scale: float = 0.02,
    device: str = "cpu",
    run_name: str = "run1",
    render_mode=None,
):
    env = DummyVecEnv([make_env(render_mode=render_mode, reward_scale=reward_scale) for _ in range(n_envs)])
    env = VecNormalize(env, norm_obs=True, norm_reward=True)

    if algo == Algo.PPO:
        model = PPO(
            "MlpPolicy",
            env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            batch_size=batch_size,
            gamma=gamma,
            verbose=1,
            tensorboard_log=tensorboard_log,
            device=device,
        )

    elif algo == Algo.TD3:
        n_actions = env.action_space.shape[0]
        action_noise = NormalActionNoise(
            mean=np.zeros(n_actions),
            sigma=0.1 * np.ones(n_actions)
        )

        model = TD3(
            "MlpPolicy",
            env,
            learning_rate=learning_rate,
            batch_size=256,
            action_noise=action_noise,
            verbose=1,
            tensorboard_log=tensorboard_log,
            device=device,
        )

    elif algo == Algo.SAC:
        model = SAC(
            "MlpPolicy",
            env,
            learning_rate=learning_rate,
            batch_size=256,
            verbose=1,
            tensorboard_log=tensorboard_log,
            device=device,
        )

    else:
        raise ValueError(f"Unsupported algorithm: {algo}")

    model.learn(
        total_timesteps=total_timesteps,
        tb_log_name=f"{algo.value}_{run_name}"
    )

    model.save(f"{model_path}/{algo.value}_{run_name}")
