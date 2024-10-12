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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class KongProxyDataJson(typing_extensions.TypedDict):
        unknown_0x9445eea3: bool
        unknown_0x80bc66ea: bool
        unknown_0x30060f67: int
        unknown_0x2f026a4f: int
        gravity_multiplier: float
        unknown_0x653fba4a: float
        maximum_run_speed: float
        acceleration: float
        unknown_0x14e317bd: json_util.JsonValue
    

_FAST_FORMAT = None
_FAST_IDS = (0x9445eea3, 0x80bc66ea, 0x30060f67, 0x2f026a4f, 0x42ac42ea, 0x653fba4a, 0x950a7b96, 0x39fb7978, 0x14e317bd)


@dataclasses.dataclass()
class KongProxyData(BaseProperty):
    unknown_0x9445eea3: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9445eea3, original_name='Unknown'
        ),
    })
    unknown_0x80bc66ea: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x80bc66ea, original_name='Unknown'
        ),
    })
    unknown_0x30060f67: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x30060f67, original_name='Unknown'
        ),
    })
    unknown_0x2f026a4f: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x2f026a4f, original_name='Unknown'
        ),
    })
    gravity_multiplier: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x42ac42ea, original_name='GravityMultiplier'
        ),
    })
    unknown_0x653fba4a: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x653fba4a, original_name='Unknown'
        ),
    })
    maximum_run_speed: float = dataclasses.field(default=9.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x950a7b96, original_name='MaximumRunSpeed'
        ),
    })
    acceleration: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x39fb7978, original_name='Acceleration'
        ),
    })
    unknown_0x14e317bd: Vector = dataclasses.field(default_factory=lambda: Vector(x=32.0, y=12.0, z=24.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x14e317bd, original_name='Unknown', from_json=Vector.from_json, to_json=Vector.to_json
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
        if property_count != 9:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LHlLHlLHfLHfLHfLHfLHfff')
    
        dec = _FAST_FORMAT.unpack(data.read(92))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            Vector(*dec[26:29]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x94E\xee\xa3')  # 0x9445eea3
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x9445eea3))

        data.write(b'\x80\xbcf\xea')  # 0x80bc66ea
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x80bc66ea))

        data.write(b'0\x06\x0fg')  # 0x30060f67
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x30060f67))

        data.write(b'/\x02jO')  # 0x2f026a4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x2f026a4f))

        data.write(b'B\xacB\xea')  # 0x42ac42ea
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity_multiplier))

        data.write(b'e?\xbaJ')  # 0x653fba4a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x653fba4a))

        data.write(b'\x95\n{\x96')  # 0x950a7b96
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_run_speed))

        data.write(b'9\xfbyx')  # 0x39fb7978
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.acceleration))

        data.write(b'\x14\xe3\x17\xbd')  # 0x14e317bd
        data.write(b'\x00\x0c')  # size
        self.unknown_0x14e317bd.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("KongProxyDataJson", data)
        return cls(
            unknown_0x9445eea3=json_data['unknown_0x9445eea3'],
            unknown_0x80bc66ea=json_data['unknown_0x80bc66ea'],
            unknown_0x30060f67=json_data['unknown_0x30060f67'],
            unknown_0x2f026a4f=json_data['unknown_0x2f026a4f'],
            gravity_multiplier=json_data['gravity_multiplier'],
            unknown_0x653fba4a=json_data['unknown_0x653fba4a'],
            maximum_run_speed=json_data['maximum_run_speed'],
            acceleration=json_data['acceleration'],
            unknown_0x14e317bd=Vector.from_json(json_data['unknown_0x14e317bd']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x9445eea3': self.unknown_0x9445eea3,
            'unknown_0x80bc66ea': self.unknown_0x80bc66ea,
            'unknown_0x30060f67': self.unknown_0x30060f67,
            'unknown_0x2f026a4f': self.unknown_0x2f026a4f,
            'gravity_multiplier': self.gravity_multiplier,
            'unknown_0x653fba4a': self.unknown_0x653fba4a,
            'maximum_run_speed': self.maximum_run_speed,
            'acceleration': self.acceleration,
            'unknown_0x14e317bd': self.unknown_0x14e317bd.to_json(),
        }


def _decode_unknown_0x9445eea3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x80bc66ea(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_unknown_0x30060f67(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_unknown_0x2f026a4f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_gravity_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x653fba4a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_run_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x14e317bd(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x9445eea3: ('unknown_0x9445eea3', _decode_unknown_0x9445eea3),
    0x80bc66ea: ('unknown_0x80bc66ea', _decode_unknown_0x80bc66ea),
    0x30060f67: ('unknown_0x30060f67', _decode_unknown_0x30060f67),
    0x2f026a4f: ('unknown_0x2f026a4f', _decode_unknown_0x2f026a4f),
    0x42ac42ea: ('gravity_multiplier', _decode_gravity_multiplier),
    0x653fba4a: ('unknown_0x653fba4a', _decode_unknown_0x653fba4a),
    0x950a7b96: ('maximum_run_speed', _decode_maximum_run_speed),
    0x39fb7978: ('acceleration', _decode_acceleration),
    0x14e317bd: ('unknown_0x14e317bd', _decode_unknown_0x14e317bd),
}
