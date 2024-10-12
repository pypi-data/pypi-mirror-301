from abc import abstractmethod

from statemonad.statemonadtree.nodes import SingleChildStateMonadNode


class PutMixin[State, U](SingleChildStateMonadNode[State, State, U]):
    def __str__(self) -> str:
        return f'put({self.child})'

    @property
    @abstractmethod
    def state(self) -> State:
        ...

    def apply(self, state: State) -> tuple[State, U]:
        _, value = self.child.apply(state)

        return self.state, value
