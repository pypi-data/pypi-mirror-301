__ver__ = '1.0.7'

import platform

if platform.system() == 'Windows':
    from .win import get_window_size

from .data import AttrDict
from .db import DataCache, DataStore
from .net import PCap, Packet, download