import pygame, sys, random
from pygame.math import Vector2

CELL_SIZE = 40
CELL_ROWS = 20
CELL_COLS = 20
HEIGHT = CELL_SIZE * CELL_COLS
WIDTH = CELL_SIZE * CELL_ROWS
FPS = 60

pygame.init()
screen = pygame.display.set_mode([HEIGHT, WIDTH])
clock = pygame.time.Clock()

class Food:
    def __init__(self):
        self.food_px = random.randint(0, CELL_ROWS - 1)
        self.food_py = random.randint(0, CELL_COLS - 1)
    
    def draw_food(self):
        food_rect = pygame.Rect(self.food_px * CELL_SIZE, self.food_py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), food_rect)


class Snake:
    def __init__(self, px, py):
        self.body = [Vector2(px - 1, py), Vector2(px,py)]
        self.dir = Vector2(0, 0)

    def draw_snake(self):
        for part in self.body:
            part_rect = pygame.Rect((int(part[0] * CELL_SIZE), int(part[1] * CELL_SIZE), CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 255, 0), part_rect)

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.dir)
        self.body = body_copy

    def warp(self):
        if self.body[0][0] < 0 or self.body[0][0] >= CELL_ROWS:
            self.body[0][0] %= CELL_ROWS
        if self.body[0][1] < 0 or self.body[0][1] >= CELL_COLS:
            self.body[0][1] %= CELL_COLS

if __name__ == "__main__":
    UPDATE_STATE = pygame.USEREVENT
    pygame.time.set_timer(UPDATE_STATE, 100)
    snake = Snake(2, 2)
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == UPDATE_STATE:
                snake.move()
                snake.warp()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.dir = Vector2(1, 0)
                elif event.key == pygame.K_DOWN:
                    snake.dir = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.dir = Vector2(-1, 0)
                elif event.key == pygame.K_UP:
                    snake.dir = Vector2(0, -1)

        screen.fill((0,0,0))
        snake.draw_snake()
        food.draw_food()
        pygame.display.update()
        clock.tick(FPS)