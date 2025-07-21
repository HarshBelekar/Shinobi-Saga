# 🌀 Shinobi Saga - Naruto vs Sasuke ⚔️

A fast-paced 2D fighting game built with **Python** and **Pygame**, featuring anime-inspired characters — **Naruto** and **Sasuke** — in an epic shinobi showdown.

---

## 🎮 Game Features

- 🧍‍♂️ Two Playable Characters: Naruto (player) vs Sasuke (enemy)
- 🌀 Smooth Character Animations (Idle, Move, Jump, Attack, Defeated)
- 🗡️ Shuriken Attacks & Health System
- 🎵 Sound Effects for Clicks & Hits
- 🛠️ Pause Menu with Resume, Restart, Exit, and Home
- 🎌 Win Banners Displayed at Game Over
- 🎨 Custom UI and Backgrounds
- ⚙️ Clean, modular code with `Player`, `Enemy`, `Button`, and `Battle` classes

---

## 📂 Project Structure

    ShinobiSaga/                            
    ├── assets/
    │   ├── images/
    │   │   ├── background/                
    │   │   │   └── bg.png
    │   │   ├── ui/                         
    │   │   │   ├── game_logo.png 
    │   │   │   ├── start_button.png 
    │   │   │   ├── help_button.png 
    │   │   │   ├── exit_button.png        
    │   │   │   ├── pause_button.png 
    │   │   │   ├── resume_button.png
    │   │   │   ├── restart_button.png
    │   │   │   ├── home_button.png 
    │   │   │   ├── exit1_button.png  
    │   │   │   ├── naruto_wins.png 
    │   │   │   ├── sasuke_wins.png 
    │   │   │   ├── naruto_head.png 
    │   │   │   ├── sasuke_head.png 
    │   │   │   ├── pause_menu.png
    │   │   │   └── back_button.png 
    │   │   ├── weapons/                  
    │   │   │   ├── shur.png               
    │   │   │   └── shur2.png              
    │   │   └── characters/
    │   │       ├── naruto/
    │   │       │   ├── stand/            
    │   │       │   ├── run/
    │   │       │   ├── jump/
    │   │       │   ├── guard/
    │   │       │   ├── damage/
    │   │       │   ├── throw/
    │   │       │   ├── defeated/
    │   │       │   └──  winner/
    │   │       └── sasuke/
    │   │           ├── stand/
    │   │           ├── run/
    │   │           ├── jump/
    │   │           ├── guard/
    │   │           ├── damage/
    │   │           ├── throw/
    │   │           ├── defeated/
    │   │           └──  winner/
    │   └── sounds/                        
    │       ├── bg_music.mp3
    │       ├── jump.wav
    │       ├── shuriken.wav
    │       ├── hit.wav
    │       ├── click.wav
    │       └── block.wav
    │
    ├── src/                               
    │   ├── main.py                        
    │   ├── battle.py                      
    │   ├── player.py                      
    │   ├── enemy.py                      
    │   ├── help.py                
    │   ├── health.py                  
    │   ├── button.py                       
    │   └──  shuriken.py                 
    │                    
    ├── README.md
    ├── requirements.txt
    └── LICENSE

---

## ▶️ How to Run

### 🔧 Requirements
- Python 3.10+
- Pygame

## 📥 Installation
```bash
# Clone the repo
git clone https://github.com/HarshBelekar/Shinobi-Saga.git
cd Shinobi-Saga
```

### (Optional) Create a virtual environment
```bush
python -m venv venv
venv\Scripts\activate   # On Windows
```

### Install dependencies
```bush
pip install -r requirements.txt
```

### 🚀 Launch Game
```bush
cd src
python main.py
```
---

# 📸 Screenshots
Coming Soon...

---

# 📄 License

This project is licensed under the [MIT License](LICENSE).

---

### 🙌 Built with ❤️ by [Harsh Belekar](https://github.com/HarshBelekar)