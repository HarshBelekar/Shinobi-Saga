import pygame  # type: ignore



# -------------------- Initialize Pygame --------------------
pygame.init()

# -------------------- Global Settings --------------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shinobi Saga")

# -------------------- Imports Python Codes --------------------
import button
import battle
import help
from assets import images, sounds  # Import preloaded images and sounds

# -------------------- Setup Buttons --------------------
start_button = button.Button(375, 460, images["start"], 1)
help_button = button.Button(100, 490, images["help"], 1)
exit_button = button.Button(680, 490, images["exit"], 1)

# -------------------- Main Menu Loop --------------------
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        screen.blit(images["bg"], (0, 0))       # Draw background
        screen.blit(images["logo"], (130, 80))  # Draw game logo

        # ---- Handle Button Clicks ----
        if start_button.draw(screen):
            sounds["click"].play()
            battle_screen = battle.Battle()
            battle_screen.run_game()

        if help_button.draw(screen):
            sounds["click"].play()
            help.help_screen(SCREEN_WIDTH)

        if exit_button.draw(screen):
            sounds["click"].play()
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
