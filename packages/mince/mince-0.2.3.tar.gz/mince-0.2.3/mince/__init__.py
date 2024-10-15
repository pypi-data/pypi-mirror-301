"""mince is a toolkit for slicing up data into bite-sized dashboards"""

__version__ = '0.2.3'

import typing

from .dashboards import Dashboard
from .ops import collect_dashboard_data, run_dashboard

if typing.TYPE_CHECKING:
    from .types import *
