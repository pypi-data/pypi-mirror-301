from __future__ import annotations

from abc import abstractmethod
from typing import Callable, override

from statemonad.statemonadtree.nodes import SingleChildStateMonadNode, StateMonadNode
from statemonad.statemonadtree.init import (
    init_flat_map,
    init_get,
    init_map,
    init_put,
    init_zip,
)
from statemonad.utils.getstacklines import get_frame_summary


class StateMonad[State, U](
    SingleChildStateMonadNode[State, U, U]
):
    """
    The StateMonad class implements a dot notation syntax, providing convenient methods to define and 
    chain monadic operations.
    """

    @override
    def apply(self, state: State) -> tuple[State, U]:
        return self.child.apply(state)

    @abstractmethod
    def copy(self, /, **changes) -> StateMonad: ...

    # operations
    ############

    def flat_map[V](
        self, func: Callable[[U], StateMonadNode[State, V]]
    ) -> StateMonad:
        return self.copy(child=init_flat_map(child=self.child, func=func, stack=get_frame_summary()))

    def get(self) -> StateMonad:
        return self.copy(child=init_get(child=self.child))

    def map[V](self, func: Callable[[U], V]) -> StateMonad:
        return self.copy(child=init_map(child=self.child, func=func, stack=get_frame_summary()))

    def put(self, state: State) -> StateMonad:
        return self.copy(child=init_put(child=self.child, state=state))

    def zip(self, others: tuple[StateMonad[State, U], ...]) -> StateMonad[State, tuple[U, ...]]:
        return self.copy(child=init_zip(children=(self,) + others))
