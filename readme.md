# DuckAI

Un logiciel d'entraînement et de visualisation d'IA dans le but de résoudre le "Problème du canard et du loup" basé sur Gymnasium et Stable-Baselines3. Réalisé dans le cadre de Math En Jean.

## Description

DuckAI est un logiciel permettant d'entraîner et de visualiser des IA dans le but de résoudre le "Problème du canard et du loup". Dans ce problème, un canard se trouve au centre d'une mare autour de laquelle se trouve un loup ; le canard doit atteindre le bord de la mare sans que le loup s'y trouve. Le but est de trouver le rapport de vitesse canard/loup le plus faible.

## Getting Started

### Dependencies

#### Standalone installer
* Windows 10/11 ou distribution Linux avec prise en charge de `.deb`
* Avec CUDA : GPU NVIDIA avec prise en charge de CUDA 13.0

#### From Source
* Git
* Python 3.14.4 ou supérieur
* Les dépendances listées dans `requirements-cpu.txt` ou `requirements-cuda.txt`

### Installing

#### Standalone installer

**Windows :**

Télécharger la dernière release correspondant à votre configuration sur la [page des releases](https://github.com/Mat-Sharp0/Math-en-jean-duck-problem-DRL-V2/releases/latest) :
- `DuckAI_x.x.x_windows_cpu_setup.exe` — version CPU (tous les PC)
- `DuckAI_x.x.x_windows_cuda_setup.exe` — version GPU NVIDIA (recommandée pour l'entraînement)

> **Note :** Pour connaître votre version de CUDA, exécutez `nvidia-smi` dans votre terminal.

Exécuter l'installeur téléchargé et suivre les étapes à l'écran.

**Linux :**

Télécharger la dernière release correspondant à votre configuration :
- `DuckAI_x.x.x_linux_cpu_setup.sh` — version CPU
- `DuckAI_x.x.x_linux_cuda_setup.sh` — version GPU NVIDIA

Rendre le fichier exécutable et lancer l'installation :
```bash
chmod +x DuckAI_x.x.x_linux_cpu_setup.sh
./DuckAI_x.x.x_linux_cpu_setup.sh
```

#### From Source

Cloner le dépôt :
```bash
git clone https://github.com/Mat-Sharp0/Math-en-jean-duck-problem-DRL-V2.git
cd Math-en-jean-duck-problem-DRL-V2
```

Installer les dépendances correspondant à votre configuration :

CPU :
```bash
pip install -r requirements-cpu.txt
```

CUDA 13.0 :
```bash
pip install -r requirements-cuda.txt
```

> **Note :** Il est recommandé d'utiliser un environnement virtuel (`python -m venv .venv`).

> **Note :** Pour d'autres versions de CUDA, installer les dépendances CPU puis la version de PyTorch correspondante depuis [pytorch.org](https://pytorch.org/get-started/locally/).

### Executing program

#### Standalone installer
Lancer Duck AI depuis le menu démarrer ou le raccourci bureau.

#### From Source
Exécuter la commande suivante:
```bash
python main.py
```

> **Note :** Si vous utilisez un environnement virtuel, activez-le dans votre terminal avant de lancer le programme (`.venv\Scripts\activate`).

## Authors

* HIOLLE Mateo

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.