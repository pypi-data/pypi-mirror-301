from __future__ import annotations

from dataclasses import replace
from typing import override
from dataclassabc import dataclassabc

from statemonad.statemonad.statemonad import StateMonad
from statemonad.statemonadtree.nodes import StateMonadNode


@dataclassabc(frozen=True, slots=True)
class StateMonadImpl[State, U](StateMonad[State, U]):
    child: StateMonadNode[State, U]

    def __str__(self) -> str:
        return f"StateMonad({self.child})"

    @override
    def copy(self, /, **changes) -> StateMonad[State, U]:
        return replace(self, **changes)


def init_state_monad[State, U](child: StateMonadNode[State, U]):
    return StateMonadImpl(child=child)
