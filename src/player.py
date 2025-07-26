import pygame 
from shuriken import Shuriken # Import Shuriken class for projectile attacks
import random
from health import HealthBar # Import custom HealthBar class for visual health display
from assets import images, sounds, load_animation , load_character # Centralized asset import

class Character:
    
    def __init__(self, x, y):
        """Initialize the character with position, motion, animations, health, etc."""
        
        # ----- Position & Movement -----
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
        self.is_big=False # Determines if next shuriken is big
        self.is_hit = False # Set to True when hit by a shuriken

        # ----- Animation & Logic -----
        self.state = "stand"  # Initial animation state
        self.frame = 0  # Frame index for animations
        self.animation_speed = 0.3  # Speed of animation transitions
        self.throw_timer = 0  # Timer to manage shuriken throw cooldown
        self.block_count = 0 # How many times player has blocked consecutively

        # ----- UI & Health -----
        self.icon = images["naruto_head"] # Load character head icon for health bar
        self.health_bar=HealthBar(self.icon,self.x,self.y) # Create health bar instance
        
        # ----- Static Images for One-Frame States -----
        self.images = {
            "stand": load_character("naruto","stand"),
            "block": load_character("naruto","guard"),
            "small_damage": load_character("naruto","small_damage"),
            "big_damage": load_character("naruto","big_damage"),
            "winner": load_character("naruto","winner"),
        }

        # ----- Animated State Sequences -----
        self.animations = {
            "run": load_animation("naruto","run", 6),
            "jump": load_animation("naruto","jump", 4),
            "throw": load_animation("naruto","throw", 3),
            "defeated": load_animation("naruto","defeated",3),
        }
        
        # ----- Sound Effects -----
        self.jump_sound = sounds["jump"]
        self.throw_sound = sounds["throw"]
        self.block_sound= sounds["block"]

    def handle_input(self, keys):
        """Handle keyboard input to control character movement and actions."""
        
        if self.state == "defeated":
            return  # Skip all input/movement if defeated
        
        # Throwing cooldown in progress
        if self.throw_timer > 0:
            self.state = "throw"
            self.throw_timer -= 1
            return
        
        # ---- Throw Shuriken ----
        if keys[pygame.K_SPACE] :
            
            # Check for big shuriken with Shift
            self.is_big = True if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else False 
            
            self.throw_sound.play()
            self.state = "throw"
            self.frame = 0
            self.throw_timer = len(self.animations["throw"]) * 4 # Cooldown duration
            
            # Add shuriken if under max and randomly selected
            if len(self.shurikens) < 6 and random.randint(1,2) == 1:
                
                # Create a new shuriken and add it to the list
                new_shuriken = Shuriken(
                    self.x + 60 if self.facing_right else self.x + 20, 
                    self.y, 
                    self.facing_right,
                    self.is_big)
                self.shurikens.append(new_shuriken)
                
                # Reset block chain after attack
                if self.block_count > 0:
                    self.block_count = 0
            return
        
        # ---- Guarding ----
        if keys[pygame.K_DOWN] and not self.is_jumping :
            self.state = "block"
            return
        
        # ---- Movement ----
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.R_limit and not self.is_hit:
            self.x += self.vel_x
            self.facing_right = True
            if not self.is_jumping:
                self.state = "run"
        
        elif keys[pygame.K_LEFT] and self.x > self.L_limit and not self.is_hit:
            self.x -= self.vel_x
            self.facing_right = False
            if not self.is_jumping:
                self.state = "run"
        
        # ---- Idle ----
        elif self.state not in ["small_damage", "big_damage"]:
            self.is_hit = False
            self.state = "stand" # No movement = standing
        
        # ---- Jumping ----
        if keys[pygame.K_UP] and self.on_ground :
            self.jump_sound.play()
            self.is_jumping = True
            self.on_ground = False
            self.vel_y = -15 # Initial jump force
            self.frame = 0

    def apply_physics(self):
        """Apply gravity and handle landing for jumping or defeated state."""

        # Check if character is in air (either jumping or falling from defeat)
        is_falling = self.is_jumping or (self.state == "defeated" and not self.on_ground)

        if is_falling:
            self.y += self.vel_y
            self.vel_y += self.gravity

            # Set jump animation if jumping and not defeated
            if self.is_jumping and self.state != "defeated":
                self.state = "jump" # Apply jump animation

            # Landing condition
            if self.y >= self.constant_y:
                self.on_ground = True
                self.vel_y = 0
                self.is_jumping = False

                # If defeated, sink below ground
                self.y = self.constant_y + 23 if self.state == "defeated" else self.constant_y

        else:
            # Smooth sinking animation when defeated
            if self.state == "defeated" and self.y < self.constant_y + 23:
                self.y += 1

    def update_animation(self):
        """Return the correct animation frame based on the current state."""

        # -------- Static States (single frame) --------
        if self.state in ["stand", "block","winner"]:
            image = self.images[self.state]
            self.frame = 0
        
        # ---- Damage Reaction Frames ----
        elif self.state in ["small_damage", "big_damage"]:
            image = self.images[self.state]
            self.frame += 1
            if self.frame > 10:  # Show damage image for ~10 frames
                self.is_hit = False
                self.state = "stand"
                self.frame = 0
        
        # -------- Defeated Animation (multi-frame + step back) --------
        elif self.state == "defeated":
            self.frame += 0.05 # Slower defeat animation

            defeated_frames = self.animations["defeated"]
            max_frame = len(defeated_frames) - 1
            current_frame_index = min(int(self.frame), max_frame)
            image = defeated_frames[current_frame_index]

            # Step back effect only during early defeat frames
            if current_frame_index < max_frame:
                if self.facing_right:
                    if self.x -2 >= self.L_limit: 
                        self.x -= 2  # Move back left if facing right
                else:
                    if self.x + 2 <= self.screen_width - self.R_limit: 
                        self.x += 2  # Move back right if facing left
        
        # -------- Animated States (run, jump, throw, etc.) --------
        else:
            self.frame += self.animation_speed if self.state == "run" else 0.1
            
            frames = self.animations[self.state]
            image = frames[int(self.frame) % len(frames)]

        # -------- Flip Image if Facing Left --------
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        return image
        
    def draw(self, surface):
        """Draw the character with current animation frame."""
        image = self.update_animation()
        
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
