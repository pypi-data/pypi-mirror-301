import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FPS = 60
PADDLE_RADIUS = 24
BALL_RADIUS = 15
INITIAL_BALL_SPEED = 3
BALL_SPEED_INCREMENT = 0.05
PADDLE_SPEED = 7

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodgeball')

# Initialize paddles
paddle1 = pygame.Rect(100 - PADDLE_RADIUS, HEIGHT // 2 - PADDLE_RADIUS, PADDLE_RADIUS * 2, PADDLE_RADIUS * 2)
paddle2 = pygame.Rect(WIDTH - 100 - PADDLE_RADIUS * 2, HEIGHT // 2 - PADDLE_RADIUS, PADDLE_RADIUS * 2, PADDLE_RADIUS * 2)

# Initialize ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
angle = math.radians(random.uniform(50, 300))  # Random initial angle
ball_speed_x = INITIAL_BALL_SPEED * math.cos(angle)
ball_speed_y = INITIAL_BALL_SPEED * math.sin(angle)

# Font setup
font = pygame.font.SysFont(None, 36)

def draw():
    screen.fill(BLACK)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw paddles
    pygame.draw.circle(screen, RED, paddle1.center, PADDLE_RADIUS)
    pygame.draw.circle(screen, BLUE, paddle2.center, PADDLE_RADIUS)
    
    # Draw ball
    pygame.draw.ellipse(screen, GREEN, ball)
    
    pygame.display.flip()

def handle_paddle_movement():
    keys = pygame.key.get_pressed()
    
    # Player 1 (WASD controls)
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED
    if keys[pygame.K_a] and paddle1.left > 0:
        paddle1.x -= PADDLE_SPEED
    if keys[pygame.K_d] and paddle1.right < WIDTH // 2:
        paddle1.x += PADDLE_SPEED
    
    # Player 2 (Arrow keys)
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += PADDLE_SPEED
    if keys[pygame.K_LEFT] and paddle2.left > WIDTH // 2:
        paddle2.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle2.right < WIDTH:
        paddle2.x += PADDLE_SPEED

def handle_ball_movement():
    global ball_speed_x, ball_speed_y
    ANGLE = random.uniform(70,300)
    radians = math.radians(ANGLE)
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    ball_speed_x += BALL_SPEED_INCREMENT * math.copysign(1, ball_speed_x)
    ball_speed_y += BALL_SPEED_INCREMENT * math.copysign(1, ball_speed_y)
    # Collision with top and bottom walls
    if ball.top <= 0:
        ball.top = 1
        ball_speed_y = -ball_speed_y* math.sin(radians)

    if ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT-1
        ball_speed_y = -ball_speed_y * math.sin(radians)

    # Collision with left and right walls
    if ball.left <= 0:
        ball.left = 1
        ball_speed_x = -ball_speed_x * math.cos(radians)

    if ball.right >= WIDTH:
        ball.right = WIDTH-1
        ball_speed_x = -ball_speed_x * math.cos(radians)
    
def check_collision():
    global ball_speed_x, ball_speed_y
    distance1 = math.hypot(ball.centerx - paddle1.centerx, ball.centery - paddle1.centery)
    distance2 = math.hypot(ball.centerx - paddle2.centerx, ball.centery - paddle2.centery)
    
    # Increment ball speed to make the game more challenging
    ball_speed_x += BALL_SPEED_INCREMENT * math.copysign(1, ball_speed_x)
    ball_speed_y += BALL_SPEED_INCREMENT * math.copysign(1, ball_speed_y)
    
    # Check if either paddle collides with the ball
    if distance1 < PADDLE_RADIUS + BALL_RADIUS or distance2 < PADDLE_RADIUS + BALL_RADIUS:
        return True
    return False

def play():
    global ball_speed_x, ball_speed_y
    clock = pygame.time.Clock()
    running = True
    frame_count = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        handle_paddle_movement()
        handle_ball_movement()
        
        if check_collision():
            running = False
            print("Game Over!")
        
        draw()
        clock.tick(FPS)
        frame_count += 1
        
        # Change ball direction every 180 frames (about 3 seconds)
        if frame_count == 120:
            angle = math.radians(random.uniform(0, 360))
            ball_speed_x = ball_speed_x * math.cos(angle) * math.copysign(1, ball_speed_x)
            ball_speed_y = ball_speed_y * math.sin(angle) * math.copysign(1, ball_speed_y)
            frame_count = 0

