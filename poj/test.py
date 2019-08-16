import curses
import random
import locale

number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
number_ch = [ord(str(i)) for i in number]
number_dict = dict(zip(number_ch, number))


def get_user_input(c):
    s = "N"
    while s not in number_dict:
        s = c.getch()
        if s not in number_dict:
            c.addstr("input error \n")
    return number_dict[s]


def main(c):
    locale.setlocale(locale.LC_ALL, '')
    code = random.choice(number)
    c.addstr("number in (0-10) please input Number")
    while True:
        inp = int(get_user_input(c))
        if inp == code:
            c.addstr("win \n")
        elif inp > code:
            c.addstr("Da le \n")
        else:
            c.addstr("Xiao le \n")


curses.wrapper(main)
