"""
Curses keycode parser. Exports (see function docstrings for more info):

- `key_to_name_mods`: parses curses keycode and returns the key name and its modifiers.
- `key_to_username`: parses curses keycode and returns the user-readable key name incl. modifiers


2020 by James Thistlewood

** LICENSE: The Unlicense **

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""


# Named keys and modifiers go up here in case you need to translate strings.
# If comparing against constants, you should only import these ones.
# `KEY_MAP` and any variables below it should not be imported.
NO_MOD = 0
MOD_SHIFT = 1
MOD_CTRL = 2
MOD_ALT = 4

MOD_SHIFT_NAME = "shift"
MOD_CTRL_NAME = "ctrl"
MOD_ALT_NAME = "alt"

KEY_BACKSPACE = "backspace"
KEY_TAB = "tab"
KEY_NEWLINE = "return"
KEY_UP_ARROW = "up arrow"
KEY_DOWN_ARROW = "down arrow"
KEY_LEFT_ARROW = "left arrow"
KEY_RIGHT_ARROW = "right arrow"
KEY_ESCAPE = "esc"
KEY_SPACE = "space"
KEY_DELETE = "delete"
KEY_INSERT = "insert"
KEY_PAGEUP = "page up"
KEY_PAGEDOWN = "page down"
KEY_HOME = "home"
KEY_END = "end"

# Main key map
KEY_MAP = {
    "\t": (KEY_TAB, NO_MOD),
    "KEY_BTAB": (KEY_TAB, MOD_SHIFT),
    "\n": (KEY_NEWLINE, NO_MOD),
    "KEY_UP": (KEY_UP_ARROW, NO_MOD),
    "KEY_DOWN": (KEY_DOWN_ARROW, NO_MOD),
    "KEY_LEFT": (KEY_LEFT_ARROW, NO_MOD),
    "KEY_RIGHT": (KEY_RIGHT_ARROW, NO_MOD),
    "KEY_SR": (KEY_UP_ARROW, MOD_SHIFT),
    "KEY_SF": (KEY_DOWN_ARROW, MOD_SHIFT),
    "KEY_SLEFT": (KEY_LEFT_ARROW, MOD_SHIFT),
    "KEY_SRIGHT": (KEY_RIGHT_ARROW, MOD_SHIFT),
    "\x1b": (KEY_ESCAPE, NO_MOD),
    "KEY_RESIZE": ("F11", NO_MOD),
    " ": (KEY_SPACE, NO_MOD),
    "\x00": (KEY_SPACE, MOD_CTRL),
    "KEY_BACKSPACE": (KEY_BACKSPACE, NO_MOD),
    "\x08": (KEY_BACKSPACE, MOD_CTRL),
    "KEY_PPAGE": (KEY_PAGEUP, NO_MOD),
    "KEY_SPREVIOUS": (KEY_PAGEUP, MOD_SHIFT),
    "KEY_NPAGE": (KEY_PAGEDOWN, NO_MOD),
    "KEY_SNEXT": (KEY_PAGEDOWN, MOD_SHIFT),
    "KEY_HOME": (KEY_HOME, NO_MOD),
    "KEY_SHOME": (KEY_HOME, MOD_SHIFT),
    "KEY_END": (KEY_END, NO_MOD),
    "KEY_SEND": (KEY_END, MOD_SHIFT),
    "KEY_IC": (KEY_INSERT, NO_MOD),
    "KEY_DC": (KEY_DELETE, NO_MOD),
    "KEY_SDC": (KEY_DELETE, MOD_SHIFT),
}


# Handle common modifiers
key_bases = {
    "kUP": KEY_UP_ARROW,
    "kDN": KEY_DOWN_ARROW,
    "kLFT": KEY_LEFT_ARROW,
    "kRIT": KEY_RIGHT_ARROW,
    "kDC": KEY_DELETE,
    "kIC": KEY_INSERT,
    "kHOM": KEY_HOME,
    "kEND": KEY_END,
    "kNXT": KEY_PAGEDOWN,
    "kPRV": KEY_PAGEUP,
}

for i in range(3, 8):
    mods = NO_MOD
    if i == 3:
        mods = MOD_ALT
    elif i == 4:
        mods = MOD_ALT | MOD_SHIFT
    elif i == 5:
        mods = MOD_CTRL
    elif i == 6:
        mods = MOD_CTRL | MOD_SHIFT
    elif i == 7:
        mods = MOD_CTRL | MOD_ALT

    for base in key_bases:
        KEY_MAP[base + str(i)] = (key_bases[base], mods)


# Init function keys
for i in range(1, 13):
    if i == 11:
        continue
    KEY_MAP["KEY_F({})".format(i)] = ("F{}".format(i), NO_MOD)

for i in range(13, 25):
    KEY_MAP["KEY_F({})".format(i)] = ("F{}".format(i - 12), MOD_SHIFT)

for i in range(25, 37):
    KEY_MAP["KEY_F({})".format(i)] = ("F{}".format(i - 24), MOD_CTRL)

for i in range(37, 49):
    KEY_MAP["KEY_F({})".format(i)] = ("F{}".format(i - 36), MOD_CTRL | MOD_SHIFT)

for i in range(49, 61):
    KEY_MAP["KEY_F({})".format(i)] = ("F{}".format(i - 48), MOD_ALT)

for i in range(61, 73):
    KEY_MAP["KEY_F({})".format(i)] = ("F{}".format(i - 60), MOD_ALT | MOD_SHIFT)

# Init CTRL keys
offset = ord("a") - 1
for i in range(1, 27):
    if chr(i) in KEY_MAP:
        continue
    KEY_MAP[chr(i)] = (chr(i + offset), MOD_CTRL)


def key_to_name_mods(key):
    """Given a key code from curses, find the key name and mods and return it as
    a tuple in the form `(key: str, mods: int flags)`. To work with this, `import *`
    and compare `key` the constants `KEY_`*, and xor `mods` with any `MOD_`*.
    """
    global KEY_MAP
    global MOD_SHIFT

    try:
        found = KEY_MAP[key]
    except KeyError:
        if len(key) > 1:
            return (key, [])

        mod = NO_MOD
        if key.lower() != key.upper():
            if key != key.lower():
                mod = MOD_SHIFT

        return (key.lower(), mod)

    return found


def mod_flags_to_strings(mods):
    modstrs = []
    if mods & MOD_CTRL:
        modstrs.append(MOD_CTRL_NAME)
    if mods & MOD_ALT:
        modstrs.append(MOD_ALT_NAME)
    if mods & MOD_SHIFT:
        modstrs.append(MOD_SHIFT_NAME)
    return modstrs

def key_to_username(key):
    """Given a key, return a user-readable key name, e.g.: kDC5 -> 'ctrl + delete'."""

    key_name, mods = key_to_name_mods(key)
    return " + ".join(mod_flags_to_strings(mods) + [key_name])
