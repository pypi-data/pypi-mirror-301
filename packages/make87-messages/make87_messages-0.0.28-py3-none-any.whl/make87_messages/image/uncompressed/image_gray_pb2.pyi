from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageGray(_message.Message):
    __slots__ = ["height", "pixels", "timestamp", "width"]
    class Pixel(_message.Message):
        __slots__ = ["intensity"]
        INTENSITY_FIELD_NUMBER: _ClassVar[int]
        intensity: int
        def __init__(self, intensity: _Optional[int] = ...) -> None: ...
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    height: int
    pixels: _containers.RepeatedCompositeFieldContainer[ImageGray.Pixel]
    timestamp: _timestamp_pb2.Timestamp
    width: int
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., pixels: _Optional[_Iterable[_Union[ImageGray.Pixel, _Mapping]]] = ...) -> None: ...
