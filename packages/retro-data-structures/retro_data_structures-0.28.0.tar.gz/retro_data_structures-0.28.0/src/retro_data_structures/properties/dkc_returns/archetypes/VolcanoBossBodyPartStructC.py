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

if typing.TYPE_CHECKING:
    class VolcanoBossBodyPartStructCJson(typing_extensions.TypedDict):
        unknown_0x64543b0c: int
        unknown_0x1e67101c: int
        unknown_0xcb515e2a: int
        unknown_0xc762476c: int
        unknown_0xb6641bf0: int
        unknown_0x217a54b9: int
        unknown_0x8b30d933: int
    

_FAST_FORMAT = None
_FAST_IDS = (0x64543b0c, 0x1e67101c, 0xcb515e2a, 0xc762476c, 0xb6641bf0, 0x217a54b9, 0x8b30d933)


@dataclasses.dataclass()
class VolcanoBossBodyPartStructC(BaseProperty):
    unknown_0x64543b0c: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x64543b0c, original_name='Unknown'
        ),
    })
    unknown_0x1e67101c: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x1e67101c, original_name='Unknown'
        ),
    })
    unknown_0xcb515e2a: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xcb515e2a, original_name='Unknown'
        ),
    })
    unknown_0xc762476c: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xc762476c, original_name='Unknown'
        ),
    })
    unknown_0xb6641bf0: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb6641bf0, original_name='Unknown'
        ),
    })
    unknown_0x217a54b9: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x217a54b9, original_name='Unknown'
        ),
    })
    unknown_0x8b30d933: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8b30d933, original_name='Unknown'
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
        if property_count != 7:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHlLHlLHlLHlLHlLHlLHl')
    
        dec = _FAST_FORMAT.unpack(data.read(70))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x07')  # 7 properties

        data.write(b'dT;\x0c')  # 0x64543b0c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x64543b0c))

        data.write(b'\x1eg\x10\x1c')  # 0x1e67101c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x1e67101c))

        data.write(b'\xcbQ^*')  # 0xcb515e2a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xcb515e2a))

        data.write(b'\xc7bGl')  # 0xc762476c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xc762476c))

        data.write(b'\xb6d\x1b\xf0')  # 0xb6641bf0
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0xb6641bf0))

        data.write(b'!zT\xb9')  # 0x217a54b9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x217a54b9))

        data.write(b'\x8b0\xd93')  # 0x8b30d933
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8b30d933))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("VolcanoBossBodyPartStructCJson", data)
        return cls(
            unknown_0x64543b0c=json_data['unknown_0x64543b0c'],
            unknown_0x1e67101c=json_data['unknown_0x1e67101c'],
            unknown_0xcb515e2a=json_data['unknown_0xcb515e2a'],
            unknown_0xc762476c=json_data['unknown_0xc762476c'],
            unknown_0xb6641bf0=json_data['unknown_0xb6641bf0'],
            unknown_0x217a54b9=json_data['unknown_0x217a54b9'],
            unknown_0x8b30d933=json_data['unknown_0x8b30d933'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x64543b0c': self.unknown_0x64543b0c,
            'unknown_0x1e67101c': self.unknown_0x1e67101c,
            'unknown_0xcb515e2a': self.unknown_0xcb515e2a,
            'unknown_0xc762476c': self.unknown_0xc762476c,
            'unknown_0xb6641bf0': self.unknown_0xb6641bf0,
            'unknown_0x217a54b9': self.unknown_0x217a54b9,
            'unknown_0x8b30d933': self.unknown_0x8b30d933,
        }


def _decode_unknown_0x64543b0c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x1e67101c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xcb515e2a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xc762476c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0xb6641bf0(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x217a54b9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x8b30d933(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x64543b0c: ('unknown_0x64543b0c', _decode_unknown_0x64543b0c),
    0x1e67101c: ('unknown_0x1e67101c', _decode_unknown_0x1e67101c),
    0xcb515e2a: ('unknown_0xcb515e2a', _decode_unknown_0xcb515e2a),
    0xc762476c: ('unknown_0xc762476c', _decode_unknown_0xc762476c),
    0xb6641bf0: ('unknown_0xb6641bf0', _decode_unknown_0xb6641bf0),
    0x217a54b9: ('unknown_0x217a54b9', _decode_unknown_0x217a54b9),
    0x8b30d933: ('unknown_0x8b30d933', _decode_unknown_0x8b30d933),
}
