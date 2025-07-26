import pygame 
from shuriken import Shuriken # Import the Shuriken class for enemy to throw
import random
from health import HealthBar # Import custom HealthBar class for visual health display
from assets import images, sounds, load_animation , load_character # Centralized asset import


class Enemy:
    
    def __init__(self, x, y):
        """ Initialize the enemy character with position, state, animations, and health. """
        
        # ----- Position and Physics Settings -----
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
        self.is_throwing = False  # Is currently in throw animation
        self.shurikens = []  # List to store thrown shuriken objects
        self.is_big=False # Whether next shuriken is big
        self.is_hit = False # True if recently hit
        
        # ----- Animation Control -----
        self.state = "stand"  # Initial animation state
        self.frame = 0  # Frame index for animations
        self.throw_timer = 0  # Timer to manage shuriken throw cooldown
        self.jump_chance = 0.03 # Small chance to jump every frame
        self.throw_chance = 0.03  # Small chance to Throw every frame
        self.throw_duration = 30  # Frames the throw lasts (~0.5 sec at 60 FPS)
        self.hit_count=0

        # ----- Health and UI -----
        self.icon = images.get("sasuke_head")
        self.health_bar=HealthBar(self.icon,self.x,self.y) # Create health bar instance

        # ----- Load Static Images -----
        self.images = {
            "stand": load_character("sasuke", "stand"),
            "block": load_character("sasuke","guard"),
            "small_damage": load_character("sasuke","small_damage"),
            "big_damage": load_character("sasuke","big_damage"),
            "winner": load_character("sasuke","winner"),
        }
        
        # ----- Load Animations -----
        self.animations = {
            "run": load_animation("sasuke", "run", 6),
            "jump": load_animation("sasuke", "jump", 4),
            "throw": load_animation("sasuke", "throw", 3),
            "defeated": load_animation("sasuke","defeated",3),
        }
        
        # ----- Load Sounds -----
        self.jump_sound = sounds.get("jump")
        self.throw_sound = sounds.get("throw")
        self.block_sound= sounds.get("block")

    def jump(self):
        """ Trigger jump action with upward velocity and sound. """
        self.is_jumping = True
        self.on_ground = False
        self.vel_y = -15  # Jump strength
        self.jump_sound.play()
    
    def throw_shuriken(self):
        """ Trigger throw action and create a new shuriken if conditions are met. """
        
        if not self.is_throwing :  # Only throw if not already throwing
            self.throw_sound.play()
            self.state = "throw"
            self.is_throwing = True
            self.throw_timer = self.throw_duration
            self.is_big = True if random.randint(1,10) == 1 else False 
            
            if len(self.shurikens) < 6 : 
                # Create a new shuriken and add it to the list
                new_shuriken = Shuriken(
                    self.x + 60 if self.facing_right else self.x + 20, 
                    self.y, 
                    self.facing_right,
                    self.is_big
                    )
                self.shurikens.append(new_shuriken)

                # Reset hit count after attack
                self.hit_count = 0
    
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
    
    def move_enemy(self):
        """ Control enemy movement logic and AI: walk, jump, throw randomly. """
        
        if self.state == "defeated":
            return  # Skip all input/movement if defeated

        # Pause movement during throwing
        if self.is_throwing:
            self.throw_timer -= 1
            if self.throw_timer <= 0:
                self.is_throwing = False
            return  # Skip movement while throwing
        
        # -------- Movement direction and screen boundaries --------
        if self.state != "block" and not self.is_hit :
            if self.facing_right:
                self.x += self.vel_x
                if self.x > self.screen_width - self.R_limit:
                    self.facing_right = False
            else:
                self.x -= self.vel_x
                if self.x < self.L_limit:
                    self.facing_right = True

        # -------- Update state based on movement or hit --------
        if self.on_ground and not self.is_hit:
            self.state = "run" 
        elif not self.on_ground and not self.is_hit :
            self.state = "jump"
        elif self.state in ["run","jump"] :
            self.is_hit = False # Clear hit state after motion


        # -------- Random Jump --------
        if self.on_ground and random.random() < self.jump_chance and not self.is_hit:
            self.jump()
        
        # -------- Random Throw --------
        if not self.is_throwing and random.random() < self.throw_chance :
            self.throw_shuriken()
        
        # -------- Switch to block if recently hit and grounded --------
        if not self.is_jumping and self.hit_count > 0 and not self.is_hit:
            self.state = "block"
            
        self.apply_physics()
    
    def update_animation(self):
        """Return the correct animation frame based on the current state."""
        
        # -------- Static States (single frame) --------
        if self.state in ["stand","block","winner"]:
            image = self.images[self.state]
            self.frame = 0
        
        # ---- Damage Reaction Frames ----
        elif self.state in ["small_damage", "big_damage"]:
            image = self.images[self.state]
            self.frame +=1
            if self.frame > 10:  # Show damage image for ~10 frames
                self.is_hit=False
                self.frame = 0

        # -------- Defeated Animation (multi-frame + step back) --------
        elif self.state == "defeated":
            self.frame += 0.05
            max_frame = len(self.animations["defeated"]) - 1
            image = self.animations["defeated"][min(int(self.frame), max_frame)]

            # Step back slowly only during early defeated frames
            if int(self.frame) < max_frame:
                if self.facing_right:
                    if self.x -2 >= self.L_limit: 
                        self.x -= 2  # Move back left if facing right
                else:
                    if self.x + 2 <= self.screen_width - self.R_limit: 
                        self.x += 2  # Move back right if facing left
        
        # -------- Animated States (run, jump, throw, etc.) --------
        else:
            self.frame += 0.09 if self.state == "throw" else 0.13
            
            frames = self.animations[self.state]
            image = frames[int(self.frame) % len(frames)]
        
        # Flip character image if facing left
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        return image
    
    def draw(self, surface):
        """Draw the character with current animation frame."""
        image = self.update_animation()
        
        surface.blit(image, (self.x, self.y)) # Draw character
        
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
        self.health_bar.enemy_bar(surface)
