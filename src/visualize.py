import json, zipfile

from src.env.environment import Environment
from stable_baselines3 import PPO, TD3, SAC

def visualize(model_path:str, wolf_speed:float = 3.0, episodes:int = 1, ) -> None:
    """Visualize model"""
    with zipfile.ZipFile(model_path, "r") as zf:
        with zf.open("metadata.json") as f:
            meta = json.load(f)

    if meta['algo'] == 'PPO':
        model = PPO.load(model_path)
    elif meta['algo'] == 'TD3':
        model = TD3.load(model_path)
    elif meta['algo'] == 'SAC':
        model = SAC.load(model_path)
    else:
        raise ValueError(f"Unsupported algorithm: {meta['algo']}")


    env = Environment(
        render_mode="human",
        duck_speed=1.0,
        wolf_speed=wolf_speed,
        render_fps=30,
        reward_scale=1.0
    )

    for i in range(episodes):
        obs, _ = env.reset()
        done = False
        print(f"Episode {i+1}/{episodes}")
        
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            if done:
                print(info["result"])
            
    env.close()
