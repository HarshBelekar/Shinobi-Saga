import pygame
import os
import sys

# ----------------- Asset Base Path -----------------
SND_PATH = "assets/sounds/"
MENU_PATH = "assets/images/ui/main_menu/"
PAUSE_MENU_PATH = "assets/images/ui/pause_menu/"
BANNERS_PATH = "assets/images/ui/banners/"
ICONS_PATH = "assets/images/ui/icons/"
BG_PATH = "assets/images/background/"
WEAPON_PATH = "assets/images/weapons/"

# ----------------- Resource Path Utility -----------------
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----------------- Image Loader -----------------
def load_image(path: str, convert_alpha=True):
    try:
        img = pygame.image.load(resource_path(path))
        return img.convert_alpha() if convert_alpha else img.convert()
    except Exception as e:
        print(f"[ERROR] Failed to load image: {path}\n{e}")
        return None

# ----------------- UI Helper Loader -----------------
def load_ui_images(folder_path, name_map):
    return {
        key: load_image(os.path.join(folder_path, f"{filename}.png"))
        for key, filename in name_map.items()
    }

# ----------------- Loading Animation Images --------------
def load_animation(character: str, action: str, frame_count: int):
        bace_path = f"assets/images/characters/{character}/{action}/{action}_"

        return [
        pygame.image.load(resource_path(f"{bace_path}{i}.png")).convert_alpha()
        for i in range(1, frame_count + 1)
    ]

# ----------------- Loading Single Animation Images --------------
def load_character(character: str, action: str):
    path = f"assets/images/characters/{character}/{action}/{action}_1"
    
    return pygame.image.load(resource_path(f"{path}.png")).convert_alpha()


# ----------------- Image Assets -----------------
images = {
    "bg": load_image(os.path.join(BG_PATH, "bg.png")),
    "logo": load_image(os.path.join(MENU_PATH, "game_logo.png")),
    "back": load_image(os.path.join(MENU_PATH, "back_button.png")),
}

# Main Menu
images.update(load_ui_images(MENU_PATH, {
    "start": "start_button",
    "help": "help_button",
    "exit": "exit_button",
}))

# Pause Menu
images.update(load_ui_images(PAUSE_MENU_PATH, {
    "pause_menu": "pause_menu",
    "resume": "resume_button",
    "restart": "restart_button",
    "home": "home_button",
    "exit1": "exit1_button",
    "pause": "pause_button"
}))

# Win Banners
images.update(load_ui_images(BANNERS_PATH, {
    "naruto_win": "naruto_wins",
    "sasuke_win": "sasuke_wins",
}))

# Icons
images.update(load_ui_images(ICONS_PATH, {
    "naruto_head": "naruto_head",
    "sasuke_head": "sasuke_head",
}))

# Weapons
images.update(load_ui_images(WEAPON_PATH, {
    "small_shuriken": "shur2",
    "big_shuriken": "shur",
}))

# ----------------- Sound Effects -----------------
sounds = {}
try:
    sounds["click"] = pygame.mixer.Sound(resource_path(os.path.join(SND_PATH, "click.wav")))
    sounds["throw"] = pygame.mixer.Sound(resource_path(os.path.join(SND_PATH, "shuriken.wav")))
    sounds["jump"] = pygame.mixer.Sound(resource_path(os.path.join(SND_PATH, "jump.wav")))
    sounds["hit"] = pygame.mixer.Sound(resource_path(os.path.join(SND_PATH, "hit.wav")))
    sounds["block"] = pygame.mixer.Sound(resource_path(os.path.join(SND_PATH, "block.wav")))
    
except Exception as e:
    print(f"[ERROR] Sound loading failed: {e}")

# ----------------- Background Music -----------------
try:
    pygame.mixer.music.load(resource_path(os.path.join(SND_PATH, "bg_music.mp3")))
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"[WARNING] Background music failed: {e}")

