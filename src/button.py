import pygame  # type: ignore

class Button:
    """A clickable button with image scaling, hover effect, and click detection."""

    def __init__(self, x, y, image, scale):
        """
        Initialize the Button.

        Args:
            x (int): X-coordinate of the top-left corner.
            y (int): Y-coordinate of the top-left corner.
            image (pygame.Surface): The original button image.
            scale (float): Scale factor for the image size.
        """
        width = image.get_width()
        height = image.get_height()

        # Scale the image according to the given scale
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

        # Store the original image for hover effect
        self.original_image = self.image.copy()

        # Create a slightly darker version for hover effect
        self.hover_image = self.image.copy()
        self.hover_image.set_alpha(220)  # Slightly transparent on hover

        # Set button position and click flag
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """
        Draw the button on the screen and handle click detection.

        Args:
            surface (pygame.Surface): The surface to draw the button on.

        Returns:
            bool: True if the button was clicked, False otherwise.
        """
        action = False
        mouse_pos = pygame.mouse.get_pos()

        # Check if the mouse is hovering over the button
        if self.rect.collidepoint(mouse_pos):
            # Draw hover image
            surface.blit(self.hover_image, self.rect.topleft)

            # Check for left mouse click
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            # Draw original image (normal state)
            surface.blit(self.original_image, self.rect.topleft)

        # Reset click status when mouse is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action
