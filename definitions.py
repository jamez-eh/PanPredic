#!/usr/bin/env python

"""
    Definitions for the ectyper project
"""

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER_CONFIG = os.path.join(ROOT_DIR, 'logging.conf')
DATA_DIR = os.path.join(ROOT_DIR, 'Data/')

PAN_RESULTS = os.path.join(ROOT_DIR, '/modules/PanPredic/panResults')
NOVEL_RESULTS = os.path.join(ROOT_DIR, '/modules/PanPredic/novelResults')