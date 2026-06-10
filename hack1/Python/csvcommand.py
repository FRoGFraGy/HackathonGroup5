# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:50:23 2026

@author: chano
"""

with open("cart_web.log", "r") as fin, open("cart_web.csv", "w") as fout:
    for line in fin:
        fout.write(line.replace("|", ","))
