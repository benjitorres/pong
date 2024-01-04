import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 90
BALL_SIZE = 15
WHITE = (255, 255, 255)
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong with AI')

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        self.rect.y += y
        self.rect.y = max(self.rect.y, 0)
        self.rect.y = min(self.rect.y, SCREEN_HEIGHT - PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-4, 4])
        self.dy = random.choice([-4, 4])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Collision with top/bottom
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy *= -1

        # Out of bounds left/right
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.rect.x, self.rect.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            self.dx *= -1
            self.dy *= -1

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def collision_with_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.dx *= -1

# Function to handle AI movement
def ai_movement(ai_paddle, ball):
    if ai_paddle.rect.centery < ball.rect.centery:
        ai_paddle.move(4)
    else:
        ai_paddle.move(-4)

# Game objects
ai_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
player_paddle = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_paddle.move(-5)
    if keys[pygame.K_DOWN]:
        player_paddle.move(5)

    # AI movement
    ai_movement(ai_paddle, ball)

    # Ball movement
    ball.move()
    ball.collision_with_paddle(player_paddle)
    ball.collision_with_paddle(ai_paddle)

    # Drawing
    screen.fill((0, 0, 0))
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
