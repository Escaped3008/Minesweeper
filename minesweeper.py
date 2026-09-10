import pygame
import minesweeper_module as ms
import numpy as np
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def load_image(name):
  path = os.path.join(BASE_DIR,'Images',name)
  return pygame.image.load(path)

gridSizeX = 22
gridSizeY = 12

msGame = ms.MinesweeperGame(gridSizeX,gridSizeY,40)
cellSize = 50
cellBorderWidth = 4

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

backColor = (48,48,48)

tile_image = load_image('minesweeper-tile.png').convert()
tile_image = pygame.transform.scale(tile_image,(cellSize,cellSize))
tile_dark_image = load_image('minesweeper-tile-dark.png').convert()
tile_dark_image = pygame.transform.scale(tile_dark_image,(cellSize+cellBorderWidth,cellSize+cellBorderWidth))

flag_dark_image = load_image('minesweeper-flag-dark.png').convert()
flag_dark_image = pygame.transform.scale(flag_dark_image,(cellSize+cellBorderWidth,cellSize+cellBorderWidth))

mine_image = load_image('minesweeper-mine.png').convert_alpha()
mine_image = pygame.transform.scale(mine_image,(cellSize,cellSize))

backTileGrid = [pygame.Rect(x,y,cellSize,cellSize) for x in range(cellBorderWidth,(cellSize+cellBorderWidth) * gridSizeX,cellSize+cellBorderWidth) for y in range(cellBorderWidth,(cellSize+cellBorderWidth) * gridSizeY,cellSize+cellBorderWidth)]
backTileColor = (70,70,70)

numImages = []
for i in range(8):
  numImg = load_image(f'minesweeper-{i+1}.png').convert_alpha()
  numImg = pygame.transform.scale(numImg,(cellSize,cellSize))
  numImages.append(numImg)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN :
      pos = pygame.mouse.get_pos()
      for i,r in enumerate(backTileGrid):
        if r.collidepoint(pos):
          if event.button == 1:
            if msGame.gameState == 3:
              msGame.init_grid(i)
            else:
              msGame.reveal_cell(math.floor(i/gridSizeY),i%gridSizeY)
          elif event.button == 3:
            msGame.toggle_flag(math.floor(i/gridSizeY),i%gridSizeY)
          break
      
  screen.fill(backColor)

  for r in backTileGrid:
    pygame.draw.rect(screen,backTileColor,r)

  if msGame.gameState == 3:# waiting to init, no grid yet
    for x in range(msGame.gridSizeX):
      for y in range(msGame.gridSizeY):
        screen.blit(tile_dark_image,((cellSize+cellBorderWidth) * x,(cellSize+cellBorderWidth) * y))
  else:
    for x,y in np.ndindex((gridSizeX,gridSizeY)):
      if msGame.grid[x,y,0] == 0:
        screen.blit(tile_dark_image,((cellSize+cellBorderWidth) * x,(cellSize+cellBorderWidth) * y))
      elif msGame.grid[x,y,0] == 2:
        screen.blit(flag_dark_image,((cellSize+cellBorderWidth) * x,(cellSize+cellBorderWidth) * y))
      elif msGame.grid[x,y,2] == 1:
        screen.blit(mine_image,(cellBorderWidth + ((cellSize + cellBorderWidth) * x),cellBorderWidth + ((cellSize + cellBorderWidth) * y)))
      elif msGame.grid[x,y,0] == 1:
        cellNum = msGame.grid[x,y,1]
        if cellNum > 0:
          screen.blit(numImages[cellNum-1],(cellBorderWidth + ((cellSize + cellBorderWidth) * x),cellBorderWidth + ((cellSize + cellBorderWidth) * y)))

  pygame.display.flip()

  clock.tick(10)

pygame.quit()
