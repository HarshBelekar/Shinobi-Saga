import pygame 

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
    # Create a clock object to manage frame rate
    clock = pygame.time.Clock()
    
    # Flag to control the main loop
    running = True

    while running:
        
        clock.tick(FPS) # Limit frame rate to FPS
        
        # ---- Draw Background and Logo ----
        screen.blit(images["bg"], (0, 0))       # Draw background
        screen.blit(images["logo"], (130, 80))  # Draw game logo

        # ---- Handle Button Clicks ----
        
        # Start Game Button
        if start_button.draw(screen):
            sounds["click"].play() # Play click sound
            battle_screen = battle.Battle() # Create battle instance
            battle_screen.run_game()  # Run the battle screen

        # Help Button
        if help_button.draw(screen):
            sounds["click"].play() # Play click sound
            help.help_screen(SCREEN_WIDTH)  # Show help screen

        # Exit Button
        if exit_button.draw(screen):
            sounds["click"].play() # Play click sound
            running = False # Exit the main menu loop

        # ---- Handle Quit Event ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Quit the game if user closes the window

        pygame.display.flip()  # Update the full display surface to the screen

    # ---- Clean Exit ----
    pygame.quit() # Close the Pygame window and clean up resources

# -------------------- Start Game --------------------
if __name__ == "__main__":
    main()
