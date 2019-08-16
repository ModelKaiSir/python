'''
    2048游戏
'''
import curses
import random
from collections import defaultdict

# 用户动作
ACTION_UP = "UP"
ACTION_LEFT = "LEFT"
ACTION_DOWN = "DOWN"
ACTION_RIGHT = "RIGHT"
ACTION_RESTART = "RESTART"
ACTION_EXIT = "EXIT"

actions = [ACTION_UP, ACTION_LEFT, ACTION_DOWN, ACTION_RIGHT, ACTION_RESTART, ACTION_EXIT]

letter_codes = [ord(i) for i in 'WASDRQwasdrq']

action_dict = dict(zip(letter_codes, actions * 2))

def get_user_action(keyboard):
    c = "N"
    while c not in action_dict:
        c = keyboard.getch()
    return action_dict[c]

def transpose(field):
    # 将
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

class GameField:

    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = win

        self.score = 0
        self.high_score = 0
        self.reset()

    def spawn(self):
        new_element = 4 if random.randrange(100) > 89 else 2

        # 随机得到i,j坐标 在field中赋值
        (i, j) = random.choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        # field是一个 width * height 的 矩阵 field[4][4]  二维数组
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]

        self.spawn()
        self.spawn()

    def move(self, direction):

        def move_row_left(row=[]):
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row=[]):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row

            return tighten(merge(tighten(row)))

        moves = {}
        moves[ACTION_LEFT] = lambda field: [move_row_left(row) for row in field]
        moves[ACTION_RIGHT] = lambda field: invert(moves[ACTION_LEFT](invert(field)))
        moves[ACTION_UP] = lambda field: transpose(moves[ACTION_LEFT](transpose(field)))
        moves[ACTION_DOWN] = lambda field: transpose(moves[ACTION_RIGHT](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        return any(any(i > self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def move_is_possible(self, direction):

        def row_is_left_moveable(row):
            def change(i):
                if row[i] == 0 and row[i+1] != 0:
                    return True
                if row[i] != 0 and row[i+1] == row[i]:
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

        check = {}

        check[ACTION_LEFT] = lambda field: any(row_is_left_moveable(row) for row in field)
        check[ACTION_RIGHT] = lambda field: check[ACTION_LEFT](invert(field))
        check[ACTION_UP] = lambda field: check[ACTION_LEFT](transpose(field))
        check[ACTION_DOWN] = lambda field: check[ACTION_RIGHT](transpose(field))

        if direction in check:
            return check[direction]
        else:
            return False

    def draw(self,screen):
        help_string1 = "w(Up) a(Left) s(Down) d(Right)"
        help_string2 = "R(Reset) Q(Quit)"
        gameover_str = "Game_over"
        win_str = "You Win"

        def cast(s):
            screen.addstr(s+"\n")

        def draw_hor_spe():
            line = '+' + ('+------'*self.width+'+')[1:]
            spe = defaultdict(lambda: line)
            if not hasattr(draw_hor_spe, "counter"):
                draw_hor_spe.counter = 0
            cast(spe[draw_hor_spe.counter])
            draw_hor_spe.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()

        cast('SCORE:'+str(self.score))
        if 0 != self.high_score:
            cast('HIGHSCORE: '+str(self.high_score))

        for row in self.field:
            draw_hor_spe()
            draw_row(row)

        draw_hor_spe()

        if self.is_win():
            cast(win_str)
        else:
            if self.is_gameover():
                cast(gameover_str)
            else:
                cast(help_string1)
        cast(help_string2)

def main(stdscr):
    def init():
        game_field.reset()
        return 'Game'

    def not_game(state):

        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        rep = defaultdict(lambda: state)
        rep[ACTION_RESTART], rep[ACTION_EXIT] = 'Init', ACTION_EXIT
        return rep[action]

    def game():
        game_field.draw(stdscr)

        action = get_user_action(stdscr)

        if action == ACTION_RESTART:
            return 'Init'
        if action == ACTION_EXIT:
            return action
        if game_field.move(action):
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }

    # curses.use_default_color()

    game_field = GameField(win=32)

    state = 'Init'

    # 状态机开始循环
    while state != 'EXIT':
        state = state_actions[state]()


curses.wrapper(main)

