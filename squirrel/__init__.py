from .identifier import Identifier, ns
from .snippet import Snippet, Const as const
from .chain import Chain
from .format import format_sql as SQL

import sys
sys.modules['squirrel.ns'] = ns
