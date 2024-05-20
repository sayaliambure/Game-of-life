import pygame 
import numpy as np
import time

# setting colors
COLOR_BG = (10,10,10)
COLOR_GRID = (40,40,40)
COLOR_DIE_NEXT = (170,170,170)
COLOR_ALIVE_NEXT = (255,255,255)

# Updating the Cell States based on rules
def update(screen, cells, size, with_progress=False):
  updated_cells = np.zeros((cells.shape[0], cells.shape[1]))


  for row, col in np.ndindex(cells.shape):
    alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
    color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

    if cells[row, col] == 1:
      if alive < 2 or alive > 3:
        if with_progress:
          color = COLOR_DIE_NEXT

      elif 2 <= alive <= 3:
        updated_cells[row,col] = 1
        if with_progress:
          color = COLOR_ALIVE_NEXT

    else:
      if alive == 3:
        updated_cells[row,col] = 1
        if with_progress:
          color = COLOR_ALIVE_NEXT


    pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1))


  return updated_cells



def main():
  pygame.init()             #Initializes all Pygame modules
  screen = pygame.display.set_mode((800,600))      #The main window of the application

  cells = np.zeros((60,80))    #Initializes a 60x80 grid of cells, all set to 0 (dead)
  screen.fill(COLOR_GRID)      # Fills the screen with the grid color
  update(screen, cells, 10)    #Draws the initial state of cells

  pygame.display.flip()        #Updates the entire screen
  pygame.display.update()      #Updates portions of the screen for software displays

  running = False            #boolean variable that controls whether simulation is running

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:    #Checks if the quit event has been triggered
        pygame.quit()
        return 
      elif event.type == pygame.KEYDOWN:   #Checks if a key has been pressed
        if event.key == pygame.K_SPACE:     #Checks if the space bar has been pressed. If so, it toggles the running state
          running = not running
          update(screen, cells, 10)         #Calls the update function to redraw the screen based on the current state of the cells
          pygame.display.update()           #Updates the display with the changes

      if pygame.mouse.get_pressed()[0]:      #Checks if any mouse buttons are pressed
        pos = pygame.mouse.get_pos()         #Gets the current mouse cursor position
        cells[pos[1] // 10, pos[0] // 10] = 1    #Converts the mouse position to cell coordinates and sets the corresponding cell to 1 (alive)
        update(screen, cells, 10)
        pygame.display.update()
      
    screen.fill(COLOR_GRID)


    if running:    #Checks if the simulation is currently running
      #Updates the state of all cells based on the Game of Life rules and 
      #redraws the cells on the screen. 
      #The with_progress flag is set to True to use different colors for cells that will change state.
      
      cells = update(screen, cells, 10, with_progress=True)
      pygame.display.update()    # Updates the display with the changes
    time.sleep(0.01)



if __name__ == "__main__":
  main()