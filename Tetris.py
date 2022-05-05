import pygame
import random

# Creating the data structure for pieces
# Setting up global vars
# Functions:
    # createGrid
    # drawGrid
    # drawWindow
    # Rotating shape in main
    # Setting up the main
  
'''
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
'''

pygame.font.init()

# Global vars
sWidth = 800 # Width of the game screen
sHeight = 700 # Height of the game screen
playWidth = 300 # meaning 300 // 10 = 30 width per block
playHeight = 600 # meaning 600 // 30 = 20 height per block
blockSize = 30

topLeftX = (sWidth - playWidth) // 2
topLeftY = sHeight - playHeight

# Shape Formats
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T] # A list holding all the available shape
shapeColors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 

class Piece(object):
    rows = 20  # y
    columns = 10  # x
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shapeColors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3
      
        
def createGrid(lockedPositions = {}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)] # Create 1 list for every row in the grid
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in lockedPositions:
                c = lockedPositions[(j, i)]
                grid[i][j] = c
    
    return grid

    
def convertShapeFormat(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
                
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
        
    return positions
    
 
def validSpace(shape, grid):
    acceptedPositions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    acceptedPositions = [j for sub in acceptedPositions for j in sub]
    
    formatted = convertShapeFormat(shape) 
    
    for pos in formatted:
        if pos not in acceptedPositions:
            if pos[1] > -1:
                return False
            
    return True

    
def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    
    return False

    
# Get the random shape from the top of the game screen
def getShape():
    global shapes, shapeColors
    
    return Piece(5, 0, random.choice(shapes))


def drawTextMiddle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label, (topLeftX + playWidth / 2 - (label.get_width() / 2), topLeftY + playHeight / 2 - label.get_height() / 2))
 
    
# Draw the midnight-blue lines for the grid, not the whole grid
def drawGrid(surface, row, col):
    sX = topLeftX
    sY = topLeftY
    
    for i in range(row):
        pygame.draw.line(surface, (25,25,112), (sX, sY + i * blockSize), (sX + playWidth, sY + i * blockSize)) # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (25,25,112), (sX + j * blockSize, sY), (sX + j * blockSize, sY + playHeight)) # vertical lines

                   
def clearRows(grid, locked):
    # need to see if row is clear the shift every other row above down one
    inc = 0
    for i in range(len(grid) -1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
                
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def drawNextShape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    
    sX = topLeftX + playWidth + 50
    sY = topLeftY + playHeight / 2 - 100
    
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sX + j * blockSize, sY + i * blockSize, blockSize, blockSize), 0)
                
    surface.blit(label, (sX + 10, sY - 30))

    
def drawWindow(surface):
    # Draw a grid in medium sea green color
    surface.fill((0,0,0))
    
    # Write the title of the game
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255)) 
    
    # Location of the label
    surface.blit(label, (topLeftX + playWidth / 2 - (label.get_width() / 2), 30))
   
    # Draw the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (topLeftX + j * blockSize, topLeftY + i * blockSize, blockSize, blockSize), 0)
    
    # Draw border
    drawGrid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (topLeftX, topLeftY, playWidth, playHeight), 5)
 

def main():
    global grid
    
    lockedPositions = {}
    grid = createGrid(lockedPositions)
    
    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    fallTime = 0
    
    while run:
        fallSpeed = 0.27

        grid = createGrid(lockedPositions)
        fallTime += clock.get_rawtime()
        clock.tick()

        # Piece falling
        if fallTime / 1000 >= fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not(validSpace(currentPiece, grid)) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currentPiece.x -= 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.x += 1
                elif event.key == pygame.K_RIGHT:
                    currentPiece.x += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.x -= 1
                elif event.key == pygame.K_UP: # rotate shape
                    currentPiece.rotation = currentPiece.rotation + 1 % len(currentPiece.shape)
                    if not validSpace(currentPiece, grid):
                        currentPiece.rotation = currentPiece.rotation - 1 % len(currentPiece.shape)
                if event.key == pygame.K_DOWN: # move the shape down
                    currentPiece.y += 1
                    if not validSpace(currentPiece, grid):
                        currentPiece.y -= 1
                            
        shapePos = convertShapeFormat(currentPiece)
        
        # Add piece to the grid for drawing
        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.color
        
        # When piece hits the ground
        if changePiece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                lockedPositions[p] = currentPiece.color
            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False
            #score += clearRows(grid, lockedPositions) * 10
            clearRows(grid, lockedPositions)    

        drawWindow(win)
        drawNextShape(nextPiece, win)  
        pygame.display.update()
        
        # Check if the user has lost
        if checkLost(lockedPositions):
            run = False
    
    drawTextMiddle("You Lost!", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)
            
                    
def mainMenu():
    run = True
    while run:
        win.fill((0, 0, 0))
        drawTextMiddle("Press Any Key To Play", 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
                     
    pygame.quit()
    
win = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption('Tetris')

mainMenu()  # start game