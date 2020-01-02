from .identifier import Identifier, Chain as IdentChain
from .snippet import Snippet, Const as const
from .chain import Chain
from .format import format_sql as SQL

ns = IdentChain()
import sys
sys.modules['squirrel.ns'] = ns
