from .identifier import Identifier, Chain as IdentChain
from .snippet import Snippet, Const as const
from .chain import Chain

ns = IdentChain()
import sys
sys.modules['squirrel.ns'] = ns
