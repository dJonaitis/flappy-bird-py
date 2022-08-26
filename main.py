from tkinter import W
import pygame
import sys
import random

random.seed()
clock = pygame.time.Clock()


pygame.init()
font = pygame.font.Font('assets/upheavtt.ttf', 50)

width, height = 500, 800
birdWidth = 34 * 2
birdHeight = 24 * 2
pipeSpacing = 150

pSpriteIndex = 1


class Pipes:
    def __init__(self, gap, xOffset):
        #width, height of pipe sprite = 104, 640
        self.gap = gap
        self.sprite = pygame.image.load('assets/pipe.png').convert()
        self.sprite = pygame.transform.scale2x(self.sprite)
        self.topSprite = pygame.transform.rotate(self.sprite, 180)
        self.xOffset = xOffset
        self.x = 300 + self.xOffset
        self.y = random.randrange(300, 600, 1)
        self.topY = self.y - self.gap - 640
        self.rect = pygame.Rect(self.x, self.y, 104, 640)
        self.rectTop = pygame.Rect(self.x, self.topY, 104, self.topY + 640)
    
    def draw(self):
        window.blit(self.sprite, (self.x, self.y))
        window.blit(self.topSprite, (self.x, self.y - self.gap - 640))

class Bird: 
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.gravity = 0.25
        self.velocity = 0
        self.x = x
        self.y = y
        self.terminalV = 2
        self.sprites = ['assets/bird1.png', 'assets/bird2.png', 'assets/bird3.png']
        self.jumpForce = -7
        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def fall(self):
        self.velocity += self.gravity
    
    def draw(self):
        if self.alive:
            window.blit(birdSprite, ())

    def checkCollision(self, pipeList):
        if self.rect.top <= -100 or self.rect.bottom >= groundY:
            return True
        j = 0
        for i in pipeList:
            j += 1
            #validity of collision
            if (self.rect.right >= i.x and self.rect.left <= i.x + 104) and ((self.rect.top <= i.rect.top - i.gap) or (self.rect.bottom >= i.y)):
                    return True
    

player = Bird(birdWidth, birdHeight, 100, 400)


window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

background = pygame.image.load('assets/bg.png').convert()
background = pygame.transform.scale2x(background)

ground = pygame.image.load('assets/base.png').convert()
ground = pygame.transform.scale2x(ground)
groundX = 0
groundY = 700

birdSprite = pygame.image.load(player.sprites[pSpriteIndex]).convert()
birdSprite = pygame.transform.scale(birdSprite, (birdWidth, birdHeight))

def drawFloor(groundX, groundY):
    window.blit(ground, (groundX, groundY))
    window.blit(ground, (groundX + 336, groundY))

def createPipe(gap, pipeList):
    if len(pipeList) > 0:
        xOffset = (len(pipeList) * pipeSpacing) + 104 * len(pipeList)
    else:
        xOffset = 0
    return Pipes(gap, xOffset)   




def main(window):
    run = True
    quit = False
    done = None
    pipeList = []

    for i in range (1, 11):
        pipeList.append(createPipe(200, pipeList))
    


    
    distanceTravelled = 0
    while run:
        global pSpriteIndex
        global birdSprite
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = False
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                player.velocity = player.jumpForce
                if pSpriteIndex < 2: 
                    pSpriteIndex += 1
                else:
                    pSpriteIndex = 0
                birdSprite = pygame.image.load(player.sprites[pSpriteIndex]).convert()
                birdSprite = pygame.transform.scale(birdSprite, (birdWidth, birdHeight))
        
        if player.velocity < player.terminalV:
            player.velocity += player.gravity
            
       
        
        player.y += player.velocity

        #background
        window.blit(background, (0, -100))
        
        #pipe
        for i in pipeList:
            i.draw()
            i.x -= 1
            if i.x <= -100:
                pipeList.append(createPipe(350, pipeList))
                pipeList.pop(0)


        #ground
        global groundX
        groundX -= 1        
        drawFloor(groundX, groundY)
        if groundX <= -336:
            groundX = 0


        #bird
        window.blit(birdSprite, (player.x, player.y))
        player.rect = pygame.Rect(player.x, player.y, player.width, player.height)
        if player.checkCollision(pipeList):
            run = False

        #score
        scoreContent = f"Score: {distanceTravelled}"
        scoreText = font.render(scoreContent, True, (255, 255, 255))
        window.blit(scoreText, (30, 30))

        distanceTravelled += 1

        

        pygame.display.update()
        clock.tick(120)
    
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                pygame.quit()
                sys.exit()

        pygame.display.update()
        window.blit(background, (0, -100))
        scorecard = pygame.image.load('assets/scorecard.png').convert_alpha()
        scorecard = pygame.transform.scale(scorecard, (375, 300))
        window.blit(scorecard, (62, 200))        
        finalScoreText = font.render(str(distanceTravelled), True, (0, 0, 0))
        window.blit(finalScoreText, (288, 325))


main(window)