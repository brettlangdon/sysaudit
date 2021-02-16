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
