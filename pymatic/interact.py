#!/usr/bin/python
# -*- coding: utf-8 -*-
#vim: set enc=utf8:
#
# Classes and functions for sending keypresses, mouse clicks and other xte-functions
#

import os
import string
import time

# For documentation purposes...
SPECIAL = ["Home", "Left", "Up", "Right", "Down", "Page_Up", "Page_Down", "End", "Return", "BackSpace", "Tab", "Escape", "Delete", "Shift_L", "Shift_R", "Control_L", "Control_R", "Meta_L", "Meta_R", "Alt_L", "Alt_R"]

class Emulate:
    """This class wraps all the functionality offered by Xte and can emulate a keyboard and a mouse."""

    def __init__(self, guidelay=200, display="", help=False):
        """Direct interaction with xte"""
        # How much should we wait after each command, in milliseconds
        self._guisleep = float(guidelay) / 1000.0
        print("Starting XTE...")
        options = []
        if display:
            options.append("-x " + display)
        if help:
            options.append("--help")
        cmdline = "/usr/bin/xte " + " ".join(options)
        self.xte = os.popen(cmdline, "w")

    def flush(self):
        """Send away the strings that are collected so far to xte that is running."""
        self.xte.flush()

    def close(self):
        """Stop xte from running."""
        self.xte.close()

    def cmd(self, cmd):
        """Execute a single xte command."""
        print("==> " + cmd)
        self.xte.write(cmd + "\n")
        self.flush()
        time.sleep(self._guisleep)

    def simplecmd(self, name, param=1):
        """Execute an xte command that only takes one parameter."""
        self.cmd(name + " " + str(param))

    # --- Basic mouse and keyboard events ---

    def press(self, s):
        """Press a key"""
        self.simplecmd("key", s)

    def keydown(self, s):
        """Hold down a key"""
        self.simplecmd("keydown", s)

    def keyup(self, s):
        """Release a key"""
        self.simplecmd("keyup", s)

    def mousedown(self, n):
        """Hold down a mouse button"""
        self.simplecmd("mousedown", n)

    def mouseup(self, n):
        """Release a mouse button"""
        self.simplecmd("mouseup", n)

    def sleep(self, n=200):
        """USleep using Python (instead of Xte)"""
        time.sleep(n / 1000.0)

    def sleepseconds(self, n=1):
        """Sleep using Python (instead of Xte)"""
        time.sleep(n)

    def click(self, n=1):
        """Click the mouse"""
        self.simplecmd("mouseclick", n)

    def move(self, x, y):
        """Move the mouse cursor to a given position"""
        self.cmd("mousemove %i %i" % (x, y))

    def move_relative(self, x, y):
        """Move the mouse cursor a given distance from the current location"""
        self.cmd("mousermove %i %i" % (x, y))

    def type_raw(self, s):
        """Type in a string directly"""
        self.simplecmd("str", s)

    # --- Actions that build on the simple key and mouse events ---

    def clickat(self, x, y=0, n=1):
        """Clicks the mouse somewhere. Both clickat((x, y)) and clickat(x, y) works"""
        if type(x) == type(tuple()):
            # If there are two coordinates in "x", then use those and ignore "y"
            self.move(x[0], x[1])
        else:
            self.move(x, y)
        # Click the left mousebutton as default
        self.click(n)

    def hotkey(self, hotkey, key):
        """Hold down a given hotkey while pressing the given key"""
        self.keydown(hotkey)
        self.press(key)
        self.keyup(hotkey)

    def alt(self, key, left=True):
        """Hold down the alt key and press a given key"""
        if left:
            self.hotkey("Alt_L", key)
        else:
            self.hotkey("Alt_R", key)

    def ctrl(self, key, left=True):
        """Hold down the ctrl key and press a given key"""
        if left:
            self.hotkey("Ctrl_L", key)
        else:
            self.hotkey("Ctrl_R", key)

    def shift(self, key, left=True):
        """Hold down the shift key and press a given key"""
        if left:
            self.hotkey("Shift_L", key)
        else:
            self.hotkey("Shift_R", key)

    def meta(self, key, left=True):
        """Hold down the meta key and press a given key"""
        if left:
            self.hotkey("Meta_L", key)
        else:
            self.hotkey("Meta_R", key)

    def type(self, text):
        """Punch the right keys for a given string. \n is allowed."""
        for letter in text:
            if letter == "\n":
                self.press("Return")
            elif letter == "!":
                self.shift("1")
            elif letter in string.ascii_lowercase:
                self.press(letter)
            elif letter in string.ascii_uppercase:
                self.shift(letter)
            else:
                self.type_raw(letter)
        self.flush()

    def shortwait(self, n=0):
        """A short wait is usually the gui wait. (0.2 seconds)"""
        if n:
            time.sleep(n)
        else:
            time.sleep(self._guisleep)

    def longwait(self, n=0):
        """A long wait is usually five times the gui wait. (1 second)"""
        if n:
            time.sleep(n)
        else:
            time.sleep(self._guisleep * 5.0)

    # More elaborate GUI-operations should go in the Automation class in lib/scripting.py


#
# Classes and functions for getting information from and about the screen
#
class Screen:

    def __init__(self):
        # TODO Get these values from somewhere that's not hardcoded
        self.width = 1680
        self.height = 1050
        self.center = (int(self.width / 2), int(self.height / 2))
