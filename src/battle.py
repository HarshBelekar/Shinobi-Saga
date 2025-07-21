import pygame # type: ignore
import sys
import button
import player
import enemy

# ----------------- Game Settings -----------------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# ----------------- Assets Paths -----------------
BG = "assets/images/background/bg.png"
UI_PATH = "assets/images/ui/pause_menu/"
BANNERS_PATH = "assets/images/ui/banners/"

class Battle:
    
    def __init__(self):
        # Initialize Pygame and set up display
        pygame.init()
        self.battle_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        pygame.display.set_caption("Shinobi Saga - Battle")
        self.clock = pygame.time.Clock()
        
        # ----------------- Load Assets -----------------
        # Background & Pause Menu UI
        try:
            self.bg=pygame.image.load(BG).convert_alpha()
            self.pause_menu=pygame.image.load(UI_PATH + "pause_menu.png").convert_alpha()
            self.pause_img=pygame.image.load(UI_PATH + "pause_button.png").convert_alpha()
            self.resume_img=pygame.image.load(UI_PATH + "resume_button.png").convert_alpha()
            self.restart_img=pygame.image.load(UI_PATH + "restart_button.png").convert_alpha()
            self.exit_img=pygame.image.load(UI_PATH + "exit1_button.png").convert_alpha()
            self.home_img=pygame.image.load(UI_PATH + "home_button.png").convert_alpha()
            self.naruto_win=pygame.image.load(BANNERS_PATH + "naruto_wins.png").convert_alpha()
            self.sasuke_win=pygame.image.load(BANNERS_PATH + "sasuke_wins.png").convert_alpha()
            
        except Exception as e:
            print("Error loading images:", e)
        
        # ----------------- Load Sound -----------------
        self.click=pygame.mixer.Sound("assets/sounds/click.wav")
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
                self.pause_game()
                
                if self.resume_button.draw(self.battle_screen):
                    self.paused=False
            
                if self.restart_button.draw(self.battle_screen):
                    self.restart_game()
                
                if self.exit_button.draw(self.battle_screen):
                    self.running=False
                    pygame.quit()
                    sys.exit()
                
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
        else:
            if self.restart:
                self.run_game()
    
    def handle_character_logic(self, character, opponent, is_player=True):
        """ Handles movement, shuriken updates, physics, health, and state. """
        
        if character.health_bar.health > 0 and not self.paused:
            if opponent.health_bar.health > 0:
                # Handle input or enemy AI
                if is_player:
                    character.handle_input(pygame.key.get_pressed())
                else:
                    character.move_enemy()
            else:
                # Opponent defeated
                character.state = "stand"
                opponent.count += 1
                self.game_over("naruto" if is_player else "sasuke")
        elif character.health_bar.health == 0:
            character.state = "defeated"
        else:
            character.state = "stand"

        # Apply physics and draw character
        character.apply_physics()
        character.draw(self.battle_screen)
        
        # Update shurikens only if not paused
        if not self.paused:
            character.update_shurikens(self.battle_screen)
        
        # Draw health bar
        character.display_health(self.battle_screen)
        
        # Check for shuriken hit collisions
        self.check_damage(character, opponent)

    def check_damage(self,player,enemy):
        """ Checks if any player shuriken collides with enemy. """
    
        for shuriken in player.shurikens[:]:
            if shuriken.rect.colliderect(enemy.rect):
                enemy.health_bar.enemy_hit()  # Reduce health
                player.shurikens.remove(shuriken)

                self.hit_sound.play()

    def game_over(self,winner):
        """ Displays win banner and handles game over buttons """
        
        self.result= self.naruto_win if winner == "naruto" else self.sasuke_win
        self.battle_screen.blit(self.result,(300,100))
        
        if self.restart_button.draw(self.battle_screen):
            self.restart_game()
        
        if self.exit_button.draw(self.battle_screen) :
            self.running=False
            pygame.quit()
            sys.exit()

    def pause_game(self):
        """ Draws semi-transparent overlay and pause menu. """
        
        pygame.draw.rect(self.surface,(128,128,128,150),[0,0,SCREEN_WIDTH,SCREEN_HEIGHT])
        self.battle_screen.blit(self.surface,(0,0))
        self.battle_screen.blit(self.pause_menu,(290,50))
        
    def restart_game(self):
        """ Resets game state for restart. """
        
        self.naruto.count=0
        self.sasuke.count=0
        self.naruto.shurikens = []
        self.sasuke.shurikens = []
        self.restart=True
        self.paused=False
        self.running=False
        
