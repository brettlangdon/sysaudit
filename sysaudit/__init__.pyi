import types
import typing

def audit(event: str, *args: typing.Any) -> None: ...
def addaudithook(
    hook: typing.Callable[[str, typing.Tuple[typing.Any, ...]], None]
) -> None: ...

_audit_fn = typing.Callable[[str, typing.Any], None]
_addaudithook_fn = typing.Callable[
    [typing.Callable[[str, typing.Tuple[typing.Any, ...]], None]], None
]

std_audit = typing.Optional[_audit_fn]
std_addaudithook = typing.Optional[_addaudithook_fn]
csysaudit_audit = typing.Optional[_audit_fn]
csysaudit_addaudithook = typing.Optional[_addaudithook_fn]
py_audit = typing.Optional[_audit_fn]
py_addaudithook = typing.Optional[_addaudithook_fn]

def _subscription_hook(event: str, args: typing.Tuple[typing.Any, ...]) -> None: ...
def subscribe(
    event: str, hook: typing.Callable[[typing.Tuple[typing.Any, ...]], None]
) -> None: ...

class Span:
    # Properties
    name: str
    started: bool
    ended: bool
    data: typing.Optional[typing.Any] = None

    # Span.Message class
    class Message:
        # Properties
        type: str
        span: Span
        data: typing.Optional[typing.Any] = None

        # Methods
        def __init__(
            self, type: str, span: Span, data: typing.Optional[typing.Any] = None
        ): ...
        def __str__(self) -> str: ...
    # Methods
    def __init__(self, name: str, data: typing.Optional[typing.Any] = None): ...
    @property
    def id(self) -> int: ...
    def message(self, type: str, data: typing.Optional[typing.Any] = None) -> None: ...
    def start(self, data: typing.Optional[typing.Any] = None) -> Span: ...
    def end(self, data: typing.Optional[typing.Any] = None) -> None: ...
    def annotate(self, data: typing.Any) -> None: ...
    def __enter__(self) -> Span: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[types.TracebackType],
    ) -> None: ...
    def __str__(self) -> str: ...
