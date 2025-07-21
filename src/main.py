import pygame  # type: ignore
import button
import battle
import help

# -------------------- Initialize Pygame --------------------
pygame.init()

# -------------------- Global Settings --------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shinobi Saga")

# -------------------- Asset Paths --------------------
ASSETS = "assets/"
UI_PATH = ASSETS + "images/ui/main_menu/"
SFX_PATH = ASSETS + "sounds/"

# -------------------- Load Images --------------------
try:
    bg = pygame.image.load(ASSETS + "images/background/bg.png").convert_alpha()
    logo = pygame.image.load(UI_PATH + "game_logo.png").convert_alpha()
    start_img = pygame.image.load(UI_PATH + "start_button.png").convert_alpha()
    help_img = pygame.image.load(UI_PATH + "help_button.png").convert_alpha()
    exit_img = pygame.image.load(UI_PATH + "exit_button.png").convert_alpha()
except Exception as e:
    print("[ERROR] Failed to load images:", e)
    exit()

# -------------------- Load Sounds --------------------
try:
    click = pygame.mixer.Sound(SFX_PATH + "click.wav")
    pygame.mixer.music.load(SFX_PATH + "bg_music.mp3")
    pygame.mixer.music.play(-1)  # Loop background music indefinitely
except Exception as e:
    print("[WARNING] Sound loading error:", e)

# -------------------- Setup Buttons --------------------
start_button = button.Button(375, 460, start_img, 1)
help_button = button.Button(100, 490, help_img, 1)
exit_button = button.Button(680, 490, exit_img, 1)

# -------------------- Main Menu Loop --------------------
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        screen.blit(bg, (0, 0))       # Draw background
        screen.blit(logo, (130, 80))  # Draw game logo

        # ---- Handle Button Clicks ----
        if start_button.draw(screen):
            click.play()
            battle_screen = battle.Battle()
            battle_screen.run_game()

        if help_button.draw(screen):
            click.play()
            help.help_screen()

        if exit_button.draw(screen):
            click.play()
            running = False

        # ---- Handle Quit Event ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Refresh the display

    pygame.quit()

# -------------------- Start Game --------------------
if __name__ == "__main__":
    main()
