#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 surfer <surfer@LinuxMint>
#
# Distributed under terms of the MIT license.

"""


"""
import os 
pid = os.fork()
if pid == 0:
    print "this is a child"
else:
    print "this is a father"

