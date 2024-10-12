from abc import abstractmethod

from statemonad.statemonadtree.nodes import StateMonadNode


class FromMixin[State, U](StateMonadNode[State, U]):
    def __str__(self) -> str:
        return f'from({self.value})'

    @property
    @abstractmethod
    def value(self) -> U:
        ...

    def apply(self, state: State) -> tuple[State, U]:
        return state, self.value
