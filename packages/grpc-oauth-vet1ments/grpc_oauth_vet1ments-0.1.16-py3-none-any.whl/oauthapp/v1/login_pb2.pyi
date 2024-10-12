from google.api import httpbody_pb2 as _httpbody_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("id", "pw")
    ID_FIELD_NUMBER: _ClassVar[int]
    PW_FIELD_NUMBER: _ClassVar[int]
    id: str
    pw: str
    def __init__(self, id: _Optional[str] = ..., pw: _Optional[str] = ...) -> None: ...

class CallbackRequest(_message.Message):
    __slots__ = ("code", "state")
    CODE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    code: str
    state: str
    def __init__(self, code: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...
