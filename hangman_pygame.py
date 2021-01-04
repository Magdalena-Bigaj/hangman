import json
import pygame
import random
import math
import numpy as np


pygame.init()
win = WIDTH, HEIGHT = 1150, 680
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("H-A-N-G-M-A-N  G-A-M-E!")

RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 500
A = 97
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    print(i%13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

LETTER_FONT = pygame.font.SysFont('arial', 32)
WORD_FONT = pygame.font.SysFont('arial', 45)
TITLE_FONT = pygame.font.SysFont('arial', 40)

images = []
for i in range(1, 7):
    image = pygame.image.load('yoda_' + str(i) + ".jpg")
    images.append(image)

hangman_status = 0
data = json.load(open("words.json"))
word = (random.choice(data))
guessed = []

BLACK= (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = '#033b6b'



def draw():
    win.fill(WHITE)
    pygame.draw.rect(win, BLUE, pygame.Rect(10, 10, 1130, 662), 2)
    pygame.display.update()

    text = TITLE_FONT.render("HANGMAN GAME", 1, BLUE)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 15))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (590, 240))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLUE, (x, y), RADIUS, 1)
            text = LETTER_FONT.render(ltr, 1, BLUE)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    win.blit(images[hangman_status], (50, 85))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLUE)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("Bingo! You guessed it !")
            break

        if hangman_status == 5:
            display_message(f"Sorry!! You loose.... The word is:  {word}")
            break


while True:
    main()
pygame.quit()
