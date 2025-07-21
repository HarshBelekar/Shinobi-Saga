import pygame # type: ignore
from shuriken import Shuriken # Import Shuriken class for projectile attacks
import random
from health import HealthBar # Import custom HealthBar class for visual health display

# ----------------- Assets Paths -----------------
CHARACTER_PATH = "assets/images/characters/naruto/"
SFX_PATH = "assets/sounds/"
ICON_PATH = "assets/images/ui/icons/"

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

        # Load character icon (used in health bar)
        self.icon = pygame.image.load(ICON_PATH + "naruto_head.png").convert_alpha()
        
        self.count=0 # Misc variable used for defeated state
        
        # Load images and sounds
        self.load_images()
        self.load_sounds()
        
        # Create health bar instance
        self.health_bar=HealthBar(self.icon,self.x,self.y)
    
    def load_images(self):
        """Load all static and animated images for the character."""
        
        # Static images
        self.images = {
            "stand": pygame.image.load(CHARACTER_PATH + "stand/stand_1.png").convert_alpha(),
            "defeated": pygame.image.load(CHARACTER_PATH + "defeated/defeated_3.png").convert_alpha(),
        }

        # Load animations for actions
        self.animations = {
            "run": self.load_animation("run", 6),
            "jump": self.load_animation("jump", 4),
            "throw": self.load_animation("throw", 3),
        }
        
    def load_animation(self, action, frame_count):
        """Helper to load a list of animation frames for a specific action."""
        return [
            pygame.image.load(f"{CHARACTER_PATH}{action}/{action}_{i}.png").convert_alpha()
            for i in range(1, frame_count + 1)
        ]
        
    def load_sounds(self):
        """Load character-related sound effects."""
        self.jump_sound = pygame.mixer.Sound(SFX_PATH + "jump.wav")
        self.throw_sound = pygame.mixer.Sound(SFX_PATH + "shuriken.wav")
    
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

        if self.state == "stand":
            image = self.images["stand"]
            self.frame = 0
            
        elif self.state == "defeated":
            image = self.images["defeated"]
            self.frame = 0
            
        elif self.state == "run":
            self.frame += self.animation_speed
            image = self.animations["run"][int(self.frame) % len(self.animations["run"])]
            
        elif self.state == "jump":
            self.frame += 0.1
            image = self.animations["jump"][int(self.frame) % len(self.animations["jump"])]
            
        elif self.state == "throw":
            self.frame += 0.1
            image = self.animations["throw"][int(self.frame) % len(self.animations["throw"])]
            
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
