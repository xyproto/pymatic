#!/usr/bin/python
# -*- coding: utf-8 -*-
#vim: set enc=utf8:
#
# Classes and functions for interpreting captured graphics and screenshots
#

class Interpret:

    def __init__(self, surface):
        # The screen surface
        self.surface = surface

    def getpixel(self, x, y):
        # code to fetch a pixel from self.surface at (x, y)
        # returns (r, g, b)
        pass

    def is_a_dialog(self):
        # code to tell if there's a dialog window up right now, waiting for attention
        pass
