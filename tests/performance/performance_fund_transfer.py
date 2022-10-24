#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import time
import random


def task():
    print("   ")
    rand = random.randint(1000,2000)
    print(rand, "Started")
    time.sleep(5)
    print(rand, "Done")
    print("------------------------------")
    print ("   ") 

