import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption('Space Invader')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

player_img = pygame.image.load('player.png')
x = 350
y = 500
change = 0

enemy_img = []
enem_x = []
enem_y = []
enem_change_x = []
enem_change_y = []
num_enemies = 6

for i in range(num_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enem_x.append(random.randint(1, 735))
    enem_y.append(random.randint(100, 250))
    enem_change_x.append(0.3)
    enem_change_y.append(45)

bullet = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 500
bullet_change_y = 1
state = "Ready"

background = pygame.image.load('background.jpg')
mixer.music.load("background.wav")
mixer.music.play(-1)

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global state
    state = "Fire"
    screen.blit(bullet, (x+16, y+16))

def is_collision(enem_x, enem_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enem_x - bullet_x, 2) + math.pow(enem_y - bullet_y, 2))
    if distance <= 32:
        return True
    else:
        return False

score_value = 0
score_x = 10
score_y = 10
font = pygame.font.SysFont('Comic Sans MS', 30)
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def show_over():
    game_over = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over, (300, 400))

running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for item in pygame.event.get():
        if item.type == pygame.QUIT:
            running = False

        if item.type == pygame.KEYDOWN:
            if item.key == pygame.K_RIGHT:
                change += 0.4
            if item.key == pygame.K_LEFT:
                change -= 0.4
            if item.key == pygame.K_SPACE:
                if state == 'Ready':
                    laser_sound = mixer.Sound("laser.wav")
                    laser_sound.play()
                    bullet_x = x
                    fire_bullet(bullet_x, bullet_y)

        if item.type == pygame.KEYUP:
            if item.key == pygame.K_RIGHT or item.key == pygame.K_LEFT:
                change = 0

    x += change
    if x <= 0:
        x = 0
    if x >= 736:
        x = 736

    for i in range(num_enemies):
        if enem_y[i] >= 450:
            for j in range(num_enemies):
                enem_y[j] = 2000
            show_over()
            break

        enem_x[i] += enem_change_x[i]
        if enem_x[i] <= 0:
            enem_change_x[i] = 0.3
            enem_y[i] += enem_change_y[i]
        if enem_x[i] >= 736:
            enem_change_x[i] = -0.3
            enem_y[i] += enem_change_y[i]

        collision = is_collision(enem_x[i], enem_y[i], bullet_x, bullet_y)
        if collision:
            explode = mixer.Sound("explosion.wav")
            explode.play()
            state = 'Ready'
            bullet_y = 500
            score_value += 1
            enem_x[i] = random.randint(1, 735)
            enem_y[i] = random.randint(100, 250)

        draw_enemy(enem_x[i], enem_y[i], i)

    if bullet_y <= 0:
        bullet_y = 500
        state = 'Ready'

    if state == "Fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_change_y


    draw_player(x, y)
    show_score(score_x, score_y)
    pygame.display.update()

