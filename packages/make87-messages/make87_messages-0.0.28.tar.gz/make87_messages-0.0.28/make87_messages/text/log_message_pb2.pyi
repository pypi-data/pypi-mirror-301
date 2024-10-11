from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogMessage(_message.Message):
    __slots__ = ["file_name", "level", "line_number", "message", "process_id", "source", "thread_id", "timestamp"]
    class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    CRITICAL: LogMessage.LogLevel
    DEBUG: LogMessage.LogLevel
    ERROR: LogMessage.LogLevel
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    INFO: LogMessage.LogLevel
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LINE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WARNING: LogMessage.LogLevel
    file_name: str
    level: LogMessage.LogLevel
    line_number: int
    message: str
    process_id: int
    source: str
    thread_id: int
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., level: _Optional[_Union[LogMessage.LogLevel, str]] = ..., message: _Optional[str] = ..., source: _Optional[str] = ..., file_name: _Optional[str] = ..., line_number: _Optional[int] = ..., process_id: _Optional[int] = ..., thread_id: _Optional[int] = ...) -> None: ...
