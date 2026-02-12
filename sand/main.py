import random
import pygame

pygame.init()
screenSize = (1024, 1024)
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

running = True

gridWidth, gridHeight = 128, 128
cellSize = 8
occupiedCells = set()
mouseDown = False

def addCellAtPos(pos):
    col = pos[0] // cellSize 
    row = pos[1] // cellSize
    if 0 <= col < gridWidth and 0 <= row < gridHeight:
        for targetRow in range(row, -1, -1):
            if (col, targetRow) not in occupiedCells:
                occupiedCells.add((col, targetRow))
                break

def stepSand():
    if not occupiedCells:
        return
    newOccupied = set(occupiedCells)
    cellsToProcess = sorted(occupiedCells, key=lambda cell: cell[1], reverse=True)
    for col, row in cellsToProcess:
        below = (col, row + 1)
        if row + 1 < gridHeight and below not in occupiedCells:
            newOccupied.discard((col, row))
            newOccupied.add(below)
            continue
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
    occupiedCells.clear()
    occupiedCells.update(newOccupied)
            
 
while running:
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
            
    if mouseDown:
        addCellAtPos(pygame.mouse.get_pos())

    stepSand()
    screen.fill((0, 0, 0))
    for col, row in occupiedCells:
        rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
        pygame.draw.rect(screen, (255, 255, 255), rect)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()