from cell import Cell
import random
import time


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed

        if self._seed is not None:
            random.seed(self._seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()

    def _create_cells(self):
        for i in range(self._num_cols):
            self._row = []
            for j in range(self._num_rows):
                self._row.append(Cell(self._win))
            self._cells.append(self._row)

        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []

            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            dir_idx = random.randrange(len(to_visit))
            next_idx = to_visit[dir_idx]

            # right
            if next_idx[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_idx[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # up
            if next_idx[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # down
            if next_idx[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            self._break_walls_r(next_idx[0], next_idx[1])

    def _reset_cells_visited(self):
        for lst in self._cells:
            for c in lst:
                c.visited = False

    def _get_cell(self, i, j):
        if 0 <= i < self._num_cols and 0 <= j < self._num_rows:
            return self._cells[i][j]
        return None

    def solve(self, i=0, j=0):
        return self._solve_r(i, j)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        while True:
            current, left, right, up, down = (
                self._cells[i][j],
                self._get_cell(i - 1, j),
                self._get_cell(i + 1, j),
                self._get_cell(i, j - 1),
                self._get_cell(i, j + 1),
            )

            # left
            if i > 0 and not left.visited and not left.has_right_wall:
                current.draw_move(left)
                if self._solve_r(i - 1, j):
                    return True
                else:
                    current.draw_move(left, True)
            # right
            if i < self._num_cols - 1 and not right.visited and not right.has_left_wall:
                current.draw_move(right)
                if self._solve_r(i + 1, j):
                    return True
                else:
                    current.draw_move(right, True)
            # up
            if j > 0 and not up.visited and not up.has_bottom_wall:
                current.draw_move(up)
                if self._solve_r(i, j - 1):
                    return True
                else:
                    current.draw_move(up, True)
            # down
            if j < self._num_rows - 1 and not down.visited and not down.has_top_wall:
                current.draw_move(down)
                if self._solve_r(i, j + 1):
                    return True
                else:
                    current.draw_move(down, True)
            return False
