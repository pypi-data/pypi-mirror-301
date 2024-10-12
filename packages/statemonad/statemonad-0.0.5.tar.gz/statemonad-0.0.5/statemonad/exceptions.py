from dataclasses import dataclass


@dataclass
class StateMonadOperatorException(Exception):
    message: str
