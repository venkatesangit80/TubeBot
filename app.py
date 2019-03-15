#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:29:59 2019

@author: venkatesansubramanian
"""

from flask import Flask
app = Flask(__name__)

@app.route('/home')
def home():
    return "Hello Tube"

app.run()