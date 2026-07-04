import os
from pathlib import Path
import sys

from src.utils.paths import init_content_dirs, CONTENT_DIR, CONFIG_DIR, MODELS_DIR, DEFAULT_CONFIG_DIR, LOGS_DIR, TENSORBOARD_DIR
from src.utils.file_function import open_folder, open_file, creat_config, clear_dir

import tkinter as tk
from tkinter import filedialog

import webbrowser
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm

from src.train import train_model
from src.visualize import visualize

from src.utils.updater import check_for_update
from src.utils.app_info import APP_NAME, __version__, AUTHOR, GITHUB_URL

def main():
    #region Init
    init_content_dirs()

    console = Console(highlight=False)

    terminal_width = console.width

    console.print("-" * terminal_width)
    console.print(APP_NAME)
    console.print("-" * terminal_width)
    console.print(f"By {AUTHOR}")
    console.print("License: MIT")
    console.print(f"Version: v{__version__}")

    if getattr(sys, 'frozen', False):
        check_for_update(console)
    #endregion

    while True:

        choice = Prompt.ask(prompt="\nChoose an option:\n1. Train\n2. Visualize\n3. Manage file\n4. Documentation\n5. Close\n",
                            console=console,
                            choices=["1", "2", "3", "4", "5"])

        #region Work
        if choice == "1":
            root = tk.Tk()
            root.withdraw()

            config = filedialog.askopenfilename(
                title="Choose config file",
                initialdir=CONFIG_DIR,
                filetypes=[
                    ("YAML file", "*.yaml *.yml"),
                    ("All file", "*.*")
                ]
            )
            root.destroy()

            if not config:
                console.print ("No config file selected")
            else:
                load_model_path = None
                choice = Prompt.ask(prompt="1. Training from scratch\n2. Continue training from existing model (Curriculum Learning)\n", console=console, choices=["1", "2"])
                if choice == "2":
                    root = tk.Tk()
                    root.withdraw()
                    selected_model = filedialog.askopenfilename(
                        title="Choose model checkpoint",
                        initialdir=MODELS_DIR,
                        filetypes=[
                            ("ZIP file", "*.zip"),
                            ("All file", "*.*")
                        ]
                    )
                    root.destroy()
                    
                    if selected_model:
                        load_model_path = Path(selected_model)
                    else:
                        console.print("No model selected, training will start from scratch.")

                try:
                    train_model(Path(config), load_model_path)
                except OSError as err:
                    console.print("OS error:", err)
                except ValueError:
                    console.print("Could not convert data to an integer.")
                except Exception as err:
                    console.print(f"Unexpected {err=}, {type(err)=}")
                    raise

        elif choice == "2":
            root = tk.Tk()
            root.withdraw()

            model = filedialog.askopenfilename(
                title="Choose model file",
                initialdir=MODELS_DIR,
                filetypes=[
                    ("ZIP file", "*.zip"),
                    ("All file", "*.*")
                ]
            )
            root.destroy()

            if not model:
                console.print("No model file selected")
            else:
                wolf_speed = FloatPrompt.ask(prompt="Wolf speed", console=console)
                episodes = IntPrompt.ask(prompt="Episodes", console=console)
                visualize(console=console, model_path=Path(model), wolf_speed=wolf_speed, episodes=episodes)
        #endregion

        #region File Managment
        elif choice == "3":
            while True:
                choice = Prompt.ask(prompt="1. Open content folder\n2. New config file\n3. Clear file\n4. Go Back\n", console=console, choices=["1", "2", "3", "4"])
                
                if choice == "1":
                    open_folder(CONTENT_DIR)
                    continue


                #region Makefile
                elif choice == "2":
                    choice = Prompt.ask(prompt="1. PPO\n2. TD3\n3. SAC\n4. Go Back\n", console=console, choices=["1", "2", "3", "4"])

                    if choice == "1":
                        new_config = creat_config(console=console, template_path=(DEFAULT_CONFIG_DIR / "default_config_ppo.yaml"))
                        console.print(f"Config file create: {new_config}")
                        open_file(new_config)
                            
                    elif choice == "2":
                        new_config = creat_config(console=console, template_path=(DEFAULT_CONFIG_DIR / "default_config_td3.yaml"))
                        console.print(f"Config file create: {new_config}")
                        open_file(new_config)

                    elif choice == "3":
                        new_config = creat_config(console=console, template_path=(DEFAULT_CONFIG_DIR / "default_config_sac.yaml"))
                        console.print(f"Config file create: {new_config}")
                        open_file(new_config)
                    continue
                #endregion



                #region Clearfile
                elif choice == "3":
                    choice = Prompt.ask(prompt="1. Clear logs\n2. Clear config files\n3. Clear models\n4. Clear all\n5. Go Back\n",
                                        console=console,
                                        choices=["1", "2", "3", "4", "5"])
                    
                    if choice == "1":
                        if Confirm.ask(prompt="Are you sure you want to delete all the logs?\nOnce you delete file, there is no going back. Please be certain.",
                                    console=console):
                            clear_dir(LOGS_DIR, {TENSORBOARD_DIR.name})
                            clear_dir(TENSORBOARD_DIR)
                            init_content_dirs()
                            console.print("Logs clear")
                        else:
                            console.print("Canceled")
                            continue
                    
                    elif choice == "2":
                        if Confirm.ask(prompt="Are you sure you want to delete all the configs?\nOnce you delete file, there is no going back. Please be certain.",
                                    console=console):
                            clear_dir(CONFIG_DIR)
                            init_content_dirs() 
                            console.print("Configs clear")
                        else:
                            console.print("Canceled")
                            continue

                    elif choice == "3":
                        if Confirm.ask(prompt="Are you sure you want to delete all the models?\nOnce you delete file, there is no going back. Please be certain.",
                                    console=console):
                            clear_dir(MODELS_DIR)
                            init_content_dirs() 
                            console.print("Models clear")
                        else:
                            console.print("Canceled")
                            continue

                    elif choice == "4":
                        if Confirm.ask(prompt="Are you sure you want to delete all the content?\nOnce you delete file, there is no going back. Please be certain.",
                                    console=console):
                            clear_dir(LOGS_DIR, [TENSORBOARD_DIR.name])
                            clear_dir(TENSORBOARD_DIR)
                            clear_dir(MODELS_DIR)
                            clear_dir(CONFIG_DIR)
                            init_content_dirs() 
                            console.print("Content clear")
                        else:
                            console.print("Canceled")
                            continue

                    continue
                #endregion
            
                elif choice == "4":
                    break
        #endregion

        elif choice == "4":
            console.print(f"\nGitHub : {GITHUB_URL}")
            webbrowser.open(GITHUB_URL)
                
        elif choice == "5":
            sys.exit(0)
            break

if __name__ == "__main__":
    main()