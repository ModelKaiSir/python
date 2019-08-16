'''
    面向对象的 2048
'''
import random
import curses
from collections import defaultdict


class GameField:
    ACT_LEFT = "LEFT"
    ACT_RIGHT = "RIGHT"
    ACT_UP = "UP"
    ACT_DOWN = "DOWN"
    ACT_RESET = "RESET"
    ACT_EXIT = "EXIT"

    field = []
    act_keys = [ACT_UP, ACT_LEFT, ACT_DOWN, ACT_RESET, ACT_RESET, ACT_EXIT]
    actions = dict(zip(list(map(ord, 'WASDEQwasdeq')), act_keys * 2))

    def __init__(self, w, h, win=2048):
        self.w = w
        self.h = h
        self.win = win
        self.score = 0
        self.high_score = 0
        self.field = [[0 for i in range(w)] for j in range(h)]

    def invert(self, field):
        return [row[::-1] for row in field]

    def transpose(self, field):
        return [list(row) for row in zip(*field)]

    def spawn(self):
        ele = 4 if random.randrange(100) > 89 else 2
        # 先将field的元素下标转换成数组 [(i,j)] 再随机取一个坐标
        (i, j) = random.choice([(i, j) for i in range(self.w) for j in range(self.h) if self.field[i][j] == 0])
        self.field[i][j] = ele

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        # 清空field
        self.field = [[0 for i in range(self.w)] for j in range(self.h)]
        # 随机生成两个数
        self.spawn()
        self.spawn()

    def isWin(self):
        return any(any(i > self.win for i in row) for row in self.field)
        pass

    def isGameOver(self):
        return not any(self.ove_is_possible(move) for move in self.actions)
        pass

    def ove_is_possible(self, direction):

        def is_left(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i] == row[i + 1]:
                    return True
                return False

            return any(change(i) for i in range(len(row) - 1))

        check = {}

        check[self.ACT_LEFT] = lambda field: any(is_left(row) for row in field)
        check[self.ACT_RIGHT] = lambda field: check[self.ACT_RIGHT](self.invert(field))
        check[self.ACT_UP] = lambda field: check[self.ACT_LEFT](self.transpose(field))
        check[self.ACT_DOWN] = lambda field: check[self.ACT_RIGHT](self.transpose(field))

        if direction in check:
            return check[direction]
        else:
            return False

    pass


class Grid:
    # 棋盘类 负责画界面
    help_string1 = "w(Up) a(Left) s(Down) d(Right)"
    help_string2 = "R(Reset) Q(Quit)"
    game_over_str = "Game_over"
    win_str = "You Win"

    spe_count = 0

    def __init__(self):
        self.screen = None
        self.game_field = None
        pass

    def start(self, screen):
        self.screen = screen
        self.game_field = GameField(4, 4)
        self.drawGrid(self.game_field)

    def _draw(self, string):
        self.screen.addstr(string + "\n")

    def _draw_hor_spe(self):
        line = "+" + ("+------" * self.game_field.w + "+")[1:]
        spe = defaultdict(lambda: line)

        self._draw(spe[self.spe_count])
        self.spe_count += 1
        pass

    def _draw_row(self, row):
        self._draw(''.join("|{: ^5} ".format(num) for num in row) + "|")
        pass

    def drawGrid(self, game_field: GameField):
        self.screen.clear()
        for row in game_field.field:
            self._draw_hor_spe()
            self._draw_row(row)

        self._draw_hor_spe()
        self._draw(self.help_string1)
        self._draw(self.help_string2)


class Game:
    STATE_GAME = "game"
    STATE_INIT = "init"
    STATE_GAME_OVER = "gameOver"
    STATE_WIN = "win"

    def init(self):

        pass

    def game(self):
        pass

    def not_game(self):
        pass

    def get_user_input(self, actions: dict):
        ch = "N"
        while ch not in actions:
            ch = self.screen.getch()
        return actions.get(ch, "None")

    def start(self, screen):
        g = Grid()
        if isinstance(g.game_field, GameField):
            g.game_field.reset()
            g.start(screen)
            g.game_field.draw(screen)
            action = self.get_user_action(screen)

            if action == GameField.ACT_RESET:
                return self.STATE_WIN
            if action == GameField.ACT_EXIT:
                return action
            if g.game_field.move(action):
                if g.game_field.is_win():
                    return self.STATE_WIN
                if g.game_field.is_gameover():
                    return self.STATE_GAME_OVER
            return self.STATE_GAME
        pass


game = Game()
curses.wrapper(game.start)
