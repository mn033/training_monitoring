"""
training_monitoring
~~~~~~~.
"""

__version__ = '0.1'
__author__ = 'jgru'


from .parsers import TrainingDataParser, XlsParser
from .plotter import Plotter
from .training_constants import *
from .training_monitor import create_training_stats
