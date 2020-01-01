from .identifier import Identifier, Chain
from .snippet import Snippet, Const as const

ns = Chain()
import sys
sys.modules['squirrel.ns'] = ns
