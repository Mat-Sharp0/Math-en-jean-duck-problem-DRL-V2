from stable_baselines3 import PPO, TD3, SAC
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize, VecVideoRecorder
from envs.circle_world import CircleWorldEnv
from wrappers.reward import DistanceRewardWrapper
from wrappers.observation import RelativeObservationWrapper

# --- Création d'un environnement vectorisé ---
def make_env():
    env = CircleWorldEnv(render_mode=None)
    env = DistanceRewardWrapper(env, scale=0.02)
    env = RelativeObservationWrapper(env)
    return env

vec_env = DummyVecEnv([make_env for _ in range(8)])  # 8 environnements pour PPO
vec_env = VecNormalize(vec_env, norm_obs=True, norm_reward=True)

# --- Sélection de l'algorithme ---
algo = "PPO"  # changer en "TD3" ou "SAC" si besoin

if algo == "PPO":
    model = PPO(
        "MlpPolicy",
        vec_env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        gamma=0.99,
        verbose=1,
        tensorboard_log="./tensorboard_logs/",
        device="cpu"
    )
elif algo == "TD3":
    from stable_baselines3.common.noise import NormalActionNoise
    import numpy as np
    n_actions = vec_env.action_space.shape[0]
    action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))
    model = TD3(
        "MlpPolicy",
        vec_env,
        action_noise=action_noise,
        learning_rate=1e-3,
        batch_size=256,
        verbose=1,
        tensorboard_log="./tensorboard_logs/",
        device="cuda"
    )
elif algo == "SAC":
    model = SAC(
        "MlpPolicy",
        vec_env,
        learning_rate=3e-4,
        batch_size=256,
        verbose=1,
        tensorboard_log="./tensorboard_logs/",
        device="cuda"
    )

# --- Entraînement ---
model.learn(total_timesteps=500_000, tb_log_name=f"{algo}_run1")
model.save(f"models/{algo}_circle_world")

# --- Évaluation avec rendu ---
env = CircleWorldEnv(render_mode="human")
env = DistanceRewardWrapper(env)
env = RelativeObservationWrapper(env)
obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated

env.close()
