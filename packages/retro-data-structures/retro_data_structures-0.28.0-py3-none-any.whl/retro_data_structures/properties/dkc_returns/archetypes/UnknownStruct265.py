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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct265Json(typing_extensions.TypedDict):
        dominance: int
        unknown_0x60d9b1cc: bool
        acceleration_frame: int
        movement_acceleration: float
        max_movement_speed: float
        passive_acceleration: float
        max_passive_speed: float
        stopped_threshold: float
        unknown_0x91b27cb3: float
        balanced_velocity_percentage: json_util.JsonObject
        unknown_0xc355fb9f: float
        unknown_0x3153f656: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct265(BaseProperty):
    dominance: enums.Dominance = dataclasses.field(default=enums.Dominance.Unknown1, metadata={
        'reflection': FieldReflection[enums.Dominance](
            enums.Dominance, id=0xc2ea7c93, original_name='Dominance', from_json=enums.Dominance.from_json, to_json=enums.Dominance.to_json
        ),
    })
    unknown_0x60d9b1cc: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x60d9b1cc, original_name='Unknown'
        ),
    })
    acceleration_frame: enums.AccelerationFrame = dataclasses.field(default=enums.AccelerationFrame.Unknown1, metadata={
        'reflection': FieldReflection[enums.AccelerationFrame](
            enums.AccelerationFrame, id=0xe3a1be31, original_name='AccelerationFrame', from_json=enums.AccelerationFrame.from_json, to_json=enums.AccelerationFrame.to_json
        ),
    })
    movement_acceleration: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfb5cf531, original_name='MovementAcceleration'
        ),
    })
    max_movement_speed: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x004cab64, original_name='MaxMovementSpeed'
        ),
    })
    passive_acceleration: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x26288849, original_name='PassiveAcceleration'
        ),
    })
    max_passive_speed: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x51b03d22, original_name='MaxPassiveSpeed'
        ),
    })
    stopped_threshold: float = dataclasses.field(default=0.009999999776482582, metadata={
        'reflection': FieldReflection[float](
            float, id=0x550574f2, original_name='StoppedThreshold'
        ),
    })
    unknown_0x91b27cb3: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x91b27cb3, original_name='Unknown'
        ),
    })
    balanced_velocity_percentage: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x59299e65, original_name='BalancedVelocityPercentage', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    unknown_0xc355fb9f: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc355fb9f, original_name='Unknown'
        ),
    })
    unknown_0x3153f656: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x3153f656, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
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
        if property_count != 12:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc2ea7c93
        dominance = enums.Dominance.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x60d9b1cc
        unknown_0x60d9b1cc = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe3a1be31
        acceleration_frame = enums.AccelerationFrame.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfb5cf531
        movement_acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x004cab64
        max_movement_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26288849
        passive_acceleration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x51b03d22
        max_passive_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x550574f2
        stopped_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x91b27cb3
        unknown_0x91b27cb3 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x59299e65
        balanced_velocity_percentage = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc355fb9f
        unknown_0xc355fb9f = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3153f656
        unknown_0x3153f656 = Spline.from_stream(data, property_size)
    
        return cls(dominance, unknown_0x60d9b1cc, acceleration_frame, movement_acceleration, max_movement_speed, passive_acceleration, max_passive_speed, stopped_threshold, unknown_0x91b27cb3, balanced_velocity_percentage, unknown_0xc355fb9f, unknown_0x3153f656)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xc2\xea|\x93')  # 0xc2ea7c93
        data.write(b'\x00\x04')  # size
        self.dominance.to_stream(data)

        data.write(b'`\xd9\xb1\xcc')  # 0x60d9b1cc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.unknown_0x60d9b1cc))

        data.write(b'\xe3\xa1\xbe1')  # 0xe3a1be31
        data.write(b'\x00\x04')  # size
        self.acceleration_frame.to_stream(data)

        data.write(b'\xfb\\\xf51')  # 0xfb5cf531
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_acceleration))

        data.write(b'\x00L\xabd')  # 0x4cab64
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_movement_speed))

        data.write(b'&(\x88I')  # 0x26288849
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.passive_acceleration))

        data.write(b'Q\xb0="')  # 0x51b03d22
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_passive_speed))

        data.write(b'U\x05t\xf2')  # 0x550574f2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stopped_threshold))

        data.write(b'\x91\xb2|\xb3')  # 0x91b27cb3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x91b27cb3))

        data.write(b'Y)\x9ee')  # 0x59299e65
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.balanced_velocity_percentage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc3U\xfb\x9f')  # 0xc355fb9f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xc355fb9f))

        data.write(b'1S\xf6V')  # 0x3153f656
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x3153f656.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct265Json", data)
        return cls(
            dominance=enums.Dominance.from_json(json_data['dominance']),
            unknown_0x60d9b1cc=json_data['unknown_0x60d9b1cc'],
            acceleration_frame=enums.AccelerationFrame.from_json(json_data['acceleration_frame']),
            movement_acceleration=json_data['movement_acceleration'],
            max_movement_speed=json_data['max_movement_speed'],
            passive_acceleration=json_data['passive_acceleration'],
            max_passive_speed=json_data['max_passive_speed'],
            stopped_threshold=json_data['stopped_threshold'],
            unknown_0x91b27cb3=json_data['unknown_0x91b27cb3'],
            balanced_velocity_percentage=Spline.from_json(json_data['balanced_velocity_percentage']),
            unknown_0xc355fb9f=json_data['unknown_0xc355fb9f'],
            unknown_0x3153f656=Spline.from_json(json_data['unknown_0x3153f656']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'dominance': self.dominance.to_json(),
            'unknown_0x60d9b1cc': self.unknown_0x60d9b1cc,
            'acceleration_frame': self.acceleration_frame.to_json(),
            'movement_acceleration': self.movement_acceleration,
            'max_movement_speed': self.max_movement_speed,
            'passive_acceleration': self.passive_acceleration,
            'max_passive_speed': self.max_passive_speed,
            'stopped_threshold': self.stopped_threshold,
            'unknown_0x91b27cb3': self.unknown_0x91b27cb3,
            'balanced_velocity_percentage': self.balanced_velocity_percentage.to_json(),
            'unknown_0xc355fb9f': self.unknown_0xc355fb9f,
            'unknown_0x3153f656': self.unknown_0x3153f656.to_json(),
        }


def _decode_dominance(data: typing.BinaryIO, property_size: int):
    return enums.Dominance.from_stream(data)


def _decode_unknown_0x60d9b1cc(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_acceleration_frame(data: typing.BinaryIO, property_size: int):
    return enums.AccelerationFrame.from_stream(data)


def _decode_movement_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_movement_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_passive_acceleration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_passive_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_stopped_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x91b27cb3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xc355fb9f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xc2ea7c93: ('dominance', _decode_dominance),
    0x60d9b1cc: ('unknown_0x60d9b1cc', _decode_unknown_0x60d9b1cc),
    0xe3a1be31: ('acceleration_frame', _decode_acceleration_frame),
    0xfb5cf531: ('movement_acceleration', _decode_movement_acceleration),
    0x4cab64: ('max_movement_speed', _decode_max_movement_speed),
    0x26288849: ('passive_acceleration', _decode_passive_acceleration),
    0x51b03d22: ('max_passive_speed', _decode_max_passive_speed),
    0x550574f2: ('stopped_threshold', _decode_stopped_threshold),
    0x91b27cb3: ('unknown_0x91b27cb3', _decode_unknown_0x91b27cb3),
    0x59299e65: ('balanced_velocity_percentage', Spline.from_stream),
    0xc355fb9f: ('unknown_0xc355fb9f', _decode_unknown_0xc355fb9f),
    0x3153f656: ('unknown_0x3153f656', Spline.from_stream),
}
