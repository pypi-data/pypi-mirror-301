from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRGBA(_message.Message):
    __slots__ = ["height", "pixels", "timestamp", "width"]
    class Pixel(_message.Message):
        __slots__ = ["alpha", "blue", "green", "red"]
        ALPHA_FIELD_NUMBER: _ClassVar[int]
        BLUE_FIELD_NUMBER: _ClassVar[int]
        GREEN_FIELD_NUMBER: _ClassVar[int]
        RED_FIELD_NUMBER: _ClassVar[int]
        alpha: int
        blue: int
        green: int
        red: int
        def __init__(self, red: _Optional[int] = ..., green: _Optional[int] = ..., blue: _Optional[int] = ..., alpha: _Optional[int] = ...) -> None: ...
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PIXELS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    height: int
    pixels: _containers.RepeatedCompositeFieldContainer[ImageRGBA.Pixel]
    timestamp: _timestamp_pb2.Timestamp
    width: int
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., pixels: _Optional[_Iterable[_Union[ImageRGBA.Pixel, _Mapping]]] = ...) -> None: ...
