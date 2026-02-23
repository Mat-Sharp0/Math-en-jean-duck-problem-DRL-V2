import os

from rich.logging import RichHandler
import logging
from rich.prompt import Prompt

from src.train import train_model
from src.visualize import visualize


terminal_width = os.get_terminal_size().columns

print("-" * terminal_width)
print("Duck AI")
print("-" * terminal_width)
print("By HIOLLE Mateo")
print("License: MIT")
print("Version: 0.1.0")

print("\nChoose an option:")
print("1. Train\n2. Visualize\n3. Close")

choice = Prompt.ask(choices=["1", "2", "3"])

if choice == "1":
    train_config=input("Config file relative path (default: config.yaml):\n")
    if train_config == "":
        train_model('config.yaml')
    else:
        train_model(input)
elif choice == "2":
    while True:
        algo=input("Algo (PPO, TD3, SAC):\n")
        if algo != "":
            break
    
    while True:
        model_path=input("Model relative path:\n")
        if algo != "":
            break
    episodes=int(input("Episodes (default: 5):\n"))

    visualize(algo,model_path,episodes)
elif choice == "3":
    exit(0)