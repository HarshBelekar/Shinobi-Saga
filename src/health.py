import pygame # type: ignore

class HealthBar:
    def __init__(self,icon,x,y):
        # Initialize the health bar with an icon and position
        self.icon=icon
        self.x=x
        self.y=y
        self.hitbox=(self.x +10 ,self.y +5 ,80,80) # Rect area around icon (can be used for collisions or UI)
        self.health=200 # Initial health value
        self.damage = 0 # Amount of damage taken (used to offset enemy health bar position)
    
    def player_bar(self,surface):
        # Draw the player's health bar and icon on the screen
        surface.blit(self.icon, (10, 10))  # Draw the player's icon at the top-left
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)  # Update hitbox (if needed for detection later)

        # Draw the red background (full bar)
        pygame.draw.rect(surface, (255, 0, 0), (87, 38, 202, 25))

        # Draw the green bar (remaining health)
        pygame.draw.rect(surface, (0, 255, 0), (89, 43, self.health, 15))
    
    def enemy_bar(self,surface):
        # Draw the enemy's health bar and icon on the screen
        surface.blit(self.icon, (910, 10))  # Draw enemy icon at the top-right
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)  # Update hitbox

        # Draw the red background (full bar)
        pygame.draw.rect(surface, (255, 0, 0), (710, 38, 202, 25))

        # Draw the green bar (remaining health) that shrinks from right to left
        pygame.draw.rect(surface, (0, 255, 0), (710 + self.damage, 43, self.health, 15))

    def player_hit(self):
        # Reduce player health by 10 (used when player gets hit)
        if self.health > 0:
            self.health -= 10
        elif self.health < 0:
            self.health = 0  # Prevent health from going negative

    def enemy_hit(self):
        # Reduce enemy health by 10 and increase the damage offset (moves the green bar left)
        if self.health > 0:
            self.health -= 10
            self.damage += 10
        elif self.health < 0:
            self.health = 0  # Prevent health from going negative
