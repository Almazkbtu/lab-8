import pygame
import random
import sys
import os

WIDTH, HEIGHT = 600, 600
CELL_SIZE = 60  
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

pygame.init()
pygame.mixer.init()

music_path = "Snake/assets/snake_music.wav"
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

bg_image = pygame.transform.scale(
    pygame.image.load("Snake/assets/snake_background.png"), (WIDTH, HEIGHT))

snake_head_img = pygame.transform.scale(
    pygame.image.load("Snake/assets/snake_head.png"), (CELL_SIZE, CELL_SIZE))

snake_body_img = pygame.transform.scale(
    pygame.image.load("Snake/assets/snake_body_clean.png"), (CELL_SIZE, CELL_SIZE))

food_image = pygame.transform.scale(
    pygame.image.load("Snake/assets/food.png"), (CELL_SIZE, CELL_SIZE))

obstacle_image = pygame.transform.scale(
    pygame.image.load("Snake/assets/obstacle.png"), (CELL_SIZE, CELL_SIZE))

class Snake:
    def __init__(self):
        self.positions = [(5, 5)]
        self.direction = RIGHT
        self.length = 1  
    
    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if (new_head in self.positions or
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in obstacles):
            return False

        self.positions = [new_head] + self.positions

        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def grow(self):
        self.length += 1  

    def change_direction(self, new_direction):
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def draw(self):
        for i, (x, y) in enumerate(self.positions):
            img = snake_head_img if i == 0 else snake_body_img
            screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))

def generate_food(snake_positions, obstacles):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake_positions and pos not in obstacles:
            return pos

def generate_obstacles(count, snake_positions):
    obs = set()
    while len(obs) < count:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake_positions:
            obs.add(pos)
    return list(obs)

snake = Snake()
obstacles = generate_obstacles(3, snake.positions)
food_pos = generate_food(snake.positions, obstacles)
score = 0
level = 1
speed = 1  

running = True
while running:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.change_direction(UP)
    elif keys[pygame.K_DOWN]:
        snake.change_direction(DOWN)
    elif keys[pygame.K_LEFT]:
        snake.change_direction(LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.change_direction(RIGHT)

    if not snake.move():
        running = False

    if snake.positions[0] == food_pos:
        snake.grow()
        score += 1
        food_pos = generate_food(snake.positions, obstacles)

    if score % 3 == 0:
        level += 1
        speed = min(speed + 1, 12)  

    screen.blit(bg_image, (0, 0))

    for ox, oy in obstacles:
        screen.blit(obstacle_image, (ox * CELL_SIZE, oy * CELL_SIZE))

    fx, fy = food_pos
    screen.blit(food_image, (fx * CELL_SIZE, fy * CELL_SIZE))

    snake.draw()

    text = font.render(f"Score: {score}  Level: {level}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

screen.fill((0, 0, 0))
game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2 - 20))
pygame.display.flip()
screen.fill((0, 0, 0))
game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2 - 20))
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

pygame.quit()
sys.exit()
