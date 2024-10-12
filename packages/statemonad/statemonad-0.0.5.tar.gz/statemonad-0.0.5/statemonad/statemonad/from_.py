from typing import Callable, Iterable

from statemonad.statemonadtree.init import init_from
from statemonad.statemonad.statemonad import StateMonad
from statemonad.statemonad.init import init_state_monad


class from_[State]:
    """
    This function (implemented as function to enable better type hinting) creates a constant state monad.
    It sets the return value to `value` while leaving the state unchanged.
    """
    
    def __new__[U](_, value: U) -> StateMonad[State, U]:
        return init_state_monad(child=init_from(value=value))


class get[State]:
    """
    This function (implemented as function to enable better type hinting) returns the state while leaving
    the state unchanged.
    """
        
    def __new__(_) -> StateMonad[State, State]:
        return from_[State](None).get()


class put[State]:        
    def __new__(_, state: State) -> StateMonad[State, None]:
        return from_[State](None).put(state=state)
    

def get_map_put[State, U](
        func: Callable[[State], tuple[State, U]],
) -> StateMonad[State, U]:
    def put_state(state_value_pair):
        state, value = state_value_pair
        return put(state).flat_map(lambda _: from_(value))

    return get().map(func).flat_map(put_state)


def zip[State, U](
    monads: Iterable[StateMonad[State, U]],
):
    """
    Combine multiple state monads into a single monad that evaluates each
    one and returns their result as a tuple.

    This function takes an iterable of state monads and produces a new state monad
    that, when applied to a state, runs each of the original monads in sequence
    with the same initial state. The final state is derived from the sequence, and
    the result is a tuple of all the values produced by the monads.

    Example:
    ``` python
    m1, m2, m3 = from_(1), from_(2), from_(3)

    state, value = zip((m1, m2, m3)).apply(state)

    print(value)  # Output will be (1, 2, 3)
    ```
    """

    monads_tuple = tuple(monads)

    match len(monads_tuple):
        case 0:
            return from_[State](tuple[U]())
        case 1:
            return monads_tuple[0].map(lambda v: (v,))
        case _:
            return monads_tuple[0].zip(monads_tuple[1:])

