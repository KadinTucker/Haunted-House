import pygame
from pygame.locals import *
import random
import sys

pygame.init()
font = pygame.font.Font(None, 30)

wallImg = pygame.image.load('h_wall.png')
candyImg = pygame.image.load('h_candy.png')
ghostImg = pygame.image.load('h_ghost.png')
reticuleImg = pygame.image.load('h_reticule.png')
playerImg = pygame.image.load('h_player.png')

display = pygame.display.set_mode((900, 600))

def buildMatrix(size, string):
    matrix = []
    for x in range(size[0]):
        matrix.append([])
        for y in range(size[1]):
            matrix[x].append(string)
    return matrix

def generateHouse(size, cavernness):
    house = buildMatrix(size, 'wall')
    worm = ( 0 + size[0] // 2, size[1] // 2)
    wormDir = 1
    for i in range(cavernness):
        rand = random.random()
        if house[worm[0]][worm[1]] == 'wall':
            house[worm[0]][worm[1]] = None
        if rand >= 0.4 and rand <= 1:
            if wormDir == 1:
                worm = (worm[0] + 1, worm[1])
            elif wormDir == 2:
                worm = (worm[0], worm[1] + 1)
            elif wormDir == 3:
                worm = (worm[0] - 1, worm[1])
            elif wormDir == 4:
                worm = (worm[0], worm[1] - 1)
        elif rand <= 0.2 and rand >= 0:
            wormDir += 1
        elif rand >= 0.2 and rand > 0.4:
            wormDir -= 1
            
        if house[worm[0]][worm[1]] == None:
            if random.random() > 0.97:
                house[worm[0]][worm[1]] = 'candy'
            if random.random() > 0.97:
                house[worm[0]][worm[1]] = 'ghost'
        
        if wormDir >= 5:
            wormDir -= 4
        elif wormDir <= 0:
            wormDir += 4
            
        if worm[0] > len(house) - 3:
            wormDir = 3
            #worm = (2, worm[1])
        elif worm[0] < 2:
            wormDir = 1
            #worm = (len(house) - 3, worm[1])
        if worm[1] > len(house[0]) - 3:
            wormDir = 4
            #worm = (worm[0], 2)
        elif worm[1] < 2:
            wormDir = 2
            #worm = (worm[0], len(house) - 3)
    return house
    
def displayHouse(display, house):
    for x in range(len(house)):
        for y in range(len(house[x])):
            if house[x][y] == 'wall':
                display.blit(wallImg, (x*25, y*25))
            elif house[x][y] == 'candy':
                display.blit(candyImg, (x*25, y*25))
            elif house[x][y] == 'ghost':
                display.blit(ghostImg, (x*25, y*25))
                
def displayHazeLayer(display, hazeLayer):
    black = pygame.image.load('h_haze.png')
    for x in range(len(hazeLayer)):
        for y in range(len(hazeLayer[x])):
            if hazeLayer[x][y]:
                display.blit(black, (x*25, y*25))
                
def displayButtons(display, time, score):
    display.blit(pygame.image.load('h_b_move.png'), (750, 0))
    display.blit(pygame.image.load('h_b_scout.png'), (750, 75))
    display.blit(pygame.image.load('h_b_take.png'), (750, 150))
    display.blit(pygame.image.load('h_time.png'), (0, 0))
    display.blit(font.render(str(time), True, (255, 0, 0)), (75, 2))
    display.blit(pygame.image.load('h_score.png'), (610, 0))
    display.blit(font.render(str(score), True, (255, 0, 0)), (685, 2))
    
def displayPlayer(display, player, activeTile):
    display.blit(playerImg, (player[0]*25, player[1]*25))
    display.blit(reticuleImg, (activeTile[0]*25, activeTile[1]*25))

def death():
    snd = pygame.mixer.Sound('dundundun.wav')
    snd.play()
    clock = pygame.time.Clock()
    clock.tick(0.3)
    return True
            
house = generateHouse((30, 24), 800)
hazeLayer = buildMatrix((30, 24), True)    
player = (15, 12)   
activeTile = (15, 12) 

hazeLayer[player[0]][player[1]] = False
time = 200
score = 0

dead = False
                
while not dead:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                activeTile = (player[0], player[1] - 1)
            elif event.key == K_a or event.key == K_LEFT:
                activeTile = (player[0] - 1, player[1])
            elif event.key == K_s or event.key == K_DOWN:
                activeTile = (player[0], player[1] + 1)
            elif event.key == K_d or event.key == K_RIGHT:
                activeTile = (player[0] + 1, player[1])

            elif event.key == K_q:
                time -= 1
                if house[activeTile[0]][activeTile[1]] == 'ghost':
                    hazeLayer[activeTile[0]][activeTile[1]] = False
                    display.blit(ghostImg, (activeTile[0]*25, activeTile[1]*25))
                    pygame.display.update()
                    dead = death()
                elif house[activeTile[0]][activeTile[1]] != 'wall':
                    hazeLayer[activeTile[0]][activeTile[1]] = False
                    player = activeTile
                else:
                    hazeLayer[activeTile[0]][activeTile[1]] = False
            elif event.key == K_e:
                time -= 1
                hazeLayer[activeTile[0]][activeTile[1]] = False
            elif event.key == K_r:
                time -= 1
                if house[activeTile[0]][activeTile[1]] == 'candy' or house[player[0]][player[1]] == 'candy':
                    score += 1
                    house[activeTile[0]][activeTile[1]] = None
                    house[player[0]][player[1]] = None
            
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse = pygame.mouse.get_pos()
                if mouse[0] >= 750 and mouse[0] <= 900:
                    if mouse[1] >= 0 and mouse[1] <= 50:
                        time -= 1
                        if house[activeTile[0]][activeTile[1]] == 'ghost':
                            hazeLayer[activeTile[0]][activeTile[1]] = False
                            display.blit(ghostImg, (activeTile[0]*25, activeTile[1]*25))
                            pygame.display.update()
                            dead = death()
                            break
                        elif house[activeTile[0]][activeTile[1]] != 'wall':
                            hazeLayer[activeTile[0]][activeTile[1]] = False
                            player = activeTile
                        else:
                            hazeLayer[activeTile[0]][activeTile[1]] = False
                    elif mouse[1] >= 75 and mouse[1] <= 125:
                        time -= 1
                        hazeLayer[activeTile[0]][activeTile[1]] = False
                    elif mouse[1] >= 125 and mouse[1] <= 275:
                        time -= 1
                        if house[activeTile[0]][activeTile[1]] == 'candy' or house[player[0]][player[1]] == 'candy':
                            score += 1
                            house[activeTile[0]][activeTile[1]] = None
                            house[player[0]][player[1]] = None
                        elif house[activeTile[0]][activeTile[1]] == 'ghost':
                            dead = death()
                            break
    display.fill((150, 150, 150))
    displayHouse(display, house)
    displayHazeLayer(display, hazeLayer)
    displayPlayer(display, player, activeTile)
    displayButtons(display, time, score)
    pygame.display.update()
    if time <= 0:
        dead = death()

font = pygame.font.Font(None, 48)

while True:
    display.blit(pygame.image.load('h_gameover.png'), (0,0))
    display.blit(font.render(str(score), True, (255, 0, 0)), (850, 515))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
