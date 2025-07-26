import pygame 
import sys
import button
import player
import enemy
from assets import images, sounds  # Import centralized assets

# ----------------- Game Settings -----------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

class Battle:
    
    def __init__(self):
        # Initialize Pygame and set up display
        pygame.init()
        self.battle_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        pygame.display.set_caption("Shinobi Saga - Battle")
        self.clock = pygame.time.Clock()
        
        # ----------------- Load Assets -----------------
        self.bg = images["bg"]
        self.pause_menu = images["pause_menu"]
        self.pause_img = images["pause"]
        self.resume_img = images["resume"]
        self.restart_img = images["restart"]
        self.exit_img = images["exit1"]
        self.home_img = images["home"]
        self.naruto_win = images["naruto_win"]
        self.sasuke_win = images["sasuke_win"]
        
        # ----------------- Load Sound -----------------
        self.click = sounds["click"]
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
        
        # ----------------- Buttons -----------------
        self.pause_button=button.Button(478,5,self.pause_img,0.7)
        self.resume_button=button.Button(390,170,self.resume_img,1)
        self.restart_button=button.Button(400,265,self.restart_img,1)
        self.exit_button=button.Button(400,355,self.exit_img,1)
        self.home_button=button.Button(465,450,self.home_img,1)
        
    def run_game(self):
        # ----------------- Game State Flags -----------------
        self.running = True
        self.paused = False
        self.restart=False
        
        # ----------------- Create Characters -----------------
        self.naruto = player.Character(10, 510)
        self.sasuke = enemy.Enemy(890,510)
        
        # -------- Game Loop --------
        while self.running:
            self.clock.tick(FPS)
            
            # Draw Background
            self.battle_screen.blit(self.bg, (0, 0))
            
            # Draw Pause Button & check Click
            if self.pause_button.draw(self.battle_screen) :
                self.paused=True
                self.click.play()
            
            # Character Logic (movement, attacks, shuriken updates)
            self.handle_character_logic(self.naruto, self.sasuke, is_player=True)
            self.handle_character_logic(self.sasuke, self.naruto, is_player=False)
            
            # -------- Pause Menu --------
            if self.paused:
                self.pause_game() # Render the semi-transparent overlay and pause menu UI
                
                #Check if Resume button is clicked
                if self.resume_button.draw(self.battle_screen):
                    self.paused=False  # Unpause the game and resume
                
                # Check if Restart button is clicked
                if self.restart_button.draw(self.battle_screen):
                    self.restart_game() # Restart the game state and loop
                
                # Check if Exit button is clicked
                if self.exit_button.draw(self.battle_screen):
                    self.running=False # Stop the game loop
                    pygame.quit() # Quit Pygame
                    sys.exit() # Exit the application completely
                
                # Check if Home button is clicked
                if self.home_button.draw(self.battle_screen):
                    self.running=False

            # -------- Handle Quit Event --------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update display
            pygame.display.flip()
        
        # Restart game loop if restart triggered
        if self.restart:
            self.run_game()
    
    def handle_character_logic(self, character, opponent, is_player=True):
        """ Handles movement, shuriken updates, physics, health, and state. """
        
        # Only update if character is alive and game is not paused
        if character.health_bar.health > 0 and not self.paused:
            if opponent.health_bar.health > 0:
                # If character is player-controlled, handle keyboard input
                if is_player:
                    character.handle_input(pygame.key.get_pressed())
                else:
                    # If character is enemy-controlled, run enemy movement logic
                    character.move_enemy()
            else:
                # Opponent is defeated, current character becomes winner
                character.state = "winner"
                self.game_over("naruto" if is_player else "sasuke") # Display win banner
            
        # If character's health is zero or below
        elif character.health_bar.health <= 0:
            # Only change to defeated state once (prevents re-triggering every frame)
            if character.state != "defeated":
                character.state = "defeated"
                character.frame = 0  # Reset defeated animation frame

        else:
            # Character is idle (e.g. paused or waiting)
            character.state = "stand"

        # Apply gravity and physics (jumping, falling)
        character.apply_physics()
        
        # Draw the character with current animation frame
        character.draw(self.battle_screen)
        
        # Update and draw shurikens if game is not paused
        if not self.paused:
            character.update_shurikens(self.battle_screen)
        
        # Draw health bar
        character.display_health(self.battle_screen)
        
        # Check if character's shuriken hit the opponent
        self.check_damage(character, opponent,is_player)

    def check_damage(self, attacker, target, is_player):
        """Checks if any of the attacker's shurikens hit the target 
        and applies damage or effects."""
        
        # Loop through a copy of the attacker's shuriken list to avoid mutation during iteration
        for shuriken in attacker.shurikens[:]:
            
            # Check if the current shuriken collides with the target's rectangle
            if shuriken.rect.colliderect(target.rect):
                
                # Check if target is not blocking (based on player/enemy logic)
                if not self.check_block(is_player,target): 
                    
                    # Determine type of damage based on shuriken's damage value
                    if shuriken.damage == 10:
                        target.state = "small_damage" # Light hit animation
                    else:
                        target.state = "big_damage" # Heavy hit animation
                    
                    # Set hit flag and reset animation frame for smooth transition
                    target.is_hit = True
                    target.frame = 0
                
                # Remove the shuriken after collision (whether it caused damage or was blocked)
                attacker.shurikens.remove(shuriken)
                
                # Play hit sound effect
                self.hit_sound.play()
                
    def check_block(self,is_player,target):
        """Checks if the target is currently blocking and 
        whether the block is successful or broken."""
        
        # If the target is the enemy (not the player)
        if not is_player:
            if target.state == "block" :
                target.block_count += 1 # Increase block count each time enemy blocks
                
                # Enemy can block only 2 times consecutively
                if target.block_count > 2:
                    target.health_bar.player_hit() #Take damage if block limit exceeded
                    return False  # Block failed
                
                return True  # Block successful

            # If not blocking, take damage
            if target.state != "block" :
                target.health_bar.player_hit()
                return False
            
        else:
            # For Enemy, increase hit count (used to track when to reset block)
            target.hit_count += 1 
            if target.state != "block" :
                target.health_bar.enemy_hit() # Take damage
                return False # Block failed
            
            return True # Block successful

    def game_over(self,winner):
        """Displays the winning banner and handles game over options like restart or exit."""
        
        # Select winning banner based on the winner character
        self.result= self.naruto_win if winner == "naruto" else self.sasuke_win
        
        self.battle_screen.blit(self.result,(300,100)) # Show the banner on screen
        
        # Show buttons for restart, exit, etc.
        if self.restart_button.draw(self.battle_screen):
            self.restart_game()
        
        if self.exit_button.draw(self.battle_screen) :
            self.running=False
            pygame.quit()
            sys.exit()

    def pause_game(self):
        """Draws a translucent overlay with the pause menu UI."""
        
        # Draw a semi-transparent gray overlay
        pygame.draw.rect(self.surface,(128,128,128,150),[0,0,SCREEN_WIDTH,SCREEN_HEIGHT])
        
        # Blit the overlay and pause menu onto the main screen
        self.battle_screen.blit(self.surface,(0,0))
        self.battle_screen.blit(self.pause_menu,(290,50))
        
    def restart_game(self):
        """Resets all game elements to their initial state to restart the battle."""
        
        # Reset win counters
        self.naruto.count=0
        self.sasuke.count=0
        
        # Clear all active shurikens
        self.naruto.shurikens = []
        self.sasuke.shurikens = []
        
        # Set restart and unpause
        self.restart=True
        self.paused=False
        self.running=False # Exit current loop to trigger game restart
        
