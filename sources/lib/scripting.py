#!/usr/bin/python
# -*- coding: utf-8 -*-
#vim: set enc=utf8:

# More elaborate GUI-operations
# Supporting the AutoIT syntax would be nice

from lib.interact import Emulate, Screen
import os

class ScriptFiles:
    """A class for managing the directory with scripts.
    The name of the script is the same as the filename."""

    def __init__(self, path):
        self.path = path
        self.filenames = os.listdir(path)

    def firstname(self, filename):
        try:
            return filename[::-1].split(".", 1)[1][::-1]
        except IndexError:
            print "Filename does not have a first name:", filename
            return filename

    def lastname(self, filename):
        try:
            return filename[::-1].split(".", 1)[0][::-1]
        except IndexError:
            print "Filename does not have a last name:", filename
            return filename

    def listscripts(self):
        return self.filenames

    def getscriptbyfilename(self, filename):
        contents = ""
        if (filename in self.filenames):
            f = open(os.path.join(self.path, filename))
            contents = f.read().strip()
            f.close()
        return contents

    def runscriptbyfirstname(self, firstname, settings):
        if firstname + ".nai" in self.filenames:
            script = self.getscriptbyfilename(firstname + ".nai")
            interp = NaiveInterpreter(settings)
        elif firstname + ".aut" in self.filenames:
            script = self.getscriptbyfilename(firstname + ".aut")
            interp = AutoItInterpreter(settings)
        else:
            if not script:
                print "Could not find any contents for that script"
            else:
                print "Could not find an interpreter for that extension"
            return
        interp.run_this(script)
        interp.close()

class Settings:
    """The settings for a specific automation. Can be expanded later on."""
    
    def __init__(self, guidelay=100):
        self.guidelay = guidelay


class Automation:
    """An automation (Automation) consists of a way to send keypresses (Emulate) and a way to read the screen (Screen)"""

    def __init__(self, settings):
        self.emu = Emulate(settings.guidelay)
        self.screen = Screen()

    def startapp(self, command):
        """Starts an application by pressing Alt+F2, clicking in the center of the screen and typing in a command."""
        e = self.emu
        e.alt("F2")
        e.shortwait()
        e.clickat(self.screen.center)
        e.shortwait()
        e.type(command + "\n")
        e.longwait()

    def alttab(self):
        """Presses Alt+Tab"""
        e = self.emu
        e.alt("Tab")
        e.shortwait()

    def say(self, text):
        """Types in text, followed by Return"""
        self.emu.type(text + "\n")
        self.emu.shortwait()

    def close(self):
        """Stops the key/mouse emulation"""
        self.emu.close()

    def getemu(self):
        """Returns the Emulation object for sending keys and mouseclicks"""
        return self.emu

    def getscreen(self):
        """Returns the Screen object for aquiring and interpreting graphics"""
        return self.screen


class GenericInterpreter:
    """A generic interpreter, meant to be subclassed"""

    def __init__(self, settings):
        self.auto = Automation(settings)
        self.emu = self.auto.getemu()
        self.variables = {}
        self.fdict = {}

    def info_msgbox(self, message, title):
        """Display an informal messagebox using Zenity"""
        return os.system("zenity --info --text=\"%s\" --title=\"%s\"" % (message, title))

    def question_msgbox(self, message, title):
        """Display a messagebox that asks a question using Zenity"""
        return os.system("zenity --question --text=\"%s\" --title=\"%s\"" % (message, title))

    def warning_msgbox(self, message, title):
        """Display a messagebox with a warning using Zenity"""
        return os.system("zenity --warning --text=\"%s\" --title=\"%s\"" % (message, title))

    def close(self):
        """Close the Automation object"""
        self.auto.close()

    def call_function(self, s):
        """Call a function given as a text string. Example: function(arg1, arg2)."""
        fun, arg = s.split("(")
        arguments = [self.value(x.strip()) for x in arg.split(")")[0].split(",")]
        # call the corresponding function with the given arguments
        try:
            return self.fdict[fun].__call__(*arguments)
        except KeyError, e:
            print "There is no such function:", e
            return ""

    def run_this(self, script):
        """Interpret and execute a script (lines of text)"""
        for line in script.strip().split("\n"):
            # TODO Interpret lines more than just calling functions
            if line.startswith("#"):
                # Skip lines that start with #
                continue
            retval = self.call_function(line.strip())
            #print retval


class NaiveInterpreter(GenericInterpreter):
    """An interpreter for a naive scripting language"""

    def __init__(self, settings):
        GenericInterpreter.__init__(self, settings)
        # the function dictionary
        self.fdict = {
            "msgbox":self.msgbox,
            "run":self.run,
            "sleep":self.sleep,
            "click":self.click,
            "print":self.printfun,
            "screenshot":self.screenshot
        }

    def value(self, s):
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        else:
            return s

    def msgbox(self, message, title="Info"):
        """example: msgbox("Hello World!")"""
        return self.info_msgbox(message, title)

    def run(self, cmd):
        print "Running %s..." % (cmd)
        os.system(cmd)

    def sleep(self, n):
        self.emu.sleep(int(n))

    def click(self, x, y):
        self.emu.clickat(int(x), int(y))

    def printfun(self, msg):
        print msg

    def screenshot(self, filename="screenshot.png"):
        fn = "../screenshots/" + filename
        # Change which X to take screnshots from
        os.putenv("DISPLAY", ":42.0")
        # Take a screenshot of the virtual X fb
        os.system("scrot " + fn)
        
class AutoItInterpreter(GenericInterpreter):
    """An interpreter for the AutoIt language"""

    def __init__(self, settings):
        GenericInterpreter.__init__(self, settings)
        # the function dictionary
        self.fdict = {"MsgBox":self.msgbox}

    def value(self, s):
        """Evaluation of values. Add strings and numbers together, etc."""
        #TODO Add more complex evaluation than just True and False...
        if s == "False":
            return False
        elif s == "True":
            return True
        elif s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        else:
            return s

    def msgbox(self, flagstring, title, message, timeout=0, hwnd=0):
        """example: MsgBox(64, "Title", "Hello world")"""
        # TODO Support the other flags and paramters that MsgBox supports
        # See: http://www.autoitscript.com/autoit3/docs/functions/MsgBox.htm
        retval = 0
        flag = int(flagstring)
        if flag in (0, 64):
            # info
            retval = self.info_msgbox(message, title)
        elif flag == 32:
            # question
            retval = self.question_msgbox(message, title)
        elif flag == 48:
            # warning
            retval = self.warning_msgbox(message, title)
        else:
            print "MsgBox, unknown flag:", flag
        # translation to AutoIt return values
        if retval == 256:
            retval = 2
        elif retval == 0:
            retval = 1
        return retval

