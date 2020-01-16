from .identifier import Identifier, ns
from .snippet import Snippet, Const as const
from .chain import Chain
from .format import format_sql as SQL
from .query import *
from .helpers import fn

import sys
sys.modules['squirrel.ns'] = ns
