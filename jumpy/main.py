import pygame
import colorsys
from maps import *

pygame.init()

# Create window
# 64 x 64 squares
# 16 x 30 grid
screen = pygame.display.set_mode((1920, 1024))
clock = pygame.time.Clock()

# Create character
happy = pygame.image.load("jumpy/happy.png").convert_alpha()
originalCharacter = pygame.transform.scale(happy, (100, 100))
flippedCharacter = pygame.transform.flip(originalCharacter, True, False)

character = originalCharacter
image_rect = happy.get_rect()
pygame.display.set_caption("Happy Jump")
pygame.display.set_icon(happy)

# Game variables
screenWidth = screen.get_width()
screenHeight = screen.get_height()
player_pos = pygame.Vector2(screenWidth / 2, screenHeight)
hue = 0.0
dt = 0
y_accel = 0
canJump = True
speed = 5
blockSize = 64
running = True

# 0 - No block
# 1 - Block
def drawMap(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 1:
                pygame.draw.rect(screen, (r, g, b), (j*blockSize, i*blockSize, blockSize, blockSize))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
    hue += 0.005
    if hue > 1.0:
        hue = 0.0
    rgb_color_float = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    r = int(rgb_color_float[0] * 255)
    g = int(rgb_color_float[1] * 255)
    b = int(rgb_color_float[2] * 255)

    screen.fill("black")

    drawMap(map1)

    image_rect.center = player_pos
    screen.blit(character, image_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and canJump:
            canJump = False
            y_accel += 40
    if keys[pygame.K_a]:
        player_pos.x -= speed * 100 * dt
        character = flippedCharacter
    if keys[pygame.K_d]:
        character = originalCharacter
        player_pos.x += speed * 100 * dt
        
    player_pos.y -= y_accel
    y_accel -= 3
    
    # Contain the player
    if(player_pos.y > screenHeight - 20):
        canJump = True
        player_pos.y = screenHeight - 20
        y_accel = 0 
    if(player_pos.x > screenWidth + 50):
        player_pos.x = screenWidth + 50
    if(player_pos.x < 70):
        player_pos.x = 70
        
        
    pygame.draw.rect(screen, (r, g, b), (0, screenHeight - 32, screenWidth, 50))
        
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()