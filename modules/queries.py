import config
from os import path
import sys
sys.path.append(path.abspath('/home/james/backend/app/'))

from app.module import groupComparisons


blazegraph_url = config.database['blazegraph_url']