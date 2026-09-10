import math
import numpy as np

def add_to_neighbors(arr,x,y,val):
  rows, cols = arr.shape[:2]
  x0,x1 = max(x-1,0),min(x+2,rows)
  y0,y1 = max(y-1,0),min(y+2,cols)
  block = arr[x0:x1,y0:y1]
  mask = np.ones(block.shape[:2],dtype=bool)
  mask[x-x0,y-y0] = False
  block[mask] += val

def get_pairs(x0,x1,y0,y1):
  result = []
  for xi in range(x0,x1+1,1):
    for yi in range(y0,y1+1,1):
      result.append((xi,yi))
  return result


def get_valid_neighbor_indices(arr,x,y):
  rows, cols = arr.shape[:2]
  x0,x1 = max(x-1,0),min(x+1,rows-1)
  y0,y1 = max(y-1,0),min(y+1,cols-1)
  result = get_pairs(x0,x1,y0,y1)
  result.remove((x,y))
  
  return result

# Guarantee that the clicked cell and neighboring cells are non-mines
# make inds mask with size of x*y - num of neighbors
# add empty cells at neighbor locations

# grid:
#  state: 0 = unopened; 1 = opened; 2 = flagged
#  numNearMines
#  hasMine: 0 = no; 1 = yes
class MinesweeperGame():
  def __init__(self,gridSizeX=10,gridSizeY=10,mineCount=1):
    # 0 = playing; 1 = won; 2 = lost; 3 = waiting to init
    self.gameState = 3
    self.gridSizeX = gridSizeX
    self.gridSizeY = gridSizeY
    self.mineCount = mineCount
    self.cellsToReveal = gridSizeX*gridSizeY - mineCount

  def init_grid(self,safeIndex=-1):
    self.gameState = 0
    safeInds = []
    if safeIndex >= 0:
      x = math.floor(safeIndex/self.gridSizeY)
      y = safeIndex%self.gridSizeY
      x0,x1 = max(x-1,0),min(x+1,self.gridSizeX-1)
      y0,y1 = max(y-1,0),min(y+1,self.gridSizeY-1)
      for i in get_pairs(x0,x1,y0,y1):
        safeInds.append((i[0] * self.gridSizeY) + i[1])

    self.grid = np.zeros((self.gridSizeX*self.gridSizeY,3), dtype=np.uint8)

    unsafeInds = np.setdiff1d(np.arange(self.gridSizeX*self.gridSizeY),list(safeInds))
    inds = np.random.choice(unsafeInds,size=self.mineCount,replace=False)

    self.grid[inds] += [np.uint8(0),np.uint8(0),np.uint8(1)]
    self.grid = self.grid.reshape((self.gridSizeX,self.gridSizeY,3))

    for ind in inds:
      add_to_neighbors(self.grid,math.floor(ind/self.gridSizeY),ind%self.gridSizeY,[np.uint8(0),np.uint8(1),np.uint8(0)])
    
    self.reveal_cell(math.floor(safeIndex/self.gridSizeY),safeIndex%self.gridSizeY)

  def reveal_cell(self,x,y):
    gridCell = self.grid[x,y]
    if not gridCell[0] == 1:
      gridCell[0] = 1
      if gridCell[2] == 1:
        print('Lost')
        self.gameState = 2
      else:
        self.cellsToReveal -= 1
        if gridCell[1] == 0:
          for iPair in get_valid_neighbor_indices(self.grid,x,y):
            self.reveal_cell(iPair[0],iPair[1])
        if self.cellsToReveal <= 0:
          print('Won')
          self.gameState = 1
      
  def toggle_flag(self,x,y):
    if not (self.grid[x,y,0] == 1):
      self.grid[x,y,0] = 2 - self.grid[x,y,0]
