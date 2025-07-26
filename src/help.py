import pygame
import button
from assets import images, sounds  # Import centralized assets

# ----------------- Help Screen Function -----------------
def help_screen(SCREEN_WIDTH):
    help_running = True
    clock = pygame.time.Clock()
    FPS = 60
    
    # --- Font and Sound ---
    font = pygame.font.SysFont("comicsans", 30, True)
    click = sounds["click"]

    # --- Load Button Images ---
    back_img = images["back"]
    
    # --- Create Button ---
    back_button = button.Button(2, 2, back_img, 0.5)

    # --- Instruction Lines ---
    instructions = [
        "1. Use LEFT Arrow Key to Move Left",
        "2. Use RIGHT Arrow Key to Move Right",
        "3. Use UP Arrow Key to Jump",
        "4. Press SPACE & Shift + SPACE to Throw Small & Big Shuriken ",
        "5. Use DOWN Arrow Key to Block Shuriken",
        "5.1 You can Block 2 Shuriken in Row.",
        "5.2 After that you need to attack 1 Shuriken to block another",
        "    Shuriken"
    ]

    # ----------------- Help Screen Loop -----------------
    while help_running:
        clock.tick(FPS)  # Maintain frame rate
        pygame.display.get_surface().fill("black")  # Clear screen

        # --- Render Title ---
        title_text = font.render("Controls", True, "red")
        pygame.display.get_surface().blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

        # --- Render Instructions ---
        for i, line in enumerate(instructions):
            rendered_line = font.render(line, True, "white")
            pygame.display.get_surface().blit(rendered_line, (20, 80 + i * 60))

        # --- Draw Back Button ---
        if back_button.draw(pygame.display.get_surface()):
            click.play()
            help_running = False  # Exit Help Screen

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                help_running = False

        # --- Update Screen ---
        pygame.display.update()
