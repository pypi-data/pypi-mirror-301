"""
Bunch of stuff
"""
import os

if os.name == 'nt':
    from .scriptlink import *
else:
    from .scriptlinkbasic import *
__version__ = "1.1.0"
__author__ = "Lopht"
__copyright__ = """
    Copyright (c) 2020-2024, Advasoft
"""
