# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from abc import ABC
from enum import Enum
from typing import cast, Any, Generic, Optional, TypeVar

from google.protobuf.message import Message

P = TypeVar("P", bound=Message)
C = TypeVar("C")


# We mainly need this to statically declare to the linter that these
# attributes will eventually exist.
class ProtoWrapperBase(ABC):
    def __init__(self, proto_type: Optional[Message] = None):
        pass


class ProtoWrapper(Generic[P]):
    def __init__(decorator, proto_type: type[P]):
        decorator.proto_type = proto_type

    def __call__(decorator, cls: type[C]) -> type[C]:
        class _W(cls):  # type: ignore
            def __init__(self, proto: Optional[P] = None):
                if proto is None:
                    proto = decorator.proto_type()
                self._proto = cast(P, proto)

            def __str__(self) -> str:
                return self._proto.__str__()

            def __repr__(self) -> str:
                return self._proto.__repr__()

        # This binds the field name to the getter.
        def getter(field_name: str) -> Any:
            return lambda self: getattr(self._proto, field_name)

        def wrapped_getter(field_name: str, wrapper: Any) -> Any:
            return lambda self: wrapper(getattr(self._proto, field_name))

        # Create getters that access the attributes of the underlying proto.
        for field in decorator.proto_type.DESCRIPTOR.fields:
            _type = cls.__annotations__.get(field.name)
            if _type:
                if issubclass(_type, Enum) or issubclass(_type, ProtoWrapperBase):
                    fget = wrapped_getter(field.name, _type)
                else:
                    fget = getter(field.name)
                setattr(_W, field.name, property(fget=fget))

        # Rename the wrapped class.
        _W.__name__ = cls.__name__

        return cast(type[C], _W)
