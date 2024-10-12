from itertools import accumulate
from statemonad.statemonadtree.nodes import MultiChildrenStateMonadNode, TwoChildrenStateMonadNode


class ZipMixin[State, U](MultiChildrenStateMonadNode[State, tuple[U, ...], U]):
    def __str__(self) -> str:
        return f'zip({self.children})'

    def apply(self, state: State) -> tuple[State, tuple[U, ...]]:
        zipped_values = []

        for child in self.children:
            state, value = child.apply(state)
            zipped_values.append(value)

        return state, tuple(zipped_values)
    

# class ZipMixin[State, L, R](TwoChildrenStateMonadNode[State, tuple[L, R], L, R]):
#     def __str__(self) -> str:
#         return f'zip({self.left}, {self.right})'

#     def apply(self, state: State) -> tuple[State, tuple[L, R]]:
#         state, left = self.left.apply(state)
#         state, right = self.right.apply(state)

#         return state, (left, right)

