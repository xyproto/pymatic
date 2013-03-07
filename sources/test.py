#!/usr/bin/python
# -*- coding: utf-8 -*-
#vim: set enc=utf8:

import unittest
from lib.interact import Emulate
import time

class TestInteract(unittest.TestCase):

    def setUp(self):
        self.emu = Emulate()

    def testSleep(self):
        beforesec = int(time.time())
        self.emu.sleepseconds(1)
        aftersec = int(time.time())
        took = aftersec - beforesec
        self.assertTrue((took >= 1) and (took < 5))

    def testUsleep(self):
        beforesec = int(time.time())
        self.emu.sleep(1000)
        aftersec = int(time.time())
        took = aftersec - beforesec
        self.assertTrue((took >= 1) and (took < 5))

    def testSleepseconds(self):
        beforesec = int(time.time())
        self.emu.sleepseconds(1)
        aftersec = int(time.time())
        took = aftersec - beforesec
        self.assertTrue((took >= 1) and (took < 5))

    def testShortwait(self):
        beforetime = time.time()
        self.emu.shortwait()
        aftertime = time.time()
        took = aftertime - beforetime
        self.assertTrue((took >= 0.2) and (took < 1))

    def testLongwait(self):
        beforesec = int(time.time())
        self.emu.longwait()
        aftersec = int(time.time())
        took = aftersec - beforesec
        self.assertTrue((took >= 1) and (took < 5))

def main():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestInteract))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()