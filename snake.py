import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame as pg
from random import randint as rand


WINDOW_SIZE = 1050, 750
CALL_SIZE = 30
FIELD_SIZE = WINDOW_SIZE[0] // CALL_SIZE, WINDOW_SIZE[1] // CALL_SIZE
START_POS = FIELD_SIZE[0] // 2, FIELD_SIZE[1] // 2
DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
SAVE_FILE = r'save_record.txt'
COLORS = ['green', 'blue', 'purple', 'yellow', 'gray', 'black', 'brown', 'orange', 'pink', 'magenta']


class Game:
    """ГЛАВНЫЙ КЛАСС"""

    def __init__(self):
        pg.init()
        pg.font.init()
        self.font_score = pg.font.SysFont("Arial", 50)
        self.font_gameover = pg.font.SysFont("Arial", 70)
        self.font_space = pg.font.SysFont("Arial", 45)
        self.font_record = pg.font.SysFont('Arial', 40)
        self.display = pg.display.set_mode(WINDOW_SIZE)
        self.snake = [START_POS]
        self.alive = True
        self.apple = (rand(0, FIELD_SIZE[0] - 1), rand(0, FIELD_SIZE[1] - 1))
        self.clock = pg.time.Clock()
        self.direct = 0
        self.fps = 5

        try:
            with open(SAVE_FILE, 'rt') as file:
                self.record = int(file.readline())

        except Exception:
            with open(SAVE_FILE, 'wt') as file:
                file.writelines('1')
            self.record = 1

    def run(self):
        """Запуск игры"""

        running = True
        while running:
            self.display.fill('#8e68ab')
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:
                        running = False

                    if event.key == pg.K_RIGHT and self.direct != 2:
                        self.direct = 0

                    if event.key == pg.K_DOWN and self.direct != 3:
                        self.direct = 1

                    if event.key == pg.K_LEFT and self.direct != 0:
                        self.direct = 2

                    if event.key == pg.K_UP and self.direct != 1:
                        self.direct = 3

                    if not self.alive and event.key == pg.K_SPACE:
                        self.alive = True
                        self.snake = [START_POS]
                        self.apple = rand(0, FIELD_SIZE[0] - 1), rand(0, FIELD_SIZE[1] - 1)
                        self.fps = 5

            for ind, value in enumerate(self.snake):
                ind = ind % len(COLORS)
                pg.draw.rect(self.display, COLORS[ind], (value[0] * CALL_SIZE, value[1] * CALL_SIZE, CALL_SIZE - 1, CALL_SIZE - 1))

            pg.draw.rect(self.display, 'red', (self.apple[0] * CALL_SIZE, self.apple[1] * CALL_SIZE, CALL_SIZE - 1, CALL_SIZE - 1))

            if self.alive:
                """если змейка жива"""

                new_pos = self.snake[0][0] + DIRECTIONS[self.direct][0], self.snake[0][1] + DIRECTIONS[self.direct][1]

                if not (0 <= new_pos[0] < FIELD_SIZE[0] and 0 <= new_pos[1] < FIELD_SIZE[1]) or new_pos in self.snake:
                    """если врезалась в стену или сама в себя"""

                    self.alive = False

                elif new_pos[0] == self.apple[0] and new_pos[1] == self.apple[1]:
                    """если попала на яблоко"""

                    self.fps += 1
                    self.apple = (rand(0, FIELD_SIZE[0] - 1), rand(0, FIELD_SIZE[1] - 1))

                else:
                    self.snake.pop(-1)

                self.snake.insert(0, new_pos)

            else:
                """если змейка не жива"""

                if self.record < len(self.snake):
                    """если рекорд побит"""

                    with open(SAVE_FILE, 'wt') as file:
                        file.writelines(str(len(self.snake)))
                    self.record = len(self.snake)

                text = self.font_gameover.render("GAME OVER", True, "white")
                self.display.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - 50))
                text = self.font_space.render("Press SPACE for restart", True, "white")
                self.display.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 + 10))

            self.display.blit(self.font_score.render(f"Score: { len(self.snake) }", True, "yellow"), (5, 5))
            self.display.blit(self.font_record.render(f'Record: { self.record }', True, 'red'), (5, 50))
            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
