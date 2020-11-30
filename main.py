import pygame, sys, random
CELL_SIZE = 40
CELL_ROWS = 20
CELL_COLS = 20
HEIGHT = CELL_SIZE * CELL_COLS
WIDTH = CELL_SIZE * CELL_ROWS

FPS = 30

pygame.init()
screen = pygame.display.set_mode([HEIGHT, WIDTH])
clock = pygame.time.Clock()
key_pressed = ""

class Food:
    def __init__(self):
        self.food_px = random.randint(0, CELL_ROWS - 1)
        self.food_py = random.randint(0, CELL_COLS - 1)
    
    def draw_food(self):
        food_rect = pygame.Rect(self.food_px * CELL_SIZE, self.food_py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), food_rect)


class Snake:
    def __init__(self, px, py):
        self.snake_head_px = px
        self.snake_head_py = py
        self.snake_head = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.snake_head.fill((0,255,0))

if __name__ == "__main__":
    snake = Snake(0, WIDTH // 2)
    food = Food()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_pressed = event.key
        
        if key_pressed == pygame.K_RIGHT:
            snake.snake_head_px += 40
        if key_pressed == pygame.K_LEFT:
            snake.snake_head_px -= 40
        if key_pressed == pygame.K_UP:
            snake.snake_head_py -= 40
        if key_pressed == pygame.K_DOWN:
            snake.snake_head_py += 40
        
        if snake.snake_head_px < 0 or snake.snake_head_px >= HEIGHT:
            snake.snake_head_px %= HEIGHT
        if snake.snake_head_py < 0 or snake.snake_head_py >= WIDTH:
            snake.snake_head_py %= WIDTH

        screen.fill((0,0,0))
        screen.blit(snake.snake_head,(snake.snake_head_px, snake.snake_head_py))
        food.draw_food()
        pygame.display.update()
        clock.tick(FPS)