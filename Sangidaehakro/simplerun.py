from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import optparse
import random
import matplotlib.pyplot as plt
from xml.etree.ElementTree import parse
from collections import defaultdict
from matplotlib.ticker import MaxNLocator

from sumolib import checkBinary
import traci

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'],'tools')
    print(tools)
    sys.path.append(tools)
else:
    sys.exit('Declare environment variable "SUMO_HOME"')
