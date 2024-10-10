from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Token(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class TokenStatus(_message.Message):
    __slots__ = ("valid",)
    VALID_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    def __init__(self, valid: bool = ...) -> None: ...
