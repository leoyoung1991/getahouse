#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

def Log(msg):
    logging.basicConfig(filename='house.log',level=logging.INFO)
    logging.info(msg)
