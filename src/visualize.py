from src.env.circle_world import CircleWorldEnv
from src.env.wrappers.reward import DistanceRewardWrapper
from src.env.wrappers.observation import RelativeObservationWrapper
from stable_baselines3 import PPO, TD3, SAC

def visualize(algo:str, model_path:str, episodes=5):
    if algo == 'PPO':
        model = PPO.load(model_path)
    elif algo == 'TD3':
        model = TD3.load(model_path)
    elif algo == 'SAC':
        model = SAC.load(model_path)
    else:
        raise ValueError(f"Unsupported algorithm: {algo}")


    env = CircleWorldEnv(render_mode="human")
    env = DistanceRewardWrapper(env)
    env = RelativeObservationWrapper(env)

    for i in range(episodes):
        obs, _ = env.reset()
        done = False
        print(f"Episode {i+1}/{episodes}")
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
    env.close()
