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
    class SwoopBehaviorDataJson(typing_extensions.TypedDict):
        unknown_0x23057384: bool
        unknown_0x875d59f9: bool
        swoop_towards_target: bool
        unknown_0xc7a07e1c: bool
        unknown_0x18c4d552: float
        unknown_0x3ce63601: float
        unknown_0xcdf6ebf3: float
        unknown_0x80842977: float
        unknown_0x8910e24c: float
        drop: float
        unknown_0x5974d648: float
        unknown_0x00c3f023: float
        unknown_0xdcfa472a: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x23057384, 0x875d59f9, 0x11f728a1, 0xc7a07e1c, 0x18c4d552, 0x3ce63601, 0xcdf6ebf3, 0x80842977, 0x8910e24c, 0xda6b7f2, 0x5974d648, 0xc3f023, 0xdcfa472a)


@dataclasses.dataclass()
class SwoopBehaviorData(BaseProperty):
    unknown_0x23057384: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x23057384, original_name='Unknown'
        ),
    })
    unknown_0x875d59f9: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x875d59f9, original_name='Unknown'
        ),
    })
    swoop_towards_target: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x11f728a1, original_name='SwoopTowardsTarget'
        ),
    })
    unknown_0xc7a07e1c: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc7a07e1c, original_name='Unknown'
        ),
    })
    unknown_0x18c4d552: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x18c4d552, original_name='Unknown'
        ),
    })
    unknown_0x3ce63601: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3ce63601, original_name='Unknown'
        ),
    })
    unknown_0xcdf6ebf3: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcdf6ebf3, original_name='Unknown'
        ),
    })
    unknown_0x80842977: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x80842977, original_name='Unknown'
        ),
    })
    unknown_0x8910e24c: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8910e24c, original_name='Unknown'
        ),
    })
    drop: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0da6b7f2, original_name='Drop'
        ),
    })
    unknown_0x5974d648: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5974d648, original_name='Unknown'
        ),
    })
    unknown_0x00c3f023: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x00c3f023, original_name='Unknown'
        ),
    })
    unknown_0xdcfa472a: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xdcfa472a, original_name='Unknown'
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
        if property_count != 13:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LHfLHfLHfLHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(118))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
            dec[29],
            dec[32],
            dec[35],
            dec[38],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\r')  # 13 properties

        data.write(b'#\x05s\x84')  # 0x23057384
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x23057384))

        data.write(b'\x87]Y\xf9')  # 0x875d59f9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x875d59f9))

        data.write(b'\x11\xf7(\xa1')  # 0x11f728a1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.swoop_towards_target))

        data.write(b'\xc7\xa0~\x1c')  # 0xc7a07e1c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0xc7a07e1c))

        data.write(b'\x18\xc4\xd5R')  # 0x18c4d552
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x18c4d552))

        data.write(b'<\xe66\x01')  # 0x3ce63601
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x3ce63601))

        data.write(b'\xcd\xf6\xeb\xf3')  # 0xcdf6ebf3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcdf6ebf3))

        data.write(b'\x80\x84)w')  # 0x80842977
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x80842977))

        data.write(b'\x89\x10\xe2L')  # 0x8910e24c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x8910e24c))

        data.write(b'\r\xa6\xb7\xf2')  # 0xda6b7f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop))

        data.write(b'Yt\xd6H')  # 0x5974d648
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5974d648))

        data.write(b'\x00\xc3\xf0#')  # 0xc3f023
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x00c3f023))

        data.write(b'\xdc\xfaG*')  # 0xdcfa472a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xdcfa472a))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SwoopBehaviorDataJson", data)
        return cls(
            unknown_0x23057384=json_data['unknown_0x23057384'],
            unknown_0x875d59f9=json_data['unknown_0x875d59f9'],
            swoop_towards_target=json_data['swoop_towards_target'],
            unknown_0xc7a07e1c=json_data['unknown_0xc7a07e1c'],
            unknown_0x18c4d552=json_data['unknown_0x18c4d552'],
            unknown_0x3ce63601=json_data['unknown_0x3ce63601'],
            unknown_0xcdf6ebf3=json_data['unknown_0xcdf6ebf3'],
            unknown_0x80842977=json_data['unknown_0x80842977'],
            unknown_0x8910e24c=json_data['unknown_0x8910e24c'],
            drop=json_data['drop'],
            unknown_0x5974d648=json_data['unknown_0x5974d648'],
            unknown_0x00c3f023=json_data['unknown_0x00c3f023'],
            unknown_0xdcfa472a=json_data['unknown_0xdcfa472a'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x23057384': self.unknown_0x23057384,
            'unknown_0x875d59f9': self.unknown_0x875d59f9,
            'swoop_towards_target': self.swoop_towards_target,
            'unknown_0xc7a07e1c': self.unknown_0xc7a07e1c,
            'unknown_0x18c4d552': self.unknown_0x18c4d552,
            'unknown_0x3ce63601': self.unknown_0x3ce63601,
            'unknown_0xcdf6ebf3': self.unknown_0xcdf6ebf3,
            'unknown_0x80842977': self.unknown_0x80842977,
            'unknown_0x8910e24c': self.unknown_0x8910e24c,
            'drop': self.drop,
            'unknown_0x5974d648': self.unknown_0x5974d648,
            'unknown_0x00c3f023': self.unknown_0x00c3f023,
            'unknown_0xdcfa472a': self.unknown_0xdcfa472a,
        }


def _decode_unknown_0x23057384(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x875d59f9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_swoop_towards_target(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0xc7a07e1c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x18c4d552(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x3ce63601(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcdf6ebf3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x80842977(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x8910e24c(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5974d648(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x00c3f023(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xdcfa472a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x23057384: ('unknown_0x23057384', _decode_unknown_0x23057384),
    0x875d59f9: ('unknown_0x875d59f9', _decode_unknown_0x875d59f9),
    0x11f728a1: ('swoop_towards_target', _decode_swoop_towards_target),
    0xc7a07e1c: ('unknown_0xc7a07e1c', _decode_unknown_0xc7a07e1c),
    0x18c4d552: ('unknown_0x18c4d552', _decode_unknown_0x18c4d552),
    0x3ce63601: ('unknown_0x3ce63601', _decode_unknown_0x3ce63601),
    0xcdf6ebf3: ('unknown_0xcdf6ebf3', _decode_unknown_0xcdf6ebf3),
    0x80842977: ('unknown_0x80842977', _decode_unknown_0x80842977),
    0x8910e24c: ('unknown_0x8910e24c', _decode_unknown_0x8910e24c),
    0xda6b7f2: ('drop', _decode_drop),
    0x5974d648: ('unknown_0x5974d648', _decode_unknown_0x5974d648),
    0xc3f023: ('unknown_0x00c3f023', _decode_unknown_0x00c3f023),
    0xdcfa472a: ('unknown_0xdcfa472a', _decode_unknown_0xdcfa472a),
}
