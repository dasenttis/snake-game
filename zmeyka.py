import pygame, sys, random, os

speed = 6

# Размер окна
frame_size_x = 1380
frame_size_y = 840

check_errors = pygame.init()

if check_errors[1] > 0:
    print("Error " + check_errors[1])
else:
    print("Game Successfully initialized")

# Инициализация окна игры
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Цвета
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
very_light_pink = pygame.Color(255, 228, 225)
olive_green = pygame.Color(151, 150, 49)
coral_pink = pygame.Color(255, 127, 127)
dark_red = pygame.Color(139, 0, 0)

fps_controller = pygame.time.Clock()
# Размер одного квадрата змеи
square_size = 60

font_path = None

# Путь к сохранению рекордного числа
high_score_file = "high_score.txt"

class HighScore:
    @staticmethod
    def load():
        if os.path.exists(high_score_file):
            with open(high_score_file, "r") as file:
                return int(file.read())
        return 0

    @staticmethod
    def save(score):
        with open(high_score_file, "w") as file:
            file.write(str(score))


class Snake:
    def __init__(self):
        self.direction = 'RIGHT'
        self.head_pos = [120, 60]
        self.body = [[120, 60]]
        self.score = 0

    def move(self):
        if self.direction == 'UP':
            self.head_pos[1] -= square_size
        elif self.direction == 'DOWN':
            self.head_pos[1] += square_size
        elif self.direction == 'LEFT':
            self.head_pos[0] -= square_size
        elif self.direction == 'RIGHT':
            self.head_pos[0] += square_size

        self.body.insert(0, list(self.head_pos))

        if self.head_pos == food.position:
            self.score += 1
            food.spawn()
        else:
            self.body.pop()

        if self.head_pos[0] < 0:
            self.head_pos[0] = frame_size_x - square_size
        elif self.head_pos[0] > frame_size_x - square_size:
            self.head_pos[0] = 0
        elif self.head_pos[1] < 0:
            self.head_pos[1] = frame_size_y - square_size
        elif self.head_pos[1] > frame_size_y - square_size:
            self.head_pos[1] = 0

    def check_collision(self):
        for block in self.body[1:]:
            if self.head_pos == block:
                return True
        return False


class Food:
    def __init__(self):
        self.position = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                         random.randrange(1, (frame_size_y // square_size)) * square_size]

    def spawn(self):
        self.position = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                         random.randrange(1, (frame_size_y // square_size)) * square_size]


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.high_score = HighScore.load()
        self.game_over = False
        self.paused = False

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.paused = False

    def show_score(self, choice, color, font_size):
        score_font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.SysFont('consolas', font_size)
        score_surface = score_font.render("Score: " + str(self.snake.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x / 10, 15)
        else:
            score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
        game_window.blit(score_surface, score_rect)

    def show_high_score(self, color, font_size):
        high_score_font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.SysFont('consolas', font_size)
        high_score_surface = high_score_font.render("High Score: " + str(self.high_score), True, color)
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.midtop = (frame_size_x / 2, frame_size_y / 10)
        game_window.blit(high_score_surface, high_score_rect)

    def game_over_message(self):
        if self.snake.score > self.high_score:
            self.high_score = self.snake.score
            HighScore.save(self.high_score)

        font = pygame.font.Font(font_path, 50) if font_path else pygame.font.SysFont('consolas', 50)
        game_over_surface = font.render('Game Over', True, dark_red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
        game_window.blit(game_over_surface, game_over_rect)
        self.show_score(0, dark_red, 50)
        self.show_high_score(dark_red, 50)
        pygame.display.flip()
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_RETURN]:
                        self.reset()
                        self.game_over = False

    def pause_menu(self):
        while self.paused:
            game_window.fill(very_light_pink)
            font = pygame.font.Font(font_path, 50) if font_path else pygame.font.SysFont('consolas', 50)
            pause_surface = font.render('Pause Menu', True, dark_red)
            continue_surface = font.render('Continue', True, dark_red)
            quit_surface = font.render('Quit', True, dark_red)

            pause_rect = pause_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 4))
            continue_rect = continue_surface.get_rect(center=(frame_size_x / 2, frame_size_y / 2))
            quit_rect = quit_surface.get_rect(center=(frame_size_x / 2, frame_size_y * 3 / 4))

            game_window.blit(pause_surface, pause_rect)
            game_window.blit(continue_surface, continue_rect)
            game_window.blit(quit_surface, quit_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if continue_rect.collidepoint(mouse_pos):
                        self.paused = False
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

    def run(self):
        global food
        food = self.food  # Provide global access to food for Snake class methods
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == ord("w")) and self.snake.direction != "DOWN":
                        self.snake.direction = "UP"
                    elif (event.key == pygame.K_DOWN or event.key == ord("s")) and self.snake.direction != "UP":
                        self.snake.direction = "DOWN"
                    elif (event.key == pygame.K_LEFT or event.key == ord("a")) and self.snake.direction != "RIGHT":
                        self.snake.direction = "LEFT"
                    elif (event.key == pygame.K_RIGHT or event.key == ord("d")) and self.snake.direction != "LEFT":
                        self.snake.direction = "RIGHT"
                    elif event.key == pygame.K_ESCAPE:
                        self.paused = True
                        self.pause_menu()

            if not self.paused:
                self.snake.move()

                game_window.fill(very_light_pink)
                for pos in self.snake.body:
                    pygame.draw.rect(game_window, olive_green, pygame.Rect(pos[0] + 2, pos[1] + 2, square_size - 2, square_size - 2))
                pygame.draw.rect(game_window, coral_pink, pygame.Rect(self.food.position[0], self.food.position[1], square_size, square_size))

                if self.snake.check_collision():
                    self.game_over = True

                if self.game_over:
                    self.game_over_message()
                else:
                    self.show_score(1, dark_red, 30)
                    self.show_high_score(dark_red, 30)
                    pygame.display.update()
                    fps_controller.tick(speed)


if __name__ == "__main__":
    game = Game()
    game.run()
