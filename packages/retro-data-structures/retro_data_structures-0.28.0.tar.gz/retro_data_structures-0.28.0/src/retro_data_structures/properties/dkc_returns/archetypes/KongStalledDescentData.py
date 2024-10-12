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
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class KongStalledDescentDataJson(typing_extensions.TypedDict):
        rate_of_descent: float
        thrust_ramp_in_time: float
        descent_control_scalar: float
        thrust_duration: float
        rocket_pack_effect: int
        rocket_pack_smoke_effect: int
        rocket_pack_smoke_trail_effect: int
        rocket_pack_effect_locator: str
        rocket_pack_sound: int
        unknown_0xbdaaa9b1: json_util.JsonObject
        unknown_0x7e50a6d2: json_util.JsonObject
        unknown_0x075f730c: json_util.JsonObject
    

@dataclasses.dataclass()
class KongStalledDescentData(BaseProperty):
    rate_of_descent: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8848e341, original_name='RateOfDescent'
        ),
    })
    thrust_ramp_in_time: float = dataclasses.field(default=0.3499999940395355, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd9ffdd53, original_name='ThrustRampInTime'
        ),
    })
    descent_control_scalar: float = dataclasses.field(default=1.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x28e1a39c, original_name='DescentControlScalar'
        ),
    })
    thrust_duration: float = dataclasses.field(default=2.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe8c06d7e, original_name='ThrustDuration'
        ),
    })
    rocket_pack_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xbf3dd0e1, original_name='RocketPackEffect'
        ),
    })
    rocket_pack_smoke_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5c271c9a, original_name='RocketPackSmokeEffect'
        ),
    })
    rocket_pack_smoke_trail_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5121648e, original_name='RocketPackSmokeTrailEffect'
        ),
    })
    rocket_pack_effect_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xc9d72254, original_name='RocketPackEffectLocator'
        ),
    })
    rocket_pack_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa2acf0fa, original_name='RocketPackSound'
        ),
    })
    unknown_0xbdaaa9b1: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xbdaaa9b1, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    unknown_0x7e50a6d2: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x7e50a6d2, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    unknown_0x075f730c: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x075f730c, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
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
        assert property_id == 0x8848e341
        rate_of_descent = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9ffdd53
        thrust_ramp_in_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x28e1a39c
        descent_control_scalar = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe8c06d7e
        thrust_duration = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf3dd0e1
        rocket_pack_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5c271c9a
        rocket_pack_smoke_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5121648e
        rocket_pack_smoke_trail_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc9d72254
        rocket_pack_effect_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa2acf0fa
        rocket_pack_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbdaaa9b1
        unknown_0xbdaaa9b1 = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7e50a6d2
        unknown_0x7e50a6d2 = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x075f730c
        unknown_0x075f730c = Spline.from_stream(data, property_size)
    
        return cls(rate_of_descent, thrust_ramp_in_time, descent_control_scalar, thrust_duration, rocket_pack_effect, rocket_pack_smoke_effect, rocket_pack_smoke_trail_effect, rocket_pack_effect_locator, rocket_pack_sound, unknown_0xbdaaa9b1, unknown_0x7e50a6d2, unknown_0x075f730c)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\x88H\xe3A')  # 0x8848e341
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rate_of_descent))

        data.write(b'\xd9\xff\xddS')  # 0xd9ffdd53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.thrust_ramp_in_time))

        data.write(b'(\xe1\xa3\x9c')  # 0x28e1a39c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.descent_control_scalar))

        data.write(b'\xe8\xc0m~')  # 0xe8c06d7e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.thrust_duration))

        data.write(b'\xbf=\xd0\xe1')  # 0xbf3dd0e1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rocket_pack_effect))

        data.write(b"\\'\x1c\x9a")  # 0x5c271c9a
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rocket_pack_smoke_effect))

        data.write(b'Q!d\x8e')  # 0x5121648e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rocket_pack_smoke_trail_effect))

        data.write(b'\xc9\xd7"T')  # 0xc9d72254
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.rocket_pack_effect_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa2\xac\xf0\xfa')  # 0xa2acf0fa
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.rocket_pack_sound))

        data.write(b'\xbd\xaa\xa9\xb1')  # 0xbdaaa9b1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xbdaaa9b1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~P\xa6\xd2')  # 0x7e50a6d2
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x7e50a6d2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x07_s\x0c')  # 0x75f730c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0x075f730c.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("KongStalledDescentDataJson", data)
        return cls(
            rate_of_descent=json_data['rate_of_descent'],
            thrust_ramp_in_time=json_data['thrust_ramp_in_time'],
            descent_control_scalar=json_data['descent_control_scalar'],
            thrust_duration=json_data['thrust_duration'],
            rocket_pack_effect=json_data['rocket_pack_effect'],
            rocket_pack_smoke_effect=json_data['rocket_pack_smoke_effect'],
            rocket_pack_smoke_trail_effect=json_data['rocket_pack_smoke_trail_effect'],
            rocket_pack_effect_locator=json_data['rocket_pack_effect_locator'],
            rocket_pack_sound=json_data['rocket_pack_sound'],
            unknown_0xbdaaa9b1=Spline.from_json(json_data['unknown_0xbdaaa9b1']),
            unknown_0x7e50a6d2=Spline.from_json(json_data['unknown_0x7e50a6d2']),
            unknown_0x075f730c=Spline.from_json(json_data['unknown_0x075f730c']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'rate_of_descent': self.rate_of_descent,
            'thrust_ramp_in_time': self.thrust_ramp_in_time,
            'descent_control_scalar': self.descent_control_scalar,
            'thrust_duration': self.thrust_duration,
            'rocket_pack_effect': self.rocket_pack_effect,
            'rocket_pack_smoke_effect': self.rocket_pack_smoke_effect,
            'rocket_pack_smoke_trail_effect': self.rocket_pack_smoke_trail_effect,
            'rocket_pack_effect_locator': self.rocket_pack_effect_locator,
            'rocket_pack_sound': self.rocket_pack_sound,
            'unknown_0xbdaaa9b1': self.unknown_0xbdaaa9b1.to_json(),
            'unknown_0x7e50a6d2': self.unknown_0x7e50a6d2.to_json(),
            'unknown_0x075f730c': self.unknown_0x075f730c.to_json(),
        }


def _decode_rate_of_descent(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_thrust_ramp_in_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_descent_control_scalar(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_thrust_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_rocket_pack_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rocket_pack_smoke_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rocket_pack_smoke_trail_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_rocket_pack_effect_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_rocket_pack_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8848e341: ('rate_of_descent', _decode_rate_of_descent),
    0xd9ffdd53: ('thrust_ramp_in_time', _decode_thrust_ramp_in_time),
    0x28e1a39c: ('descent_control_scalar', _decode_descent_control_scalar),
    0xe8c06d7e: ('thrust_duration', _decode_thrust_duration),
    0xbf3dd0e1: ('rocket_pack_effect', _decode_rocket_pack_effect),
    0x5c271c9a: ('rocket_pack_smoke_effect', _decode_rocket_pack_smoke_effect),
    0x5121648e: ('rocket_pack_smoke_trail_effect', _decode_rocket_pack_smoke_trail_effect),
    0xc9d72254: ('rocket_pack_effect_locator', _decode_rocket_pack_effect_locator),
    0xa2acf0fa: ('rocket_pack_sound', _decode_rocket_pack_sound),
    0xbdaaa9b1: ('unknown_0xbdaaa9b1', Spline.from_stream),
    0x7e50a6d2: ('unknown_0x7e50a6d2', Spline.from_stream),
    0x75f730c: ('unknown_0x075f730c', Spline.from_stream),
}
