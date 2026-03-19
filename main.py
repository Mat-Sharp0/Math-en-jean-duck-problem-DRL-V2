import os
from pathlib import Path
import sys

from src.utils.paths import init_content_dirs, CONTENT_DIR, CONFIG_DIR, MODELS_DIR, DEFAULT_CONFIG_DIR, LOGS_DIR, TENSORBOARD_DIR
from src.utils.file_function import open_folder, open_file, creat_config, clear_dir

import tkinter as tk
from tkinter import filedialog

import webbrowser
from rich.prompt import Prompt

from src.train import train_model
from src.visualize import visualize

from src.utils.updater import check_for_update
from src.utils.app_info import APP_NAME, VERSION, AUTHOR, GITHUB_URL

#region Init
init_content_dirs()

terminal_width = os.get_terminal_size().columns

print("-" * terminal_width)
print(APP_NAME)
print("-" * terminal_width)
print(f"By {AUTHOR}")
print("License: MIT")
print(f"Version: {VERSION}")

if getattr(sys, 'frozen', False):
    check_for_update()

#endregion

while True:
    
    print("\nChoose an option:")
    print("1. Train\n2. Visualize\n3. Manage file\n4. Documentation\n5. Close")

    choice = Prompt.ask(choices=["1", "2", "3", "4", "5"])

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
            print ("No config file selected")
        else:
            try:
                train_model(config)
            except OSError as err:
                print("OS error:", err)
            except ValueError:
                print("Could not convert data to an integer.")
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
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
            print("No model file selected")
        else:
            while True:
                episodes=input("Episodes: ")
                if episodes == "":
                    print("Episodes not defined")
                else:
                    visualize(model, int(episodes))
                    break
    #endregion

    #region File Managment
    elif choice == "3":
        while True:
            print("1. Open content folder\n2. New config file\n3. Clear file\n4. Go Back")
            choice = Prompt.ask(choices=["1", "2", "3", "4"])
            
            if choice == "1":
                open_folder(CONTENT_DIR)
                continue


            #region Makefile
            elif choice == "2":
                print("1. PPO\n2. TD3\n3. SAC\n4. Go Back")
                choice = Prompt.ask(choices=["1", "2", "3", "4"])

                if choice == "1":
                    try:
                        new_config = creat_config(template_path=(DEFAULT_CONFIG_DIR / "default_config_ppo.yaml"))
                    except ValueError("Canceled"):
                        print("Canceled")
                        continue
                    print(f"Config file create: {new_config}")
                    open_file(new_config)
                        
                elif choice == "2":
                    try:
                        new_config = creat_config(template_path=(DEFAULT_CONFIG_DIR / "default_config_td3.yaml"))
                    except ValueError("Canceled"):
                        print("Canceled")
                        continue
                    print(f"Config file create: {new_config}")
                    open_file(new_config)

                elif choice == "3":
                    try:
                        new_config = creat_config(template_path=(DEFAULT_CONFIG_DIR / "default_config_sac.yaml"))
                    except ValueError("Canceled"):
                        print("Canceled")
                        continue
                    print(f"Config file create: {new_config}")
                    open_file(new_config)
                continue
            #endregion

            #region Clearfile
            elif choice == "3":
                print("1. Clear logs\n2. Clear config files\n3. Clear models\n4. Clear all\n5. Go Back")
                choice = Prompt.ask(choices=["1", "2", "3", "4", "5"])
                if choice == "1":
                    print("Are you sure you want to delete all the logs?\nOnce you delete file, there is no going back. Please be certain.")
                    choice = Prompt.ask(choices=["y", "n"])
                    if choice == "y":
                        clear_dir(LOGS_DIR, {TENSORBOARD_DIR.name})
                        clear_dir(TENSORBOARD_DIR)
                        init_content_dirs()
                        print("Logs clear")
                    elif choice == "2":
                        print("Canceled")
                        continue
                elif choice == "2":
                    print("Are you sure you want to delete all the configs?\nOnce you delete file, there is no going back. Please be certain.")
                    choice = Prompt.ask(choices=["y", "n"])
                    if choice == "y":
                        clear_dir(CONFIG_DIR)
                        init_content_dirs() 
                        print("Configs clear")
                    elif choice == "2":
                        print("Canceled")
                        continue
                elif choice == "3":
                    print("Are you sure you want to delete all the models?\nOnce you delete file, there is no going back. Please be certain.")
                    choice = Prompt.ask(choices=["y", "n"])
                    if choice == "y":
                        clear_dir(MODELS_DIR)
                        init_content_dirs() 
                        print("Models clear")
                    elif choice == "2":
                        print("Canceled")
                        continue
                elif choice == "4":
                    print("Are you sure you want to delete all the content?\nOnce you delete file, there is no going back. Please be certain.")
                    choice = Prompt.ask(choices=["y", "n"])
                    if choice == "y":
                        clear_dir(LOGS_DIR, [TENSORBOARD_DIR.name])
                        clear_dir(TENSORBOARD_DIR)
                        clear_dir(MODELS_DIR)
                        clear_dir(CONFIG_DIR)
                        init_content_dirs() 
                        print("Content clear")
                    elif choice == "2":
                        print("Canceled")
                        continue
                continue
            #endregion
         
            elif choice == "4":
                break
    #endregion

    elif choice == "4":

        print(f"\nGitHub : {GITHUB_URL}")
        webbrowser.open(GITHUB_URL)
            
    elif choice == "5":
        sys.exit(0)
        break