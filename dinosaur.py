import pygame
import os
from math import *
from random import randint

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((800, 400))
background = pygame.image.load("dino_back.png")
pygame.display.set_caption("Dino Rush")  # Title
icon = pygame.image.load("dinosaur.png")
pygame.display.set_icon(icon)

cact = pygame.image.load("cactus1.png")
pause = pygame.image.load("pause.png")
play = pygame.image.load("play.png")

player1 = pygame.image.load("dino21.png")
player2 = pygame.image.load("dino22.png")

dino = pygame.image.load("dinosaur1.png")
counter = 1

scroll_sound = pygame.mixer.Sound("click2.wav")
jump_sound = pygame.mixer.Sound("jump2.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")


def player(x, y, state):
    global counter
    if counter <= 6 and state == "play":
        screen.blit(player1, (x, y))
    else:
        screen.blit(player2, (x, y))
    counter += 1
    if counter == 12:
        counter = 1


def cactus(x, y):
    screen.blit(cact, (x, y))


def collision(x1, y1, x2, y2):
    d = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    if d < 60:
        return True
    else:
        return False


def game_over():
    font1 = pygame.font.SysFont("comicsansms.ttf", 70)
    over = font1.render("GAME OVER!!", True, (0, 0, 0))
    go = True
    while go:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
        screen.blit(over, (225, 50))

        font = pygame.font.SysFont("comicsansms.ttf", 38)
        pygame.draw.rect(screen, (255, 255, 255), (170, 300, 140, 30))
        pygame.draw.rect(screen, (255, 255, 255), (570, 300, 80, 30))

        color = (0, 0, 0)
        color1 = (0, 0, 0)
        mouse = pygame.mouse.get_pos()

        if 170 < mouse[0] < 310 and 300 < mouse[1] < 330:
            color = (0, 200, 20)

        if 570 < mouse[0] < 650 and 300 < mouse[1] < 330:
            color1 = (0, 200, 20)

        restart = font.render("Play again", True, color)
        screen.blit(restart, (178, 305))

        end = font.render("Quit", True, color1)
        screen.blit(end, (583, 305))

        if color == (0, 200, 20) and (1, 0, 0) == pygame.mouse.get_pressed():
            scroll_sound.play()
            game_loop()
            break
        if color1 == (0, 200, 20) and (1, 0, 0) == pygame.mouse.get_pressed():
            scroll_sound.play()
            pygame.quit()
            break

        pygame.display.update()


def show_score(score):
    font = pygame.font.SysFont("comicsansms.ttf", 30)
    score1 = font.render("Score : " + str(score), True, (0, 0, 0))
    screen.blit(score1, (650, 10))


def game_loop():
    isJump = False
    jumpcount = 18
    velx = 8
    cactusx = 900
    cactusy = 160
    playerx = 250
    playery = 175

    color = (255, 255, 255)
    score = 0
    running = True
    state = "play"

    while running:
        pygame.time.delay(11)

        screen.fill((255, 255, 255))  # RGB
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scroll_sound.play()
                    if state == "play":
                        state = "pause"
                    else:
                        state = "play"
                    break
                if event.key == pygame.K_SPACE and state == "play":
                    jump_sound.play()
                    isJump = True

        player(playerx, playery, state)
        cactus(cactusx, cactusy)
        show_score(score)

        if state == "pause":
            pygame.draw.rect(screen, color, (10, 10, 32, 32))
            screen.blit(play, (10, 10))

        if state == "play":

            pygame.draw.rect(screen, color, (10, 10, 32, 32))
            screen.blit(pause, (10, 10))

            col = collision(playerx, playery, cactusx, cactusy)
            if col:
                explosion_sound.play()
                pygame.draw.rect(screen, (255, 255, 255), (10, 10, 32, 32))
                game_over()
                break

            if 0 < cactusx <= 2000:
                cactusx -= velx
            elif cactusx <= 0:
                cactusx = randint(800, 2000)
                score += 1
                if score >= 5 and score % 5 == 0:
                    velx += 1

            if isJump:
                if jumpcount >= -18:
                    playery -= jumpcount
                    jumpcount -= 1

                else:
                    isJump = False
                    jumpcount = 18

        pygame.display.update()


def intro_screen():
    intro = True

    while intro:

        screen.fill((255, 255, 255))
        screen.blit(dino, (400, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
        font = pygame.font.SysFont("comicsansms.ttf", 35)
        pygame.draw.rect(screen, (255, 255, 255), (200, 150, 80, 30))
        pygame.draw.rect(screen, (255, 255, 255), (200, 190, 80, 30))

        color = (0, 0, 0)
        color1 = (0, 0, 0)
        mouse = pygame.mouse.get_pos()

        if 200 < mouse[0] < 280 and 150 < mouse[1] < 180:
            color = (0, 200, 20)

        if 200 < mouse[0] < 280 and 190 < mouse[1] < 220:
            color1 = (0, 200, 20)

        start = font.render("Start", True, color)
        screen.blit(start, (210, 154))

        end = font.render("Quit", True, color1)
        screen.blit(end, (210, 194))

        font1 = pygame.font.SysFont("comicsansms.ttf", 30)

        space = font1.render("Jump - Space bar", True, (0, 0, 0))
        screen.blit(space, (10, 340))

        enter = font1.render("Pause - Enter", True, (0, 0, 0))
        screen.blit(enter, (10, 370))

        if color == (0, 200, 20) and (1, 0, 0) == pygame.mouse.get_pressed():
            scroll_sound.play()
            game_loop()
            break
        if color1 == (0, 200, 20) and (1, 0, 0) == pygame.mouse.get_pressed():
            scroll_sound.play()
            pygame.quit()
            break

        pygame.display.update()


intro_screen()
