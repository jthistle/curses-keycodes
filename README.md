# Curses keycode parser

Parses curses keycodes into human-readable strings, or provides them in a standardized, machine-readable way.

[Skip to Usage](#usage).

### Pros

- very small
- permissive license
- flexible

### Cons

- not very well encapsulated
- probably has a few problems with non-English keyboards

## Usage

**A.** To find a key's user name:

```py
import curses
from .keycodes import key_to_username

def main(stdscr):
    dimensions = (curses.LINES, curses.COLS)
    win = curses.newwin(*dimensions, 0, 0)
    win.keypad(True)

    while True:
        key = win.getkey()

        win.erase()
        win.addstr(1, 1, "You pressed: {}".format(key_to_username(key)))
        win.refresh()

curses.wrapper(main)
```

**B.** To, for example, check if 'ctrl + delete' was pressed:

```py
import curses
from .keycodes import key_to_name_mods, KEY_DELETE, MOD_CTRL

def main(stdscr):
    dimensions = (curses.LINES, curses.COLS)
    win = curses.newwin(*dimensions, 0, 0)
    win.keypad(True)

    while True:
        key = win.getkey()

        win.erase()
        key_name, mods = key_to_name_mods(key)
        if key_name == KEY_DELETE and mods ^ MOD_CTRL == 0:
            win.addstr(1, 1, "You pressed the secret key combo!")
        else:
            win.addstr(1, 1, "You didn't press the secret key combo :(")
        win.refresh()

curses.wrapper(main)
```

**N.B** for simple, one-character keys like 'A' or '&', there are no defined constants like `KEY_A` or `KEY_AMP`. You just
need to compare against the strings `"A"` or `"&"`.

## License

Licensed under The Unlicense. See `keycodes.py` for full license text. 

