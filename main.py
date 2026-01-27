import pygame

pygame.init()


screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True
dt = 0
y_accel = 0
canJump = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and canJump:
                canJump = False
                y_accel += 50

    screen.fill("blue")
    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
        
    player_pos.y -= y_accel
    y_accel -= 5
    
    if(player_pos.y > screen.get_height() - 50):
        canJump = True
        player_pos.y = screen.get_height() - 50
        y_accel = 0
    if(player_pos.x > screen.get_width() - 20):
        player_pos.x = screen.get_width() - 20
    if(player_pos.x < 20):
        player_pos.x = 20
    
    pygame.display.flip()
    
    dt = clock.tick(30) / 1000

pygame.quit()