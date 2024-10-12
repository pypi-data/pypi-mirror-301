from typing import Any, Callable
from dataclassabc import dataclassabc

from statemonad.statemonadtree.nodes import StateMonadNode
from statemonad.statemonadtree.operations.flatmapmixin import FlatMapMixin
from statemonad.statemonadtree.operations.frommixin import FromMixin
from statemonad.statemonadtree.operations.getmixin import GetMixin
from statemonad.statemonadtree.operations.mapmixin import MapMixin
from statemonad.statemonadtree.operations.putmixin import PutMixin
from statemonad.statemonadtree.operations.zipmixin import ZipMixin
from statemonad.utils.getstacklines import FrameSummary


@dataclassabc(frozen=True, repr=False)
class FlatMapImpl[State, U, ChildU](FlatMapMixin[State, U, ChildU]):
    child: StateMonadNode[State, ChildU]
    func: Callable[[ChildU], StateMonadNode[State, U]]
    stack: tuple[FrameSummary, ...]


init_flat_map = FlatMapImpl


@dataclassabc(frozen=True, slots=True)
class FromImpl[State, U](FromMixin[State, U]):
    value: U


init_from = FromImpl


@dataclassabc(frozen=True, slots=True)
class GetImpl[State](GetMixin[State]):
    child: StateMonadNode[State, Any]


init_get = GetImpl


@dataclassabc(frozen=True, repr=False)
class MapImpl[State, U, ChildU](MapMixin[State, U, ChildU]):
    child: StateMonadNode[State, ChildU]
    func: Callable[[ChildU], U]
    stack: tuple[FrameSummary, ...]


init_map = MapImpl


@dataclassabc(frozen=True, slots=True)
class PutImpl[State, U](PutMixin[State, U]):
    child: StateMonadNode[State, U]
    state: State


init_put = PutImpl


@dataclassabc(frozen=True, slots=True)
class ZipImpl[State, U](ZipMixin[State, U]):
    children: tuple[StateMonadNode[State, U], ...]


init_zip = ZipImpl


