from abc import abstractmethod
import traceback

from dataclasses import dataclass
from dataclasses import fields


@dataclass(frozen=True)
class FrameSummary:
    filename: str
    lineno: int | None
    name: str
    line: str | None


def get_frame_summary(index: int = 3) -> tuple[FrameSummary, ...]:
    def gen_stack_lines():
        for obj in traceback.extract_stack()[:-index]:
            if '<frozen ' not in obj.filename:
                yield FrameSummary(
                    filename=obj.filename,
                    lineno=obj.lineno,
                    name=obj.name,
                    line=obj.line,
                )

    return tuple(gen_stack_lines())


def to_operator_traceback(
    stack: tuple[FrameSummary, ...],
) -> str:
    assert stack is not None

    traceback_line = (
        "StateMonad Operation Traceback (most recent call last):",
        *(
            f'  File "{stack_line.filename}", line {stack_line.lineno}\n    {stack_line.line}'
            for stack_line in stack
        ),
    )

    return "\n".join(traceback_line)


def to_operator_exception_message(stack: tuple[FrameSummary, ...]):
    message = (
        'State Monad operator exception caught. '
        'See the traceback below for details on the operator call stack.'
        '\n'
    )
    traceback = to_operator_traceback(stack=stack)
    return f'{message}\n{traceback}'


class FrameSummaryMixin:
    @property
    @abstractmethod
    def stack(self) -> tuple[FrameSummary, ...]:
        ...

    # implement custom __repr__ method that returns a representation without the stack
    def __repr__(self):
        fields_str = ','.join(f'{field.name}={repr(getattr(self, field.name))}' for field in fields(self) if field.name != 'stack') # type: ignore

        return f"{self.__class__.__name__}({fields_str})"
    
    def to_operator_exception_message(self):
        return to_operator_exception_message(self.stack)
