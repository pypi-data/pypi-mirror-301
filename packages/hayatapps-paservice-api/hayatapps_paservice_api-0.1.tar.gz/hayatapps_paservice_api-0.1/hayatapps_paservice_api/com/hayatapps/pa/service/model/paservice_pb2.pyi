from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PAService(_message.Message):
    __slots__ = ("service_id", "service_title", "created_at")
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TITLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    service_id: int
    service_title: str
    created_at: str
    def __init__(self, service_id: _Optional[int] = ..., service_title: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...
