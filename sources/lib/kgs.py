#!/usr/bin/python
# -*- coding: utf-8 -*-
#vim: set enc=utf8:

class KGS:
    """Starts Cgoban3, logs onto KGS and controls the client"""

    def __init__(self, auto, username, password):
        # TODO Use script-files in the script/ directory, refer to them by name
        self.auto = auto

        self.startkgs()
        self.logon(username, password)

