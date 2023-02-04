from typing import List


class Sudoku:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.is_complete = False

    def solve(self) -> None:
        self.solve_rec(0, 0)
        if not self.is_complete:
            raise Exception("Sudoku can not be solved.")

    def solve_rec(self, row: int, col: int) -> bool:
        if self.check_complete():
            self.is_complete = True
            return True

        new_col = (col + 1) % 9
        new_row = row + 1 if new_col == 0 else row

        if self.grid[row][col] != 0:
            return self.solve_rec(new_row, new_col)

        for i in range(1, 10):
            if not self.check_validity(i, row, col):
                continue

            self.grid[row][col] = i

            if self.solve_rec(new_row, new_col):
                return True

            self.grid[row][col] = 0

        return False

    def check_validity(self, num: int, row: int, col: int) -> bool:
        return self.check_row(num, row) and self.check_col(num, col) and self.check_box(num, row, col)

    def check_row(self, num: int, row: int) -> bool:
        for square in self.grid[row]:
            if square == num:
                return False
        return True

    def check_col(self, num: int, col: int) -> bool:
        for i in range(9):
            if self.grid[i][col] == num:
                return False
        return True

    def check_box(self, num: int, row: int, col: int) -> bool:
        start_row = row - row % 3
        start_col = col - col % 3

        for i in range(3):
            for j in range(3):
                square = self.grid[start_row + i][start_col + j]
                if square == num:
                    return False

        return True

    def check_complete(self) -> bool:
        for row in self.grid:
            for num in row:
                if num == 0:
                    return False
        return True


def main() -> None:
    test_sudoku()


def test_sudoku() -> None:

    sudoku2 = Sudoku([[9, 0, 6, 0, 7, 0, 4, 0, 3],
                      [0, 0, 0, 4, 0, 0, 2, 0, 0],
                      [0, 7, 0, 0, 2, 3, 0, 1, 0],
                      [5, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 4, 0, 2, 0, 8, 0, 6, 0],
                      [0, 0, 3, 0, 0, 0, 0, 0, 5],
                      [0, 3, 0, 7, 0, 0, 0, 5, 0],
                      [0, 0, 7, 0, 0, 5, 0, 0, 0],
                      [4, 0, 5, 0, 1, 0, 7, 0, 8]])

    sudoku2.solve()
    assert sudoku2.is_complete

    # -------------------------------------------

    sudoku1 = Sudoku([[0, 0, 0, 8, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 4, 3],
                      [5, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 7, 0, 8, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 2, 0, 0, 3, 0, 0, 0, 0],
                      [6, 0, 0, 0, 0, 0, 0, 7, 5],
                      [0, 0, 3, 4, 0, 0, 0, 0, 0],
                      [0, 0, 0, 2, 0, 0, 6, 0, 0]])

    sudoku1.solve()
    assert sudoku1.is_complete
    assert sudoku1.grid == [[2, 3, 7, 8, 4, 1, 5, 6, 9],
                            [1, 8, 6, 7, 9, 5, 2, 4, 3],
                            [5, 9, 4, 3, 2, 6, 7, 1, 8],
                            [3, 1, 5, 6, 7, 4, 8, 9, 2],
                            [4, 6, 9, 5, 8, 2, 1, 3, 7],
                            [7, 2, 8, 1, 3, 9, 4, 5, 6],
                            [6, 4, 2, 9, 1, 8, 3, 7, 5],
                            [8, 5, 3, 4, 6, 7, 9, 2, 1],
                            [9, 7, 1, 2, 5, 3, 6, 8, 4]]

    # -------------------------------------------


if __name__ == "__main__":
    main()
