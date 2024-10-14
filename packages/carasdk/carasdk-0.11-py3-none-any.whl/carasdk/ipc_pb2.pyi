from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IPCCommand(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    IPC_COMMAND_REQUEST: _ClassVar[IPCCommand]
    IPC_COMMAND_RESPONSE: _ClassVar[IPCCommand]
    IPC_COMMAND_EVENT: _ClassVar[IPCCommand]
    IPC_COMMAND_REGISTER_SERVICE: _ClassVar[IPCCommand]
    IPC_COMMAND_REGISTER_HANDLER: _ClassVar[IPCCommand]
    IPC_COMMAND_UNREGISTER_SERVICE: _ClassVar[IPCCommand]
    IPC_COMMAND_UNREGISTER_HANDLER: _ClassVar[IPCCommand]
IPC_COMMAND_REQUEST: IPCCommand
IPC_COMMAND_RESPONSE: IPCCommand
IPC_COMMAND_EVENT: IPCCommand
IPC_COMMAND_REGISTER_SERVICE: IPCCommand
IPC_COMMAND_REGISTER_HANDLER: IPCCommand
IPC_COMMAND_UNREGISTER_SERVICE: IPCCommand
IPC_COMMAND_UNREGISTER_HANDLER: IPCCommand

class IPCMessage(_message.Message):
    __slots__ = ("command", "content")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    command: IPCCommand
    content: bytes
    def __init__(self, command: _Optional[_Union[IPCCommand, str]] = ..., content: _Optional[bytes] = ...) -> None: ...

class RegisterServiceRequest(_message.Message):
    __slots__ = ("instance_id", "service_name", "action", "category")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    service_name: str
    action: str
    category: str
    def __init__(self, instance_id: _Optional[str] = ..., service_name: _Optional[str] = ..., action: _Optional[str] = ..., category: _Optional[str] = ...) -> None: ...

class UnregisterServiceRequest(_message.Message):
    __slots__ = ("instance_id", "service_name", "action", "category")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    service_name: str
    action: str
    category: str
    def __init__(self, instance_id: _Optional[str] = ..., service_name: _Optional[str] = ..., action: _Optional[str] = ..., category: _Optional[str] = ...) -> None: ...

class RegisterHandlerRequest(_message.Message):
    __slots__ = ("instance_id", "event", "category")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    event: str
    category: str
    def __init__(self, instance_id: _Optional[str] = ..., event: _Optional[str] = ..., category: _Optional[str] = ...) -> None: ...

class UnregisterHandlerRequest(_message.Message):
    __slots__ = ("instance_id", "event", "category")
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    instance_id: str
    event: str
    category: str
    def __init__(self, instance_id: _Optional[str] = ..., event: _Optional[str] = ..., category: _Optional[str] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("request_id", "instance_id", "action", "category", "data", "args")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    instance_id: str
    action: str
    category: str
    data: bytes
    args: str
    def __init__(self, request_id: _Optional[str] = ..., instance_id: _Optional[str] = ..., action: _Optional[str] = ..., category: _Optional[str] = ..., data: _Optional[bytes] = ..., args: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("request_id", "result", "is_ok", "error")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    IS_OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    result: bytes
    is_ok: bool
    error: str
    def __init__(self, request_id: _Optional[str] = ..., result: _Optional[bytes] = ..., is_ok: bool = ..., error: _Optional[str] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("event", "category", "data", "args")
    EVENT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    event: str
    category: str
    data: bytes
    args: str
    def __init__(self, event: _Optional[str] = ..., category: _Optional[str] = ..., data: _Optional[bytes] = ..., args: _Optional[str] = ...) -> None: ...
