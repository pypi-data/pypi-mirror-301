"""mince is a toolkit for slicing up data into bite-sized dashboards"""

__version__ = '0.2.1'

import typing

from .dashboards.dashboard import Dashboard

if typing.TYPE_CHECKING:
    from .types import *
