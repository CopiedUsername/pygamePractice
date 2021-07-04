# Import the pygame module
from operator import gt

from pygame.locals import *
import math
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((0, 0, 255))
        self.healthBG = pygame.Surface((20, 8))
        self.healthBG.fill((255, 255, 255))
        self.healthBar = pygame.Surface((15, 5))
        self.healthBar.fill((0, 255, 0))
        self.rect = self.surf.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.velocity = 2
        self.mass = 1
        self.isjump = 0

        self.rectHBG = self.healthBG.get_rect(center=(self.rect.x + 12, self.rect.y - 20))
        self.rectH = self.healthBar.get_rect(center=(self.rect.x + 12, self.rect.y - 20))

    # Move the sprite based on user keypresses
    def getX(self):
        return self.rect.x
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.isjump = 1
        if pressed_keys[K_LEFT]:
            self.rectH.move_ip(-10,0)
            self.rectHBG.move_ip(-10,0)
            self.rect.move_ip(-10,0)
        if pressed_keys[K_RIGHT]:
            self.rectH.move_ip(10, 0)
            self.rectHBG.move_ip(10, 0)
            self.rect.move_ip(10,0)
        if pressed_keys[K_a]:
            self.attacking = 1

        if self.isjump == 1:
            # Calculate force (F). F = 0.5 * mass * velocity^2.
            if self.velocity > 0:
                F = (0.5 * self.mass * (self.velocity * self.velocity))
            else:
                F = -(0.5 * self.mass * (self.velocity * self.velocity))

            # Change position
            self.rectH.y -= F
            self.rectHBG.y -= F
            self.rect.y = self.rect.y - F

            # Change velocity
            self.velocity = self.velocity - 1

            # If ground is reached, reset variables.
            if self.rect.y >= 500:
                self.rect.y = 500
                self.rectH.y = 480
                self.rectHBG.y = 480
                self.isjump = 0
                self.velocity = 8

            if self.rect.y <= 0:
                self.rect.y = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.healthBG = pygame.Surface((45, 8))
        self.healthBG.fill((255, 255, 255))
        self.healthBar = pygame.Surface((40, 5))
        self.healthBar.fill((0, 255, 0))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.health = 100
        self.isjump = 0
        self.velocity = 2
        self.mass = 1
        # self.surf = pygame.transform.scale(self.surf, (116,48))
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = 500
        self.rectHBG = self.healthBG.get_rect(center=(self.rect.x + 20, self.rect.y - 20))
        self.rectH = self.healthBar.get_rect(center=(self.rect.x + 20, self.rect.y - 20))
        self.speed = random.randint(2, 4)

    def getHealth(self):
        return self.health
    def getX(self):
        return self.rect.x
    def hurt(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.kill()
        else:
            self.healthBar = pygame.Surface((int((40 / 100) * self.health), 5))
            self.healthBar.fill((0, 255, 0))
            #self.surf = None
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, direction):
        #self.rect.move_ip(self.speed, 0)
        if self.rect.right < 0:
            self.rect.x = 0
        if self.rect.x > 800:
            self.rect.x = 800

        if direction == 'left':
            self.rect.move_ip(3, 0)
            self.rectH.move_ip(3,0)
            self.rectHBG.move_ip(3,0)
        else:
            self.rect.move_ip(-3, 0)
            self.rectH.move_ip(-3, 0)
            self.rectHBG.move_ip(-3, 0)
        # if self.rect.right < 0:
        #     self.kill()

        if self.health <= 0:
            self.kill()

        roll = random.randint(0,100)

        if roll == 3:
            self.isjump = 1

        if self.isjump == 1:
            # Calculate force (F). F = 0.5 * mass * velocity^2.
            if self.velocity > 0:
                F = (0.5 * self.mass * (self.velocity * self.velocity))
            else:
                F = -(0.5 * self.mass * (self.velocity * self.velocity))

            # Change position
            self.rect.y = self.rect.y - F

            # Change velocity
            self.velocity = self.velocity - 1

            # If ground is reached, reset variables.
            if self.rect.y >= 500:
                self.rect.y = 500
                self.isjump = 0
                self.velocity = 8

            if self.rect.y <= 0:
                self.rect.y = 0


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 100000)

myfont = pygame.font.SysFont('Comic Sans MS', 30)

enemy = Enemy()
enemies.add(enemy)
all_sprites.add(enemy)
# Variable to keep the main loop running
running = True
collided = True

time = 0
count = 0
clock = pygame.time.Clock()
enemyHealth = 100

while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
            #if event.key == K_a:

        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.fill((0, 0, 0))
    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    #print(len(enemies))

    # Update the player sprite based on user keypresses
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        screen.blit(entity.healthBG, entity.rectHBG)
        screen.blit(entity.healthBar, entity.rectH)



    #print(player.getX())

    if pygame.sprite.spritecollideany(player,enemies) and collided == False and count >= 20:
        for enem in enemies:
            collided = True

            print("Health: ", enem.getHealth())
            count = 0
            enem.hurt(20)
            enemyHealth = enem.getHealth()
            if enemyHealth <= 0:
                enem.kill()
                enemies.empty()
                all_sprites.remove(enemy)
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
                enemyHealth = 100
            else:
                print("HIT")

    else:
        count += 1
        collided = False


    print(collided)
    print(count)
    print(enemyHealth)


    if (player.getX() >= enemy.getX()):
        enemies.update('left')
    else:
        enemies.update('right')


    #print(time)

        #print(time)
    player.update(pressed_keys)

    textsurface = myfont.render(str(int(enemyHealth)), False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))

    # Fill the screen with black

    #screen.blit(enemy.surf, enemy.rect)

    # screen.blit(player.surf, player.rect)

    pygame.display.flip()

    clock.tick(30)