import yaml

import numpy as np
from stable_baselines3 import PPO, TD3, SAC
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.noise import NormalActionNoise

from src.env.circle_world import CircleWorldEnv
from src.env.wrappers.reward import DistanceRewardWrapper
from src.env.wrappers.observation import RelativeObservationWrapper

def make_env(render_mode=None, reward_scale:float=0.02):
    env = CircleWorldEnv(render_mode=render_mode)
    env = DistanceRewardWrapper(env, scale=reward_scale)
    env = RelativeObservationWrapper(env)
    return env


def train_model(yaml_config_path:str):
    
    with open(yaml_config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    env = DummyVecEnv([make_env(render_mode=config['render_mode'], reward_scale=config['hyperparameters']['reward_scale']) for _ in range(config['training']['n_envs'])])
    env = VecNormalize(env, norm_obs=True, norm_reward=True)


    if config['algo'] == 'PPO':
        model = PPO(
            config['policy'],
            env,
            learning_rate=config['hyperparameters']['learning_rate'],
            n_steps=config['hyperparameters']['n_steps'],
            batch_size=config['hyperparameters']['batch_size'],
            n_epochs=config['hyperparameters']['n_epochs'],
            gae_lambda=config['hyperparameters']['gae_lambda'],
            clip_range=config['hyperparameters']['clip_range'],
            ent_coef=config['hyperparameters']['ent_coef'],
            gamma=config['hyperparameters']['gamma'],
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
            learning_rate=config['hyperparameters']['learning_rate'],
            batch_size=256,
            action_noise=action_noise,
            verbose=1,
            tensorboard_log=config['log']['tensorboard_log'],
            device=config['device'],
        )


    elif config['algo'] == 'SAC':
        model = SAC(
            config['policy'],
            env,
            learning_rate=config['hyperparameters']['learning_rate'],
            batch_size=256,
            verbose=1,
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
