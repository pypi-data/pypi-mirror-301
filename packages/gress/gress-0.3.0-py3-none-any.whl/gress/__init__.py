#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# set version
version = (0, 3, 0)

# import constants
from .enums import *

# import objects
from .bar import Bar
from .widgets import Widget, Callback, Variable, Property
from .widgets import Time, Timer, ETA, Speed
from .widgets import Gauge, Spin

# import utils
from .prebuilds import register
from .utils import format_time, format_power


# init convenient func
def gress(items, *widgets, minimum=0, maximum=None, size=80, refresh=0.5, sample=10, output=None):
    """
    Initializes a new instance of the progress Bar monitor class and returns its
    iterator filled by given items
    
    Args:
        widgets: (Widget,) or str
            Collection of widgets to display on each update. The widget can
            be one of the many predefined widgets, simple string to show or
            any class derived from the Widget base. The widgets can also be
            provided using a template, where the widgets are specified by a
            name in curly brackets (e.g. 'Processed: {count} ETA: {eta}').
        
        minimum: int or float
            Minimum progress value or count.
        
        maximum: int, float or None
            Maximum progress value or count.
        
        size: int
            Number of characters available to display the progress.
        
        refresh: float
            Minimum number of seconds between individual updates to be
            displayed.
        
        sample: int
            Number of last sample to keep for adaptive widgets like ETA
            or speed. Such widgets are calculating progress from last
            measurements instead of overall progress.
        
        output: any
            Custom output to which all the progress and messages are writen.
            This must support 'write' and 'flush' method calls.
    """
    
    # get maximum
    if maximum is None and hasattr(items, '__len__'):
        maximum = len(items)
    
    # init bar
    bar = Bar(
        *widgets,
        minimum = minimum,
        maximum = maximum,
        size = size,
        refresh = refresh,
        sample = sample,
        output = output)
    
    # init iterator
    return bar(items)
