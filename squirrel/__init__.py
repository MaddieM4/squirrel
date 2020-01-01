from .identifier import Identifier, Chain

ns = Chain()
import sys
sys.modules['squirrel.ns'] = ns
