import pygame # type: ignore
from shuriken import Shuriken # Import Shuriken class for projectile attacks
import random
from health import HealthBar # Import custom HealthBar class for visual health display
from assets import images, sounds, load_animation , load_character # Centralized asset import

class Character:
    
    def __init__(self, x, y):
        """Initialize the character with position, motion, animations, health, etc."""
        
        self.x = x  # X coordinate (horizontal position)
        self.y = y  # Y coordinate (vertical position)
        self.constant_y = y # Base/ground Y position used for resetting jump
        self.vel_x = 5  # Speed of horizontal movement
        self.vel_y = 0  # Initial vertical velocity (used for jumping)
        self.gravity = 1  # Gravity effect on jumping
        self.L_limit = -18  # Left movement boundary
        self.R_limit = 80  # Right movement margin from screen edge
        self.screen_width=1000 # Width of the game screen
        
        self.is_jumping = False  # Flag to check if currently jumping
        self.on_ground = True  # Flag to check if on the ground
        self.facing_right = True  # Direction the character is facing
        self.shurikens = []  # List to store thrown shuriken objects
        
        # Animation & State
        self.state = "stand"  # Initial animation state
        self.frame = 0  # Frame index for animations
        self.animation_speed = 0.3  # Speed of animation transitions
        self.throw_timer = 0  # Timer to manage shuriken throw cooldown
        self.count=0 # Misc variable used for defeated state
        
        # Load character head icon for health bar
        self.icon = images["naruto_head"]
        self.health_bar=HealthBar(self.icon,self.x,self.y) # Create health bar instance
        
        # Load character base images
        self.images = {
            "stand": load_character("naruto","stand"),
            "defeated": load_character("naruto","defeated"),
        }

        # Load animations from character folder
        self.animations = {
            "run": load_animation("naruto","run", 6),
            "jump": load_animation("naruto","jump", 4),
            "throw": load_animation("naruto","throw", 3),
        }
        
        # Load sounds from centralized dictionary
        self.jump_sound = sounds["jump"]
        self.throw_sound = sounds["throw"]

    def handle_input(self, keys):
        """Handle keyboard input to control character movement and actions."""
        
        # If already throwing, continue animation and cooldown
        if self.throw_timer > 0:
            self.state = "throw"
            self.throw_timer -= 1
            return
        
        # Handle shuriken throw
        if keys[pygame.K_SPACE] :
            self.throw_sound.play()
            self.state = "throw"
            self.frame = 0
            self.throw_timer = len(self.animations["throw"]) * 4 # Cooldown duration
            
            # Limit shuriken count and add a bit of randomness
            if len(self.shurikens) < 6 and random.randint(1,2) == 1:
                
                # Create a new shuriken and add it to the list
                new_shuriken = Shuriken(
                    self.x + 60 if self.facing_right else self.x + 20, 
                    self.y, 
                    self.facing_right)
                self.shurikens.append(new_shuriken)
            return
        
        # Handle horizontal movement
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.R_limit :
            self.x += self.vel_x
            self.facing_right = True
            if not self.is_jumping:
                self.state = "run"
        
        elif keys[pygame.K_LEFT] and self.x > self.L_limit:
            self.x -= self.vel_x
            self.facing_right = False
            if not self.is_jumping:
                self.state = "run"
        
        else:
            self.state = "stand" # No movement = standing
        
        # Handle jump
        if keys[pygame.K_UP] and self.on_ground:
            self.jump_sound.play()
            self.is_jumping = True
            self.on_ground = False
            self.vel_y = -15 # Initial jump force
            self.frame = 0
            
    def apply_physics(self):
        """Apply gravity and jump movement."""
        if self.is_jumping:
            self.state = "jump"
            self.y += self.vel_y
            self.vel_y += self.gravity
            
            # Stop jumping if character hits the ground
            if self.y >= self.constant_y:
                self.y = self.constant_y
                self.is_jumping = False
                self.on_ground = True
                self.vel_y = 0

    def update_animation(self):
        """Return the correct animation frame based on the current state."""

        if self.state in ["stand", "defeated"]:
            image = self.images[self.state]
            self.frame = 0
        else:
            self.frame += self.animation_speed if self.state == "run" else 0.1
            frames = self.animations[self.state]
            image = frames[int(self.frame) % len(frames)]
        
        # Flip character image if facing left
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        return image
    
    def draw(self, surface):
        """Draw the character with current animation frame."""
        image = self.update_animation()
        
        # Adjust vertical offset if defeated animation
        if self.state == "defeated" and self.count == 1:
            self.y+=23
        
        surface.blit(image, (self.x, self.y))  # Draw character
        
        # Update hitbox for collision
        self.rect = pygame.Rect(self.x+10, self.y+5,80,85)

    def update_shurikens(self, surface):
        """Update and draw all active shurikens."""
        for shuriken in self.shurikens[:]:
            shuriken.update() # Move shuriken
            shuriken.draw(surface)  # Draw it on the screen
        
            # Remove shurikens that went off-screen
            if not shuriken.active:
                self.shurikens.remove(shuriken)

    def display_health(self,surface):
        """Display the character's health bar on screen."""
        self.health_bar.player_bar(surface)
