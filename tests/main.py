#!/usr/bin/python
# -*- coding: utf-8 -*-
#vim: set enc=utf8:

import sys
from pymatic.scripting import Automation, Settings, NaiveInterpreter, ScriptFiles

def test1():
    auto = Automation(Settings(300))
    auto.startapp("gedit")
    auto.alttab()
    auto.say("Hello World!")
    auto.close()

def test2():
    sf = ScriptFiles("../scripts")
    sf.runscriptbyfirstname("helloworlds", Settings())

def test3():
    script = """
    msgbox("hello world")
    msgbox("hi there")
    """
    interp = NaiveInterpreter(Settings())
    interp.run_this(script)
    interp.close()

def test4():
    # TODO An environment variable for where to look for files
    settings = Settings()
    sf = ScriptFiles("../scripts")
    sf.runscriptbyfirstname("startcgoban", settings)

def test5():
    # nonfunctional test
    # login
    settings = Settings()
    sf = ScriptFiles("../scripts")
    print "starting in the background..."
    sf.runscriptbyfirstname("startcgoban", settings)
    print "started? alt tab now"
    auto = Automation(settings)
    auto.alttab()
    print "sending a click"
    emu = auto.getemu()
    emu.move(100, 500)
    emu.click()
    auto.close()

def test6():
    settings = Settings()
    sf = ScriptFiles("../scripts")
    print "Starting Cgoban..."
    sf.runscriptbyfirstname("startcgoban_xvfb", settings)
    sf.runscriptbyfirstname("login", settings)
    sf.runscriptbyfirstname("killxvfb", settings)

def main():
    if len(sys.argv) > 1:
        scriptfirstname = sys.argv[1].strip()
        settings = Settings()
        sf = ScriptFiles("../scripts")
        sf.runscriptbyfirstname(scriptfirstname, settings)
    else:
        test1()
        #test2()
        #test3()
        #test4()
        #test5()
        #test6()

if __name__ == "__main__":
    main()
