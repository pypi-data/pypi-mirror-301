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
from retro_data_structures.properties.dkc_returns.archetypes.DamageInfo import DamageInfo

if typing.TYPE_CHECKING:
    class GrabPlayerBehaviorDataJson(typing_extensions.TypedDict):
        grab_player_type: int
        chew_damage: json_util.JsonObject
        chew_damage_time: float
        chew_damage_on_spit_out: bool
        chew_damage_on_spit_out_delay_time: float
        ground_pound_let_go_time: float
        ground_pound_relapse_multiplier: float
        ground_pound_window: float
        attract_target_speed: float
        grab_distance_threshold: float
        post_release_ignore_time: float
        spit_distance: float
        spit_height: float
        spit_speed: float
        vine_ignore_time: float
        vine_swing_dampen_time: float
        vine_swing_undampen_time: float
    

@dataclasses.dataclass()
class GrabPlayerBehaviorData(BaseProperty):
    grab_player_type: enums.GrabPlayerType = dataclasses.field(default=enums.GrabPlayerType.Unknown1, metadata={
        'reflection': FieldReflection[enums.GrabPlayerType](
            enums.GrabPlayerType, id=0xbf89d05d, original_name='GrabPlayerType', from_json=enums.GrabPlayerType.from_json, to_json=enums.GrabPlayerType.to_json
        ),
    })
    chew_damage: DamageInfo = dataclasses.field(default_factory=DamageInfo, metadata={
        'reflection': FieldReflection[DamageInfo](
            DamageInfo, id=0x6f7a3416, original_name='ChewDamage', from_json=DamageInfo.from_json, to_json=DamageInfo.to_json
        ),
    })
    chew_damage_time: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x267edd84, original_name='ChewDamageTime'
        ),
    })
    chew_damage_on_spit_out: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4bcef91a, original_name='ChewDamageOnSpitOut'
        ),
    })
    chew_damage_on_spit_out_delay_time: float = dataclasses.field(default=0.375, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc793c525, original_name='ChewDamageOnSpitOutDelayTime'
        ),
    })
    ground_pound_let_go_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xce7b09c8, original_name='GroundPoundLetGoTime'
        ),
    })
    ground_pound_relapse_multiplier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x686e030b, original_name='GroundPoundRelapseMultiplier'
        ),
    })
    ground_pound_window: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x68d787b4, original_name='GroundPoundWindow'
        ),
    })
    attract_target_speed: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2307a992, original_name='AttractTargetSpeed'
        ),
    })
    grab_distance_threshold: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x79fad0a2, original_name='GrabDistanceThreshold'
        ),
    })
    post_release_ignore_time: float = dataclasses.field(default=0.30000001192092896, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6fcaf068, original_name='PostReleaseIgnoreTime'
        ),
    })
    spit_distance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x04408e47, original_name='SpitDistance'
        ),
    })
    spit_height: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa54be635, original_name='SpitHeight'
        ),
    })
    spit_speed: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4b3db4d5, original_name='SpitSpeed'
        ),
    })
    vine_ignore_time: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbf7f3cd1, original_name='VineIgnoreTime'
        ),
    })
    vine_swing_dampen_time: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6046ee04, original_name='VineSwingDampenTime'
        ),
    })
    vine_swing_undampen_time: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x30ac886c, original_name='VineSwingUndampenTime'
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
        if property_count != 17:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf89d05d
        grab_player_type = enums.GrabPlayerType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6f7a3416
        chew_damage = DamageInfo.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x267edd84
        chew_damage_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4bcef91a
        chew_damage_on_spit_out = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc793c525
        chew_damage_on_spit_out_delay_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xce7b09c8
        ground_pound_let_go_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x686e030b
        ground_pound_relapse_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68d787b4
        ground_pound_window = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2307a992
        attract_target_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x79fad0a2
        grab_distance_threshold = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6fcaf068
        post_release_ignore_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x04408e47
        spit_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa54be635
        spit_height = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4b3db4d5
        spit_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbf7f3cd1
        vine_ignore_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6046ee04
        vine_swing_dampen_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x30ac886c
        vine_swing_undampen_time = struct.unpack('>f', data.read(4))[0]
    
        return cls(grab_player_type, chew_damage, chew_damage_time, chew_damage_on_spit_out, chew_damage_on_spit_out_delay_time, ground_pound_let_go_time, ground_pound_relapse_multiplier, ground_pound_window, attract_target_speed, grab_distance_threshold, post_release_ignore_time, spit_distance, spit_height, spit_speed, vine_ignore_time, vine_swing_dampen_time, vine_swing_undampen_time)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x11')  # 17 properties

        data.write(b'\xbf\x89\xd0]')  # 0xbf89d05d
        data.write(b'\x00\x04')  # size
        self.grab_player_type.to_stream(data)

        data.write(b'oz4\x16')  # 0x6f7a3416
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.chew_damage.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'&~\xdd\x84')  # 0x267edd84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chew_damage_time))

        data.write(b'K\xce\xf9\x1a')  # 0x4bcef91a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.chew_damage_on_spit_out))

        data.write(b'\xc7\x93\xc5%')  # 0xc793c525
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chew_damage_on_spit_out_delay_time))

        data.write(b'\xce{\t\xc8')  # 0xce7b09c8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_let_go_time))

        data.write(b'hn\x03\x0b')  # 0x686e030b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_relapse_multiplier))

        data.write(b'h\xd7\x87\xb4')  # 0x68d787b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_window))

        data.write(b'#\x07\xa9\x92')  # 0x2307a992
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attract_target_speed))

        data.write(b'y\xfa\xd0\xa2')  # 0x79fad0a2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.grab_distance_threshold))

        data.write(b'o\xca\xf0h')  # 0x6fcaf068
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.post_release_ignore_time))

        data.write(b'\x04@\x8eG')  # 0x4408e47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_distance))

        data.write(b'\xa5K\xe65')  # 0xa54be635
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_height))

        data.write(b'K=\xb4\xd5')  # 0x4b3db4d5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.spit_speed))

        data.write(b'\xbf\x7f<\xd1')  # 0xbf7f3cd1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vine_ignore_time))

        data.write(b'`F\xee\x04')  # 0x6046ee04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vine_swing_dampen_time))

        data.write(b'0\xac\x88l')  # 0x30ac886c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vine_swing_undampen_time))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("GrabPlayerBehaviorDataJson", data)
        return cls(
            grab_player_type=enums.GrabPlayerType.from_json(json_data['grab_player_type']),
            chew_damage=DamageInfo.from_json(json_data['chew_damage']),
            chew_damage_time=json_data['chew_damage_time'],
            chew_damage_on_spit_out=json_data['chew_damage_on_spit_out'],
            chew_damage_on_spit_out_delay_time=json_data['chew_damage_on_spit_out_delay_time'],
            ground_pound_let_go_time=json_data['ground_pound_let_go_time'],
            ground_pound_relapse_multiplier=json_data['ground_pound_relapse_multiplier'],
            ground_pound_window=json_data['ground_pound_window'],
            attract_target_speed=json_data['attract_target_speed'],
            grab_distance_threshold=json_data['grab_distance_threshold'],
            post_release_ignore_time=json_data['post_release_ignore_time'],
            spit_distance=json_data['spit_distance'],
            spit_height=json_data['spit_height'],
            spit_speed=json_data['spit_speed'],
            vine_ignore_time=json_data['vine_ignore_time'],
            vine_swing_dampen_time=json_data['vine_swing_dampen_time'],
            vine_swing_undampen_time=json_data['vine_swing_undampen_time'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'grab_player_type': self.grab_player_type.to_json(),
            'chew_damage': self.chew_damage.to_json(),
            'chew_damage_time': self.chew_damage_time,
            'chew_damage_on_spit_out': self.chew_damage_on_spit_out,
            'chew_damage_on_spit_out_delay_time': self.chew_damage_on_spit_out_delay_time,
            'ground_pound_let_go_time': self.ground_pound_let_go_time,
            'ground_pound_relapse_multiplier': self.ground_pound_relapse_multiplier,
            'ground_pound_window': self.ground_pound_window,
            'attract_target_speed': self.attract_target_speed,
            'grab_distance_threshold': self.grab_distance_threshold,
            'post_release_ignore_time': self.post_release_ignore_time,
            'spit_distance': self.spit_distance,
            'spit_height': self.spit_height,
            'spit_speed': self.spit_speed,
            'vine_ignore_time': self.vine_ignore_time,
            'vine_swing_dampen_time': self.vine_swing_dampen_time,
            'vine_swing_undampen_time': self.vine_swing_undampen_time,
        }


def _decode_grab_player_type(data: typing.BinaryIO, property_size: int):
    return enums.GrabPlayerType.from_stream(data)


def _decode_chew_damage_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_chew_damage_on_spit_out(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_chew_damage_on_spit_out_delay_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_let_go_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_relapse_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attract_target_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_grab_distance_threshold(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_post_release_ignore_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spit_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vine_ignore_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vine_swing_dampen_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vine_swing_undampen_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xbf89d05d: ('grab_player_type', _decode_grab_player_type),
    0x6f7a3416: ('chew_damage', DamageInfo.from_stream),
    0x267edd84: ('chew_damage_time', _decode_chew_damage_time),
    0x4bcef91a: ('chew_damage_on_spit_out', _decode_chew_damage_on_spit_out),
    0xc793c525: ('chew_damage_on_spit_out_delay_time', _decode_chew_damage_on_spit_out_delay_time),
    0xce7b09c8: ('ground_pound_let_go_time', _decode_ground_pound_let_go_time),
    0x686e030b: ('ground_pound_relapse_multiplier', _decode_ground_pound_relapse_multiplier),
    0x68d787b4: ('ground_pound_window', _decode_ground_pound_window),
    0x2307a992: ('attract_target_speed', _decode_attract_target_speed),
    0x79fad0a2: ('grab_distance_threshold', _decode_grab_distance_threshold),
    0x6fcaf068: ('post_release_ignore_time', _decode_post_release_ignore_time),
    0x4408e47: ('spit_distance', _decode_spit_distance),
    0xa54be635: ('spit_height', _decode_spit_height),
    0x4b3db4d5: ('spit_speed', _decode_spit_speed),
    0xbf7f3cd1: ('vine_ignore_time', _decode_vine_ignore_time),
    0x6046ee04: ('vine_swing_dampen_time', _decode_vine_swing_dampen_time),
    0x30ac886c: ('vine_swing_undampen_time', _decode_vine_swing_undampen_time),
}
