import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60
GOAL_COLOR = (255, 255, 0)  # Yellow
GOAL_WIDTH = 5
GOAL_HEIGHT = 100
PADDLE_RADIUS = 24
PUCK_RADIUS = 15
PUCK_SPEED_INCREMENT = 1.1
INITIAL_PUCK_SPEED = 5
paddle_speed = 5  # Paddle movement speed

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Air Hockey')

# Initialize paddles
paddle1 = pygame.Rect(100 - PADDLE_RADIUS, HEIGHT // 2 - PADDLE_RADIUS, PADDLE_RADIUS * 2, PADDLE_RADIUS * 2)
paddle2 = pygame.Rect(WIDTH - 100 - PADDLE_RADIUS * 2, HEIGHT // 2 - PADDLE_RADIUS, PADDLE_RADIUS * 2, PADDLE_RADIUS * 2)

# Initialize puck
puck = pygame.Rect(WIDTH // 2 - PUCK_RADIUS, HEIGHT // 2 - PUCK_RADIUS, PUCK_RADIUS * 2, PUCK_RADIUS * 2)
puck_speed_x = 0
puck_speed_y = 0

# Score setup
player1_score = 0
player2_score = 0
font = pygame.font.SysFont(None, 36)

# Game state
kickoff = True
losing_player = None

def draw():
    screen.fill(BLACK)
    
    # Draw paddles
    pygame.draw.circle(screen, RED, paddle1.center, PADDLE_RADIUS)
    pygame.draw.circle(screen, BLUE, paddle2.center, PADDLE_RADIUS)
    
    # Draw puck
    pygame.draw.ellipse(screen, WHITE, puck)
    
    # Draw center line
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Draw goals
    pygame.draw.rect(screen, GOAL_COLOR, (0, HEIGHT // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT))
    pygame.draw.rect(screen, GOAL_COLOR, (WIDTH - GOAL_WIDTH, HEIGHT // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT))
    
    # Draw scores
    score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    
    pygame.display.flip()

def handle_paddle_movement():
    keys = pygame.key.get_pressed()
    
    # Player 1 (WASD controls)
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= paddle_speed
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += paddle_speed
    if keys[pygame.K_a] and paddle1.left > 0:
        paddle1.x -= paddle_speed
    if keys[pygame.K_d] and paddle1.right < WIDTH // 2 - PUCK_RADIUS:
        paddle1.x += paddle_speed
    
    # Player 2 (Arrow keys)
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += paddle_speed
    if keys[pygame.K_LEFT] and paddle2.left > WIDTH // 2 + PUCK_RADIUS:
        paddle2.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle2.right < WIDTH:
        paddle2.x += paddle_speed

def handle_puck_movement():
    global puck_speed_x, puck_speed_y, player1_score, player2_score, kickoff, losing_player
    
    puck.x += puck_speed_x
    puck.y += puck_speed_y
    
    # Collision with top and bottom walls
    if puck.top <= 0 or puck.bottom >= HEIGHT:
        puck_speed_y = -puck_speed_y
    
    # Check collision with paddles
    if paddle_collision(paddle1):
        reflect_puck(paddle1)
    elif paddle_collision(paddle2):
        reflect_puck(paddle2)
    
    # Goal scoring
    if puck.left <= 0 and HEIGHT // 2 - GOAL_HEIGHT // 2 < puck.centery < HEIGHT // 2 + GOAL_HEIGHT // 2:
        player2_score += 1
        kickoff = True
        losing_player = 1  # Player 1 conceded a goal
    elif puck.right >= WIDTH and HEIGHT // 2 - GOAL_HEIGHT // 2 < puck.centery < HEIGHT // 2 + GOAL_HEIGHT // 2:
        player1_score += 1
        kickoff = True
        losing_player = 2  # Player 2 conceded a goal
    elif puck.left <= 0 or puck.right >= WIDTH:  # Bounce back if not in goal
        puck_speed_x = -puck_speed_x

def paddle_collision(paddle):
    distance = math.hypot(puck.centerx - paddle.centerx, puck.centery - paddle.centery)
    return distance < PADDLE_RADIUS + PUCK_RADIUS

def reflect_puck(paddle):
    global puck_speed_x, puck_speed_y
    angle = math.atan2(puck.centery - paddle.centery, puck.centerx - paddle.centerx)
    
    # Reflect puck based on the angle of collision
    speed = math.hypot(puck_speed_x, puck_speed_y) * PUCK_SPEED_INCREMENT
    puck_speed_x = math.cos(angle) * speed
    puck_speed_y = math.sin(angle) * speed
    
    # Ensure the puck moves away from the paddle
    if puck.centerx < paddle.centerx:
        puck_speed_x = -abs(puck_speed_x)
    else:
        puck_speed_x = abs(puck_speed_x)

def reset_puck():
    global puck_speed_x, puck_speed_y, losing_player
    puck_speed_x = 0
    puck_speed_y = 0

    # Position the puck in the court of the player who conceded the goal
    if losing_player == 1:
        puck.x = WIDTH // 4 - PUCK_RADIUS
    elif losing_player == 2:
        puck.x = 3 * WIDTH // 4 - PUCK_RADIUS
    puck.y = HEIGHT // 2 - PUCK_RADIUS

def play():
    global kickoff , puck_speed_x , puck_speed_y
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Kickoff the puck when the player presses the spacebar
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and kickoff:
                puck_speed_x = INITIAL_PUCK_SPEED if losing_player == 1 else -INITIAL_PUCK_SPEED
                puck_speed_y = 5
                kickoff = False
        
        if kickoff:
            reset_puck()
            draw()
            continue
        handle_paddle_movement()
        handle_puck_movement()
        draw()
        
        clock.tick(FPS)

if __name__ == "__main__":
    play()
