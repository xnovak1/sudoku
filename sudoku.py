import pygame
import random
import time
import datetime
from typing import List, Tuple, Optional
from sudoku_database import grids


class Grid:
    rows = 9
    cols = 9

    def __init__(self, width: int, height: int, board: List[List[int]], window):
        self.cubes = [[Cube(board[i][j], i, j, width, height) for j in range(self.cols)] for i in range(self.rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.window = window
        self.is_complete = False
        # seconds that took to complete
        self.completion_time = None

    def solve(self, gui: bool) -> bool:
        return self.solve_rec(0, 0, gui)

    def solve_rec(self, row: int, col: int, gui: bool) -> bool:
        if row == 9:
            if gui:
                self.is_complete = True
                # self.completion_time = int(time.time() - START_TIME)
            return True

        if gui:
            self.update_model()

        new_col = (col + 1) % 9
        new_row = row + 1 if new_col == 0 else row

        if self.model[row][col] != 0:
            return self.solve_rec(new_row, new_col, gui)

        for i in range(1, 10):
            if not self.check_validity(i, row, col):
                continue

            self.model[row][col] = i

            if gui:
                self.cubes[row][col].value = i
                self.cubes[row][col].draw_change(self.window, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(20)

            if self.solve_rec(new_row, new_col, gui):
                return True

            self.model[row][col] = 0

            if gui:
                self.cubes[row][col].value = 0
                self.update_model()
                self.cubes[row][col].draw_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(20)

        return False

    def check_validity(self, num: int, row: int, col: int) -> bool:
        return self.check_row(num, row) and self.check_col(num, col) and self.check_box(num, row, col)

    def check_row(self, num: int, row: int) -> bool:
        for val in self.model[row]:
            if val == num:
                return False
        return True

    def check_col(self, num: int, col: int) -> bool:
        for i in range(9):
            if self.model[i][col] == num:
                return False
        return True

    def check_box(self, num: int, row: int, col: int) -> bool:
        start_row = row - row % 3
        start_col = col - col % 3

        for i in range(3):
            for j in range(3):
                if num == self.model[start_row + i][start_col + j]:
                    return False

        return True

    def check_complete(self) -> bool:
        for row in self.cubes:
            for cube in row:
                if cube.value == 0:
                    return False
        self.is_complete = True
        self.completion_time = int(time.time() - START_TIME)
        return True

    def draw(self) -> None:
        # grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i != 0 and i % 3 == 0:
                thickness = 4
            else:
                thickness = 1

            pygame.draw.line(self.window, (0, 0, 0), (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(self.window, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thickness)

        # cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.window)

    def update_model(self) -> None:
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def click(self, position: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        x = position[0]
        y = position[1]
        if x < self.width and y < self.height:
            gap = self.width / 9
            col = x // gap
            row = y // gap
            return (int(row), int(col))
        return None

    def select(self, row: int, col: int):
        if self.selected is not None:
            select_row = self.selected[0]
            select_col = self.selected[1]
            self.cubes[select_row][select_col].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self) -> None:
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].temp_value = 0

    def reset(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                self.select(row, col)
                self.clear()

        global START_TIME
        START_TIME = int(time.time())

    def place(self, val: int) -> bool:
        row, col = self.selected
        if self.cubes[row][col].value != 0:
            return False

        self.cubes[row][col].value = val
        if not (self.check_validity(val, row, col) and self.solve(False)):
            self.cubes[row][col].value = 0
            return False
        self.cubes[row][col].temp_value = 0
        self.update_model()

        return True

    def sketch(self, value: int) -> None:
        row, col = self.selected
        self.cubes[row][col].temp_value = value


class Cube:
    def __init__(self, value: int, row: int, col: int, width: int, height: int):
        self.value = value
        self.temp_value = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, window) -> None:
        font = pygame.font.SysFont("Ariel", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.value == 0 and self.temp_value != 0:
            text = font.render(str(self.temp_value), 1, (128,128,128))
            window.blit(text, (x + 5, y + 5))
        elif self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, window, setting = True) -> None:
        fnt = pygame.font.SysFont("Ariel", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(window, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if setting:
            pygame.draw.rect(window, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 3)


def draw_window(window, grid: Grid):
    window.fill((255,255,255))
    # timer
    fnt = pygame.font.SysFont("Ariel", 40)
    if grid.completion_time is None:
        tm = str(datetime.timedelta(seconds=int(time.time()) - START_TIME))
    else:
        tm = str(datetime.timedelta(seconds=grid.completion_time))

    text = fnt.render("Time: " + tm, 1, (0,0,0))
    window.blit(text, (20, 559))

    grid.draw()


START_TIME = int(time.time())


def main() -> None:
    # choose random puzzle
    our_grid = random.choice(grids)

    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    grid = Grid(540, 540, our_grid, window)
    key = None
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    grid.clear()
                    key = None
                if event.key == pygame.K_r:
                    grid.reset()

                if event.key == pygame.K_SPACE and not grid.is_complete:
                    grid.solve(True)
                    if grid.is_complete:
                        grid.completion_time = int(time.time()) - START_TIME

                # enter
                if event.key == pygame.K_RETURN and not grid.is_complete and grid.selected is not None:
                    i, j = grid.selected
                    if grid.cubes[i][j].temp_value != 0:
                        grid.place(grid.cubes[i][j].temp_value)
                        key = None
                        if grid.check_complete():
                            print("Puzzle complete!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked is not None:
                    row, col = clicked
                    grid.select(row, col)
                    key = None

        if grid.selected and key != None:
            grid.sketch(key)

        draw_window(window, grid)
        pygame.display.update()


if __name__ == "__main__":
    pygame.font.init()
    main()
    pygame.quit()
