# Import the pygame module
from operator import gt

from pygame.locals import *
import math
import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
            if self.velocity > 0:
                F = (0.5 * self.mass * (self.velocity * self.velocity))
            else:
                F = -(0.5 * self.mass * (self.velocity * self.velocity))

            self.rectH.y -= F
            self.rectHBG.y -= F
            self.rect.y = self.rect.y - F

            self.velocity = self.velocity - 1

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

    def update(self, direction):
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

        if self.health <= 0:
            self.kill()

        roll = random.randint(0,100)

        if roll == 3:
            self.isjump = 1

        if self.isjump == 1:
            if self.velocity > 0:
                F = (0.5 * self.mass * (self.velocity * self.velocity))
            else:
                F = -(0.5 * self.mass * (self.velocity * self.velocity))

            self.rect.y = self.rect.y - F

            self.velocity = self.velocity - 1

            if self.rect.y >= 500:
                self.rect.y = 500
                self.isjump = 0
                self.velocity = 8

            if self.rect.y <= 0:
                self.rect.y = 0


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
running = True
collided = True

time = 0
count = 0
clock = pygame.time.Clock()
enemyHealth = 100

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    screen.fill((0, 0, 0))
    pressed_keys = pygame.key.get_pressed()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        screen.blit(entity.healthBG, entity.rectHBG)
        screen.blit(entity.healthBar, entity.rectH)

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

    player.update(pressed_keys)

    textsurface = myfont.render(str(int(enemyHealth)), False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))

    pygame.display.flip()

    clock.tick(30)