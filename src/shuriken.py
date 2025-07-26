import pygame
from assets import images # Centralized asset import

# Shuriken class to handle its behavior and rendering
class Shuriken:
    
    def __init__(self, x, y, facing_right,is_big):
        
        self.damage = 10  # 💥 damage on hit
        
        # Load the Small shuriken image
        if is_big :
            self.img = "big_shuriken" 
            self.damage = 20 # Big damage on hit
        else :
            self.img = "small_shuriken" 
            
        self.original_image = images[self.img]
        
        # Starting angle
        self.angle = 0
        
        # Set its position (x, y)
        self.x = x
        self.y = y + 30  # Slight offset so it comes from the hand
        
        # Set its speed (move right or left depending on player direction)
        self.speed = 10 if facing_right  else -10
    
        self.facing_right = facing_right # Remember the direction it's going
        self.active = True # This is used to check if it should still be on screen
        
        # Create a rectangle for collision or screen limits
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        # Move the shuriken
        self.x += self.speed
        self.rect.x = self.x # Update rectangle position
        
        # Spin the shuriken
        self.angle = (self.angle + 15) % 360  # Rotate 15 degrees every frame
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        # Recalculate position to center the rotated image
        self.rect = self.image.get_rect(center=self.rect.center)

        # If it goes off screen, mark it as inactive
        if self.x < -50 or self.x > 1050:
            self.active = False

    def draw(self, surface):
        # Draw the spinning shuriken
        surface.blit(self.image, self.rect.topleft)
