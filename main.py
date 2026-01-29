import pygame
import colorsys

pygame.init()



# Create window
# 128 x 128 squares
# 8 x 15
screen = pygame.display.set_mode((1920, 1024))
clock = pygame.time.Clock()

# Create image
happy = pygame.image.load("happy.png").convert_alpha()
scaled_image = pygame.transform.scale(happy, (100, 100))
image_rect = happy.get_rect()
pygame.display.set_caption("Happy Jump")
pygame.display.set_icon(happy)

# Game variables
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height())
hue = 0.0
dt = 0
y_accel = 0
canJump = True
speed = 5
running = True

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

    image_rect.center = player_pos
    screen.blit(scaled_image, image_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and canJump:
            canJump = False
            y_accel += 40
    if keys[pygame.K_a]:
        player_pos.x -= speed * 100 * dt
    if keys[pygame.K_d]:
        player_pos.x += speed * 100 * dt
        
    player_pos.y -= y_accel
    y_accel -= 3
    
    # Contain the player
    if(player_pos.y > screen.get_height() - 20):
        canJump = True
        player_pos.y = screen.get_height() - 20
        y_accel = 0 
    if(player_pos.x > screen.get_width() + 50):
        player_pos.x = screen.get_width() + 50
    if(player_pos.x < 70):
        player_pos.x = 70
        
        
    pygame.draw.rect(screen, (r, g, b), (0, screen.get_height() - 32, screen.get_width(), 50))
        
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()