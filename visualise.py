from envs.circle_world import CircleWorldEnv
from wrappers.reward import DistanceRewardWrapper
from wrappers.observation import RelativeObservationWrapper
from stable_baselines3 import PPO  # ou TD3, SAC selon ton modèle

# ⚡ Charger le modèle
model = PPO.load("models\PPO_circle_world.zip")  # change le nom si nécessaire

# ⚡ Créer un env pour visualisation (1 seul env)
env = CircleWorldEnv(render_mode="human")
env = DistanceRewardWrapper(env)
env = RelativeObservationWrapper(env)

# ⚡ Nombre d'épisodes à visualiser
n_episodes = 5

for ep in range(n_episodes):
    obs, _ = env.reset()
    done = False
    print(f"Episode {ep+1}/{n_episodes}")
    
    while not done:
        # deterministic=True pour policy stable
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

env.close()
