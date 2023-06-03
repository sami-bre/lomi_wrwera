import random
import sys
from time import sleep
from pygame.sprite import Group
import math
from game_sprites import *

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 896, 640
fly_width, fly_height = 600, 600
fly_dimensions = ((250, 850), (0, 600))
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Wenchf")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# setup the aim sprite
aim = AimSprite(initial_position=(448, 320))

# Set up the bird sprites
birdList = []
for _ in range(10):
    bird = BirdSprite(initial_position=(random.randint(*fly_dimensions[0]), random.randint(*fly_dimensions[1])))
    birdList.append(bird)
birdSprites = Group(birdList)

# Initially, the stone will be at (100, height // 2)
stone = StoneSprite(initial_position=(100, height // 2))

# Set up the projectile
projectile_radius = 5
stone.rect.x = 100
stone.rect.y = height // 2
pre_release_projectile_speed = 0
projectile_angle = 45

def setup_projectile_initial_position():
    global stone
    global pre_release_projectile_speed
    global projectile_angle
    stone.rect.x = 100
    stone.rect.y = height // 2
    pre_release_projectile_speed = 0
    projectile_angle = 45

# Set up the slingshot control
mouse_down = False
projectile_released = False
slingshot_origin = (100, height // 2)

# Set up the game clock
clock = pygame.time.Clock()

# Define velocity components
projectile_speed_x = 0
projectile_speed_y = 0

# Function to calculate velocity components based on angle and speed
def calculate_velocity(speed, angle):
    velocity_x = speed * math.cos(math.radians(angle))
    velocity_y = -speed * math.sin(math.radians(angle))
    return velocity_x, velocity_y

shots = 0
gameplay_time = 30000  # the amount of time (in milliseconds) the game lasts for

# Set up the fonts
time_font = pygame.font.Font(None, 32) # creating the font
time_font = pygame.font.Font(None, 32) # creating the font
result_font = pygame.font.Font(None, 48)



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit();
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button down
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button up
                if mouse_down:
                    mouse_down = False
                    # Calculate velocity components based on angle and speed
                    velocity_x, velocity_y = calculate_velocity(pre_release_projectile_speed, projectile_angle)
                    projectile_speed_x = velocity_x
                    projectile_speed_y = velocity_y
                    projectile_released = True
                    shots += 1

    # This is when the mouse is down but not released yet
    # Update projectile position and velocity
    if mouse_down and not projectile_released:
        mouse_pos = pygame.mouse.get_pos()
        # Calculate angle between slingshot origin and mouse position
        dx = mouse_pos[0] - slingshot_origin[0]
        dy = mouse_pos[1] - slingshot_origin[1]
        pre_release_projectile_speed = math.sqrt(dx**2 + dy**2) / 15
        projectile_angle = math.degrees(math.atan2(-dy, dx))

    # This is when the projectile is released and traveling in the air
    if projectile_released:
        stone.rect.x += projectile_speed_x
        projectile_speed_y += 0.1  # Add a small constant for gravity
        stone.rect.y += projectile_speed_y

    # Let's check if the ball is out of the window and reset the game if so
    if stone.rect.x < 0 or stone.rect.x >= width or stone.rect.y < 0 or stone.rect.y >= height:
        projectile_released = False
        mouse_down = False
        # Reset the position
        setup_projectile_initial_position()

    gameplay_time -= 1

    # Let's check if there is a collision between the stone and the birds
    collision = pygame.sprite.spritecollide(stone, birdSprites, True)
    if collision:
        # check if there are birds left
        if len(birdSprites) == 0:
            running = False

    # Clear the window
    window.fill(WHITE)

    # Draw the stone
    Group(stone).draw(window)

    # Update the sprite position to match the mouse coordinates
    aim.rect.center = pygame.mouse.get_pos()

    # Draw the sprite onto the window
    Group(aim).draw(window)

    # making the bird sprites move randomly
    birdSprites.update(fly_dimensions)

    # Draw the birds
    birdSprites.draw(window)

    # Draw the time text onto the window
    time_text_surface = time_font.render(f"Seconds left: {(gameplay_time - pygame.time.get_ticks())//1000}", True, BLACK)    # creating the surface
    window.blit(time_text_surface, (10, 10))

    # Draw the shots text onto the window
    shots_text_surface = time_font.render(f"Shots: {shots}", True, BLACK)    # creating the surface
    window.blit(shots_text_surface, (10, 40))


    if(pygame.time.get_ticks() > gameplay_time and len(birdSprites) > 0):
        running = False
        game_over_surface = result_font.render("Time's up!", True, BLACK)
        window.blit(game_over_surface, (width//2 - 80, height//2 - 20))

    if(len(birdSprites) == 0):
        running = False
        win_message_surface = result_font.render(f"You won! with {shots} shots", True, BLACK)
        window.blit(win_message_surface, (width//2 - 160, height//2 - 20))

    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

sleep(4)
# Quit the game
pygame.quit()
