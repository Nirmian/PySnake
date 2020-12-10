import pygame, sys, random
from pygame.math import Vector2

CELL_SIZE = 40
CELL_ROWS = 20
CELL_COLS = 20
HEIGHT = CELL_SIZE * CELL_COLS
WIDTH = CELL_SIZE * CELL_ROWS

FPS = 60
VALID_KEYS = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]

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
        self.last_dir = Vector2(-100, -100)

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

    def eat(self):
        self.body.insert(0, self.body[0] + self.dir)

class Obstacle:
    def __init__(self):
        self.obstacles = []
    def set_obstacles(self, pos_vec):
        for pos_x, pos_y in pos_vec:
            self.obstacles.append((pos_x, pos_y))
    def print_obstacles(self):
        print(self.obstacles)
        for pos in self.obstacles:
            print(pos, pos)
    def draw_obstacles(self):
        for pos in self.obstacles:
            obstacle_rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (64, 64, 64), obstacle_rect)


class GameUI:
    def __init__(self, high_score):
        self.font = pygame.font.SysFont(None, 36)
        self.score = 0
        self.high_score = high_score
        self.score_text = self.font.render('Score: ' + str(self.score), True, (0, 255, 0))
    def update_score(self):
        self.score += 1
        self.score_text = self.font.render('Score: ' + str(self.score), True, (0, 255, 0))
    def draw_ui(self):
        screen.blit(self.score_text, self.score_text.get_rect())
    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
    def draw_game_end(self):
        continue_text = self.font.render('Try again? Y / N ', True, (0, 255, 0))
        continue_text_rect = continue_text.get_rect()
        continue_text_rect.centerx = WIDTH // 2 
        continue_text_rect.centery = HEIGHT // 2 - 50

        highest_score = self.font.render('High Score: ' + str(self.high_score), True, (0, 255, 0))
        highest_score_rect = highest_score.get_rect()
        highest_score_rect.centerx = WIDTH // 2 
        highest_score_rect.centery = HEIGHT // 2

        last_score = self.font.render('Your Score: ' + str(self.score), True, (0, 255, 0))
        last_score_rect = last_score.get_rect()
        last_score_rect.centerx = highest_score_rect.centerx
        last_score_rect.centery = highest_score_rect.centery + 50

        screen.blit(continue_text, continue_text_rect)
        screen.blit(highest_score, highest_score_rect)
        screen.blit(last_score, last_score_rect)

if __name__ == "__main__":
    UPDATE_STATE = pygame.USEREVENT
    pygame.time.set_timer(UPDATE_STATE, 100)
    ui = GameUI(0)
    snake = Snake(2, 2)
    food = Food()
    obstacles = Obstacle()
    obstacles.set_obstacles([(0,0), (0,1), (0,2) ,(2,0), (2,1), (2,2)])
    game_over = False
    
    while True:
        screen.fill((0,0,0))
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == UPDATE_STATE:
                    snake.move()
                    snake.warp()
                    if ((snake.body[0] in snake.body[1:] or snake.body[0] in obstacles.obstacles) and snake.dir != Vector2(0,0)) or snake.last_dir * (-1) == snake.dir:
                        game_over = True
                        ui.update_high_score()
                    elif snake.body[0][0] == food.food_px and snake.body[0][1] == food.food_py:
                        snake.eat()
                        food = Food()
                        ui.update_score()
                if event.type == pygame.KEYDOWN and event.key in VALID_KEYS:
                    snake.last_dir = snake.dir

                    if event.key == pygame.K_RIGHT:
                        snake.dir = Vector2(1, 0)
                    elif event.key == pygame.K_DOWN:
                        snake.dir = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT:
                        snake.dir = Vector2(-1, 0)
                    elif event.key == pygame.K_UP:
                        snake.dir = Vector2(0, -1)

            snake.draw_snake()
            food.draw_food()
            obstacles.draw_obstacles()
            ui.draw_ui()
        else:
            ui.draw_game_end()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        game_over = False
                        ui = GameUI(ui.high_score)
                        snake = Snake(2, 2)
                        food = Food()
                    if event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()
            
        pygame.display.update()
        clock.tick(FPS)