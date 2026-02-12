import random
import pygame

pygame.init()  # Start up the pygame system
screenSize = (1024, 1024)  # Size of the window in pixels
screen = pygame.display.set_mode(screenSize)  # Create the window
clock = pygame.time.Clock()  # Keeps the game loop at a steady speed

running = True  # Main loop switch

gridWidth, gridHeight = 128, 128  # Grid size in cells
cellSize = 8  # Size of each cell in pixels
occupiedCells = set()  # Set of (col, row) cells that have sand
mouseDown = False  # Track whether the left mouse button is held

def addCellAtPos(pos):
    # Convert mouse position in pixels into a grid cell
    col = pos[0] // cellSize
    row = pos[1] // cellSize
    if 0 <= col < gridWidth and 0 <= row < gridHeight:
        # Drop the new sand straight down until it hits another grain
        for targetRow in range(row, -1, -1):
            if (col, targetRow) not in occupiedCells:
                occupiedCells.add((col, targetRow))
                break

def stepSand():
    # Move each grain of sand one step if it can fall or slide
    if not occupiedCells:
        return
    newOccupied = set(occupiedCells)  # Copy so we can update safely
    # Process from bottom to top so lower grains move first
    cellsToProcess = sorted(occupiedCells, key=lambda cell: cell[1], reverse=True)
    for col, row in cellsToProcess:
        below = (col, row + 1)
        # Try to fall straight down
        if row + 1 < gridHeight and below not in occupiedCells:
            newOccupied.discard((col, row))
            newOccupied.add(below)
            continue
        # If blocked, try to slide down-left or down-right
        directions = [(-1, 1), (1, 1)]
        random.shuffle(directions)
        moved = False
        for dx, dy in directions:
            newCol = col + dx
            newRow = row + dy
            if 0 <= newCol < gridWidth and newRow < gridHeight:
                if (newCol, newRow) not in occupiedCells:
                    newOccupied.discard((col, row))
                    newOccupied.add((newCol, newRow))
                    moved = True
                    break
        if moved:
            continue
    # Replace the old set with the updated positions
    occupiedCells.clear()
    occupiedCells.update(newOccupied)
            
 
while running:
    # Handle input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseDown = True
                addCellAtPos(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouseDown = False
        if event.type == pygame.MOUSEMOTION and mouseDown:
            addCellAtPos(event.pos)
            
    # Keep adding sand while the mouse is held down
    if mouseDown:
        addCellAtPos(pygame.mouse.get_pos())

    # Update simulation
    stepSand()
    # Draw everything
    screen.fill((0, 0, 0))
    for col, row in occupiedCells:
        rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
        pygame.draw.rect(screen, (255, 255, 255), rect)
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second
pygame.quit()  # Close game when not running