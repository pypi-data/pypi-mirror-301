from typing import Any
from statemonad.statemonadtree.nodes import SingleChildStateMonadNode


class GetMixin[State](SingleChildStateMonadNode[State, State, Any]):
    def __str__(self) -> str:
        return 'get'

    def apply(self, state: State) -> tuple[State, State]:
        state, _ = self.child.apply(state)

        return state, state
