import yaml

import numpy as np
from stable_baselines3 import PPO, TD3, SAC
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.noise import NormalActionNoise

from src.env.circle_world import CircleWorldEnv
from src.env.wrappers.reward import DistanceRewardWrapper
from src.env.wrappers.observation import RelativeObservationWrapper


def make_env(render_mode=None, reward_scale: float = 1.0):
    env = CircleWorldEnv(render_mode=render_mode)
    env = DistanceRewardWrapper(env, scale=reward_scale)
    env = RelativeObservationWrapper(env)
    return env


def train_model(yaml_config_path: str):

    with open(yaml_config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    hp = config['hyperparameters']  # raccourci lisible

    env = DummyVecEnv([
        make_env(render_mode=config['render_mode'], reward_scale=hp.get('reward_scale', 1.0))
        for _ in range(config['training']['n_envs'])
    ])
    env = VecNormalize(env, norm_obs=True, norm_reward=True)

    if config['algo'] == 'PPO':
        model = PPO(
            config['policy'],
            env,
            learning_rate=hp['learning_rate'],
            n_steps=hp['n_steps'],
            batch_size=hp['batch_size'],
            n_epochs=hp['n_epochs'],
            gae_lambda=hp['gae_lambda'],
            clip_range=hp['clip_range'],
            ent_coef=hp['ent_coef'],
            gamma=hp['gamma'],
            verbose=config['log']['verbose'],
            tensorboard_log=config['log']['tensorboard_log'],
            device=config['device'],
        )

    elif config['algo'] == 'TD3':
        n_actions = env.action_space.shape[0]
        action_noise = NormalActionNoise(
            mean=np.zeros(n_actions),
            sigma=0.1 * np.ones(n_actions)
        )
        model = TD3(
            config['policy'],
            env,
            learning_rate=hp['learning_rate'],
            batch_size=hp.get('batch_size', 256),
            gamma=hp.get('gamma', 0.99),
            tau=hp.get('tau', 0.005),
            action_noise=action_noise,
            learning_starts=hp.get('learning_starts', 10_000),
            buffer_size=hp.get('buffer_size', 500_000),
            train_freq=hp.get('train_freq', 1),
            gradient_steps=hp.get('gradient_steps', 1),
            verbose=config['log']['verbose'],
            tensorboard_log=config['log']['tensorboard_log'],
            device=config['device'],
        )

    elif config['algo'] == 'SAC':
        model = SAC(
            config['policy'],
            env,
            learning_rate=hp['learning_rate'],
            batch_size=hp.get('batch_size', 256),
            gamma=hp.get('gamma', 0.99),
            tau=hp.get('tau', 0.005),
            ent_coef=hp.get('ent_coef', 'auto'),
            target_entropy=hp.get('target_entropy', 'auto'),
            learning_starts=hp.get('learning_starts', 10_000),
            buffer_size=hp.get('buffer_size', 500_000),
            train_freq=hp.get('train_freq', 1),
            gradient_steps=hp.get('gradient_steps', 1),
            verbose=config['log']['verbose'],
            tensorboard_log=config['log']['tensorboard_log'],
            device=config['device'],
        )

    else:
        raise ValueError(f"Unsupported algorithm: {config['algo']}")

    model.learn(
        total_timesteps=config['training']['total_timesteps'],
        tb_log_name=f"{config['algo']}_{config['run_name']}",
        progress_bar=True
    )

    model.save(f"{config['model_path']}/{config['algo']}_{config['run_name']}")