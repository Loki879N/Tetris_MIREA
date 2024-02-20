import pygame
import random


pygame.init()
WINDOW_SIZE = 750, 750
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'violet']
figure = [[(0, 0), (1, 0), (0, 1), (1, 1)],
          [(1, 0), (0, 0), (2, 0), (3, 0)],
          [(0, 0), (1, 0), (2, 0), (1, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 2)],
          [(0, 0), (0, 1), (0, 2), (-1, 2)],
          [(2, 1), (1, 1), (1, 2), (0, 2)],
          [(0, 0), (0, 1), (1, 1), (1, 2)]]

FPS = 60
clock = pygame.time.Clock()


class Figure(object):
    def __init__(self):
        color = random.choice(colors)
        self.color = color
        self.form = [pygame.Rect(x + 3, y, 1, 1) for x, y in random.choice(figure)]
        self.side = 35
        self.v = 3
        self.falling = True

    def draw(self, screen):
        for square in self.form:
            pygame.draw.rect(screen, self.color, (square.x * self.side + 25,
                                                  square.y * self.side + 25,
                                                  self.side, self.side))
        pygame.display.flip()

    def check_y(self, field):
        for c in self.form:
            if field.cells[c.y + 1][c.x]:
                return False
        return True

    def fall(self, field):
        if self.falling:
            clock.tick(self.v)
            y_y = [r.y for r in self.form]
            if max(y_y) < 19 and self.check_y(field):
                for r in self.form:
                    r.y += 1
            else:
                field.add_figure(self.form, self.color)
                self.falling = False
        clock.tick(FPS)
        pygame.display.flip()

    def check_x_2(self, field, movement):
        for f in self.form:
            if field.cells[f.y][f.x + 1] and movement is False:
                return False
        return True

    def check_x(self, field, movement):
        for f in self.form:
            if field.cells[f.y][f.x - 1] != 0 and movement:
                return False
        return True

    def move(self, movement, field):
        x_coord = [coord.x for coord in self.form]
        if min(x_coord) > 0 and movement and self.check_x(field, movement) or\
                (max(x_coord) <= 8 and movement is False and self.check_x_2(field, movement)):
            for rects in self.form:
                if movement:
                    rects.x -= 1
                else:
                    rects.x += 1
            pygame.display.flip()

    def check_turn(self, field):
        coords = []
        for forms in self.form:
            x = forms.y - self.form[0].y
            y = forms.x - self.form[0].x
            coords.append((x, y))
        for f in range(len(self.form)):
            if self.form[0].x - coords[f][0] > 9 or self.form[0].x - coords[f][0] < 0\
                    or field.cells[self.form[f].y][self.form[0].x - coords[f][0]] != 0:
                return False
            elif self.form[0].y - coords[f][1] > 19 or self.form[0].y - coords[f][1] < 0 or\
                    field.cells[self.form[0].y - coords[f][1]][self.form[f].x] != 0:
                return False
        return True

    def turn(self, field):
        if self.check_turn(field) is True:
            for forms in self.form:
                x = forms.y - self.form[0].y
                y = forms.x - self.form[0].x
                forms.x = self.form[0].x - x
                forms.y = self.form[0].y + y


class Field(object):
    def __init__(self, width, height, side):
        self.width = width
        self.height = height
        self.side = side
        self.color = 'black'
        self.stroke = 'white'
        self.points_game = 0
        self.x = 25
        self.y = 25
        self.cells = [[0 for _ in range(10)] for _ in range(20)]
        self.field = [pygame.Rect(x * side + self.x, y * side + self.y, side, side) for x in range(width) for y in range(height)]

    def draw_field(self, screen):
        screen.fill(self.color)
        [pygame.draw.rect(screen, self.stroke, coord, width=1) for coord in self.field]

    def score(self, count_lines):
        scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500, 5: 3100}
        return scores[count_lines]

    def points(self, screen, count_lines):
        font = pygame.font.Font(None, 50)
        scores = self.score(count_lines)
        self.points_game += scores
        text = font.render(f"Очки {self.points_game}", True, (100, 255, 100))
        screen.blit(text, (400, 300))

    def draw_next_figure(self, screen, next_figur):
        font = pygame.font.Font(None, 30)
        text = font.render(f"Следующая фигура:", True, (100, 255, 100))
        screen.blit(text, (400, 250))
        for square in range(4):
            pygame.draw.rect(screen, next_figur.color,
                             (next_figur.form[square].x * self.side + 25 + 400,
                              next_figur.form[square].y * self.side + 25 + 75,
                              self.side, self.side))

    def add_figure(self, figure, color):
        for rects in range(4):
            self.cells[figure[rects].y][figure[rects].x] = color

    def check_lines(self, screen):
        del_cells = 0
        del_lines = 0
        num_line = 19
        for y in range(19, -1, -1):
            for x in range(10):
                if self.cells[y][x] != 0:
                    del_cells += 1
                self.cells[num_line][x] = self.cells[y][x]
            if del_cells != 10:
                num_line -= 1
            else:
                del_lines += 1
            del_cells = 0
        self.points(screen, del_lines)

    def end_game(self):
        for x in range(10):
            if self.cells[0][x] != 0:
                return False
        return True

    def draw_figures(self, screen):
        for y in range(20):
            for x in range(10):
                if self.cells[y][x] != 0:
                    pygame.draw.rect(screen, self.cells[y][x],
                                     (x * self.side + self.x, y * self.side + self.y, self.side, self.side))


class GameManager(object):
    def __init__(self):
        self.field = Field(10, 20, 35)
        self.movement = None

    def game_cycle(self):
        screen = pygame.display.set_mode(WINDOW_SIZE)
        running = True
        figur = Figure()
        next_figur = Figure()
        while running:
            self.field.draw_field(screen)
            self.field.draw_figures(screen)
            self.field.points(screen, 0)
            self.field.draw_next_figure(screen, next_figur)
            self.field.check_lines(screen)
            if self.field.end_game() is False:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement = True
                        figur.move(self.movement, self.field)
                    elif event.key == pygame.K_RIGHT:
                        self.movement = False
                        figur.move(self.movement, self.field)
                    elif event.key == pygame.K_UP:
                        figur.turn(self.field)
            figur.draw(screen)
            if figur.falling is not False:
                figur.fall(self.field)
            else:
                figur = next_figur
                next_figur = Figure()
                self.field.draw_next_figure(screen, next_figur)
            pygame.display.flip()
            clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    manager = GameManager()
    manager.game_cycle()
