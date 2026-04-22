import yaml
import json, uuid, zipfile
from datetime import datetime
from pathlib import Path

from src.utils.paths import TENSORBOARD_DIR, MODELS_DIR

import numpy as np

from stable_baselines3 import PPO, TD3, SAC
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.noise import NormalActionNoise

from src.env.environment import Environment


def make_env(
        render_mode: str = None,
        duck_speed: float = 1.0,
        wolf_speed: float = 2.0,
        reward_scale: float = 1.0
        ) -> Environment:
    
    def _init() -> Environment:
        env = Environment(
            render_mode=render_mode,
            duck_speed=duck_speed,
            wolf_speed=wolf_speed,
            reward_scale=reward_scale
        )
        return env
    return _init


def train_model(yaml_config_path: Path) -> Path:
    """
    Train AI using config file
    
    :param yaml_config_path: The config file path
    :return: The trained model path
    """

    with open(yaml_config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    hp = config['hyperparameters']

    env = DummyVecEnv([
        make_env(render_mode=config['render_mode'], duck_speed=config['env']['duck_speed'], wolf_speed=config['env']['wolf_speed'], reward_scale=hp.get('reward_scale', 1.0))
        for _ in range(config['training']['n_envs'])
    ])
    env = VecNormalize(env, norm_obs=True, norm_reward=False)

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
            tensorboard_log=TENSORBOARD_DIR,
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
            tensorboard_log=TENSORBOARD_DIR,
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
            tensorboard_log=TENSORBOARD_DIR,
            device=config['device'],
        )

    else:
        raise ValueError(f"Unsupported algorithm: {config['algo']}")

    model.learn(
        total_timesteps=config['training']['total_timesteps'],
        tb_log_name=config['meta']['run_name'],
        progress_bar=True
    )

    path = MODELS_DIR / config['meta']['run_name']

    model.save(path)

    model_path = Path(f"{path}.zip")

    meta = {
    "model_name": config['meta']['run_name'],
    "version": config['meta']['version'],
    "run_id": str(uuid.uuid4()),
    "date": datetime.now().isoformat(),
    "algo": config['algo']
    }

    with zipfile.ZipFile(model_path, "a") as zf:
        zf.writestr("metadata.json", json.dumps(meta, indent=2))

    return model_path