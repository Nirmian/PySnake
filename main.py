import pygame, sys, random, json
from pygame.math import Vector2

CELL_SIZE = 40
CELL_ROWS = 20
CELL_COLS = 20
HEIGHT = CELL_SIZE * CELL_COLS
WIDTH = CELL_SIZE * CELL_ROWS

FPS = 60
VALID_KEYS = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]

class Food:
    def __init__(self):
        self.food_px = random.randint(0, CELL_ROWS - 1)
        self.food_py = random.randint(0, CELL_COLS - 1)

    def draw_food(self):
        food_rect = pygame.Rect(self.food_px * CELL_SIZE, self.food_py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), food_rect)

    def spawn_food(self, obstacles):
        px = random.randint(0, CELL_ROWS - 1)
        py = random.randint(0, CELL_COLS - 1)
        while (px, py) in obstacles:
            px = random.randint(0, CELL_ROWS - 1)
            py = random.randint(0, CELL_COLS - 1)
        self.food_px = px
        self.food_py = py

class Snake:
    def __init__(self):
        self.body = []
        self.head = (0, 0)
        self.dir = Vector2(0, 0)
        self.last_dir = Vector2(-100, -100)

    def draw_snake(self):
        for part in self.body:
            part_rect = pygame.Rect((int(part[0] * CELL_SIZE), int(part[1] * CELL_SIZE), CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 255, 0), part_rect)

    def spawn_snake(self, px, py):
        self.body = [Vector2(px, py), Vector2(px - 1, py)]

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

    def get_obstacles(self):
        return self.obstacles

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
        last_score_rect.centerx = WIDTH // 2
        last_score_rect.centery = highest_score_rect.centery + 50

        screen.blit(continue_text, continue_text_rect)
        screen.blit(highest_score, highest_score_rect)
        screen.blit(last_score, last_score_rect)


class Game:
    def __init__(self):
        self.board = []
        self.snake = Snake()
        self.food = Food()
        self.obstacles = Obstacle()

    def is_valid_json(self, file):
        if not file.lower().endswith('.json'):
            print("File given as a paramater doesn't have .json as extension")
            return False
        with open(file) as f:
            data = json.load(f)
        if "rows" not in data:
            print("Json file doesn't have rows field.")
            return False
        if "cols" not in data:
            print("Json file doesn't have cols field.")
            return False
        if "game_state" not in data:
            print("Json file doesn't have game_state field.")
            return False
        if data["rows"] < 10 or data["cols"] < 10 or data["rows"] > 20 or data["cols"] > 20:
            print("Rows_count and Cols_count has to be in range 10-20")
            return False
        return True

    def parse_json(self, file):
        with open(file) as f:
            data = json.load(f)
        global CELL_ROWS, CELL_COLS, HEIGHT, WIDTH
        CELL_ROWS = data["rows"]
        CELL_COLS = data["cols"]
        HEIGHT = CELL_SIZE * CELL_COLS
        WIDTH = CELL_SIZE * CELL_ROWS
        self.board = data["game_state"]

    def init_game(self):
        obs_vec = []
        for j in range(CELL_COLS):
            for i in range(CELL_ROWS):
                if self.board[i][j] == 1:
                    obs_vec.append((j, i))
                elif self.board[i][j] == 2:
                    self.snake.head = (j, i)
                    self.snake.spawn_snake(j, i)
        self.obstacles.set_obstacles(obs_vec)
        self.food.spawn_food(self.obstacles.get_obstacles())

    def new_game(self):
        self.snake.spawn_snake(self.snake.head[0], self.snake.head[1])
        self.snake.dir = Vector2(0, 0)
        self.snake.last_dir = Vector2(-100, -100)
        self.food.spawn_food(self.obstacles.get_obstacles())

if __name__ == "__main__":
    pygame.init()
    game = Game()
    if len(sys.argv) != 2:
        print("Incorrect number of parameters. Example of usage: py.exe main.py board.json")
        sys.exit()
    else:
        board = sys.argv[1]
    if game.is_valid_json(board):
        game.parse_json(board)
    else:
        print('Invalid json file. Loading default board')
        game.parse_json('board.json')
    screen = pygame.display.set_mode([HEIGHT, WIDTH])
    clock = pygame.time.Clock()

    game.init_game()
    ui = GameUI(0)
    game_over = False

    UPDATE_STATE = pygame.USEREVENT
    pygame.time.set_timer(UPDATE_STATE, 100)
    
    while True:
        screen.fill((0,0,0))
        if not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == UPDATE_STATE:
                    game.snake.move()
                    game.snake.warp()
                    if ((game.snake.body[0] in game.snake.body[1:] or game.snake.body[0] in game.obstacles.get_obstacles()) and game.snake.dir != Vector2(0,0)) or game.snake.last_dir * (-1) == game.snake.dir:
                        game_over = True
                        ui.update_high_score()
                    elif game.snake.body[0][0] == game.food.food_px and game.snake.body[0][1] == game.food.food_py:
                        game.snake.eat()
                        game.food.spawn_food(game.obstacles.get_obstacles())
                        ui.update_score()
                if event.type == pygame.KEYDOWN and event.key in VALID_KEYS:
                    game.snake.last_dir = game.snake.dir

                    if event.key == pygame.K_RIGHT:
                        game.snake.dir = Vector2(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.snake.dir = Vector2(0, 1)
                    elif event.key == pygame.K_LEFT:
                        game.snake.dir = Vector2(-1, 0)
                    elif event.key == pygame.K_UP:
                        game.snake.dir = Vector2(0, -1)

            game.snake.draw_snake()
            game.food.draw_food()
            game.obstacles.draw_obstacles()
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
                        game.new_game()
                    if event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()
            
        pygame.display.update()
        clock.tick(FPS)