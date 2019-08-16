import curses

def main(window):
    window.clear()
    newWin()
    window.box()
    curses.textpad.rectangle(window, 10, 10, 20, 20)
    while True:
        c = window.getkey()
        window.addstr(5, 0, c)

    pass


def newWin():
    begin_x = 20
    begin_y = 7
    height = 5
    width = 40
    win = curses.newwin(height, width, begin_y, begin_x)
    return win


curses.wrapper(main)
