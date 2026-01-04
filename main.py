import os
# import warnings

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# warnings.filterwarnings("ignore")

# import tensorflow as tf
# tf.get_logger().setLevel("ERROR")

from rich.logging import RichHandler
import logging
from rich.prompt import Prompt

from src.train import train_model,Algo
from src.visualize import visualize


terminal_width = os.get_terminal_size().columns

print("-" * terminal_width)
print("Duck AI")
print("-" * terminal_width)
print("By HIOLLE Mateo")
print("License: MIT")
print("Version: 0.1.0")

print("\nChoose an option:")
print("1. Train\n2. Visualize\n3. Files\n4. Close")

choice = Prompt.ask(choices=["1", "2", "3", "4"])

if choice == "1":
    train_model("logs\tensorboard","models\saved_model", Algo.PPO, device="cuda",)
