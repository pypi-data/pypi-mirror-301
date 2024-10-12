from __future__ import annotations

from statemonad.statemonad.statemonad import StateMonad
from statemonad.statemonadtree.nodes import StateMonadNode

def init_state_monad[State, U](
    child: StateMonadNode[State, U],
) -> StateMonad[State, U]: ...
