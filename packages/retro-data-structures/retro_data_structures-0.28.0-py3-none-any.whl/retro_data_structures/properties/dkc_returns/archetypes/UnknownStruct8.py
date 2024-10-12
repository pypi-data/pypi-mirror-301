# Generated File
from __future__ import annotations

import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseProperty
from retro_data_structures.properties.field_reflection import FieldReflection
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct7 import UnknownStruct7

if typing.TYPE_CHECKING:
    class UnknownStruct8Json(typing_extensions.TypedDict):
        num_attachments: int
        unknown: bool
        attachment1: json_util.JsonObject
        attachment2: json_util.JsonObject
        attachment3: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct8(BaseProperty):
    num_attachments: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xc2ad5735, original_name='NumAttachments'
        ),
    })
    unknown: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6351a049, original_name='Unknown'
        ),
    })
    attachment1: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7, metadata={
        'reflection': FieldReflection[UnknownStruct7](
            UnknownStruct7, id=0xdaa9d4be, original_name='Attachment1', from_json=UnknownStruct7.from_json, to_json=UnknownStruct7.to_json
        ),
    })
    attachment2: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7, metadata={
        'reflection': FieldReflection[UnknownStruct7](
            UnknownStruct7, id=0xf361604c, original_name='Attachment2', from_json=UnknownStruct7.from_json, to_json=UnknownStruct7.to_json
        ),
    })
    attachment3: UnknownStruct7 = dataclasses.field(default_factory=UnknownStruct7, metadata={
        'reflection': FieldReflection[UnknownStruct7](
            UnknownStruct7, id=0x5d09f1dd, original_name='Attachment3', from_json=UnknownStruct7.from_json, to_json=UnknownStruct7.to_json
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        property_count = struct.unpack(">H", data.read(2))[0]
        if (result := cls._fast_decode(data, property_count)) is not None:
            return result

        present_fields = default_override or {}
        for _ in range(property_count):
            property_id, property_size = struct.unpack(">LH", data.read(6))
            start = data.tell()
            try:
                property_name, decoder = _property_decoder[property_id]
                present_fields[property_name] = decoder(data, property_size)
            except KeyError:
                raise RuntimeError(f"Unknown property: 0x{property_id:08x}")
            assert data.tell() - start == property_size

        return cls(**present_fields)

    @classmethod
    def _fast_decode(cls, data: typing.BinaryIO, property_count: int) -> typing_extensions.Self | None:
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc2ad5735
        num_attachments = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6351a049
        unknown = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdaa9d4be
        attachment1 = UnknownStruct7.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf361604c
        attachment2 = UnknownStruct7.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5d09f1dd
        attachment3 = UnknownStruct7.from_stream(data, property_size)
    
        return cls(num_attachments, unknown, attachment1, attachment2, attachment3)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xc2\xadW5')  # 0xc2ad5735
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_attachments))

        data.write(b'cQ\xa0I')  # 0x6351a049
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown))

        data.write(b'\xda\xa9\xd4\xbe')  # 0xdaa9d4be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachment1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf3a`L')  # 0xf361604c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachment2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\t\xf1\xdd')  # 0x5d09f1dd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.attachment3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct8Json", data)
        return cls(
            num_attachments=json_data['num_attachments'],
            unknown=json_data['unknown'],
            attachment1=UnknownStruct7.from_json(json_data['attachment1']),
            attachment2=UnknownStruct7.from_json(json_data['attachment2']),
            attachment3=UnknownStruct7.from_json(json_data['attachment3']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'num_attachments': self.num_attachments,
            'unknown': self.unknown,
            'attachment1': self.attachment1.to_json(),
            'attachment2': self.attachment2.to_json(),
            'attachment3': self.attachment3.to_json(),
        }


def _decode_num_attachments(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc2ad5735: ('num_attachments', _decode_num_attachments),
    0x6351a049: ('unknown', _decode_unknown),
    0xdaa9d4be: ('attachment1', UnknownStruct7.from_stream),
    0xf361604c: ('attachment2', UnknownStruct7.from_stream),
    0x5d09f1dd: ('attachment3', UnknownStruct7.from_stream),
}
