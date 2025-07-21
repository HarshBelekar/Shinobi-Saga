import pygame  # type: ignore
import button

# ----------------- Initialize Pygame -----------------
pygame.init()

# ----------------- Global Settings -----------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shinobi Saga")

# ----------------- Help Screen Function -----------------
def help_screen():
    help_running = True
    clock = pygame.time.Clock()

    # --- Font and Sound ---
    font = pygame.font.SysFont("comicsans", 30, True)
    click = pygame.mixer.Sound("assets/sounds/click.wav")

    # --- Load Button Images ---
    back_img = pygame.image.load("assets/images/ui/main_menu/back_button.png").convert_alpha()
    
    # --- Create Button ---
    back_button = button.Button(2, 2, back_img, 0.5)

    # --- Instruction Lines ---
    instructions = [
        "1. Use LEFT Arrow Key to Move Left",
        "2. Use RIGHT Arrow Key to Move Right",
        "3. Use UP Arrow Key to Jump",
        "4. Press SPACE to Throw Shuriken"
    ]

    # ----------------- Help Screen Loop -----------------
    while help_running:
        clock.tick(FPS)  # Maintain frame rate
        screen.fill("black")  # Clear screen

        # --- Render Title ---
        title_text = font.render("Controls", True, "red")
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

        # --- Render Instructions ---
        for i, line in enumerate(instructions):
            rendered_line = font.render(line, True, "white")
            screen.blit(rendered_line, (220, 100 + i * 60))

        # --- Draw Back Button ---
        if back_button.draw(screen):
            click.play()
            help_running = False  # Exit Help Screen

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                help_running = False

        # --- Update Screen ---
        pygame.display.update()
