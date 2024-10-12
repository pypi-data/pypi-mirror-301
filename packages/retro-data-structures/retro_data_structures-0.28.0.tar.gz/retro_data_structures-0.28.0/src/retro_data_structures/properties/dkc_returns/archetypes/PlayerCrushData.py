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
    class PlayerCrushDataJson(typing_extensions.TypedDict):
        shove_limit: float
        pinch_limit: float
        minimum_display_size: float
        failsafe_delay: float
        pre_breakout_buffer: float
        landing_blend_time: float
        can_crush_push_player: bool
        horz_revive_delay: float
        horz_revive_limit: float
        horz_reflate_time: float
        horz_knock_back_speed: float
        horz_hurl_height: float
        horz_pop_right_velocity: float
        horz_pop_left_velocity: float
        horz_pop_up_velocity: float
        horz_offset_right: float
        horz_offset_left: float
        horz_rider_offset_right: float
        horz_rider_offset_left: float
        horz_stop_player: bool
        vert_revive_delay: float
        vert_revive_limit: float
        vert_reflate_time: float
        vert_knock_back_speed: float
        vert_hurl_height: float
        vert_pop_up_velocity: float
        vert_pop_down_velocity: float
        vert_offset_up: float
        vert_offset_down: float
        vert_rider_offset_up: float
        vert_rider_offset_down: float
        vert_stop_player: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0x7589789b, 0x7b42fdfa, 0x47f3f101, 0x90aa0d86, 0xe8c4ba9b, 0xf54b2392, 0x57018cf1, 0xadcbb494, 0x1bf35a53, 0xa32f3e1c, 0x42e8f3fd, 0x213f330e, 0x72b927f9, 0x2b32b1f3, 0x50158691, 0x1727325d, 0xf5c708a8, 0x6dca433c, 0x72ecc123, 0xf515e7f6, 0x68c4b734, 0xdefc59f3, 0x66203dbc, 0x2002e00a, 0x94072db6, 0x671baecd, 0x53366bbd, 0x7619947f, 0x9031e47, 0x9b741c93, 0x18ab44d8, 0x1dc46e4b)


@dataclasses.dataclass()
class PlayerCrushData(BaseProperty):
    shove_limit: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7589789b, original_name='ShoveLimit'
        ),
    })
    pinch_limit: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7b42fdfa, original_name='PinchLimit'
        ),
    })
    minimum_display_size: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x47f3f101, original_name='MinimumDisplaySize'
        ),
    })
    failsafe_delay: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x90aa0d86, original_name='FailsafeDelay'
        ),
    })
    pre_breakout_buffer: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe8c4ba9b, original_name='PreBreakoutBuffer'
        ),
    })
    landing_blend_time: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf54b2392, original_name='LandingBlendTime'
        ),
    })
    can_crush_push_player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x57018cf1, original_name='CanCrushPushPlayer'
        ),
    })
    horz_revive_delay: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xadcbb494, original_name='HorzReviveDelay'
        ),
    })
    horz_revive_limit: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1bf35a53, original_name='HorzReviveLimit'
        ),
    })
    horz_reflate_time: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa32f3e1c, original_name='HorzReflateTime'
        ),
    })
    horz_knock_back_speed: float = dataclasses.field(default=12.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x42e8f3fd, original_name='HorzKnockBackSpeed'
        ),
    })
    horz_hurl_height: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x213f330e, original_name='HorzHurlHeight'
        ),
    })
    horz_pop_right_velocity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x72b927f9, original_name='HorzPopRightVelocity'
        ),
    })
    horz_pop_left_velocity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2b32b1f3, original_name='HorzPopLeftVelocity'
        ),
    })
    horz_pop_up_velocity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x50158691, original_name='HorzPopUpVelocity'
        ),
    })
    horz_offset_right: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1727325d, original_name='HorzOffsetRight'
        ),
    })
    horz_offset_left: float = dataclasses.field(default=0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf5c708a8, original_name='HorzOffsetLeft'
        ),
    })
    horz_rider_offset_right: float = dataclasses.field(default=-0.15000000596046448, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6dca433c, original_name='HorzRiderOffsetRight'
        ),
    })
    horz_rider_offset_left: float = dataclasses.field(default=-0.20000000298023224, metadata={
        'reflection': FieldReflection[float](
            float, id=0x72ecc123, original_name='HorzRiderOffsetLeft'
        ),
    })
    horz_stop_player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf515e7f6, original_name='HorzStopPlayer'
        ),
    })
    vert_revive_delay: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x68c4b734, original_name='VertReviveDelay'
        ),
    })
    vert_revive_limit: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0xdefc59f3, original_name='VertReviveLimit'
        ),
    })
    vert_reflate_time: float = dataclasses.field(default=0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0x66203dbc, original_name='VertReflateTime'
        ),
    })
    vert_knock_back_speed: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2002e00a, original_name='VertKnockBackSpeed'
        ),
    })
    vert_hurl_height: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x94072db6, original_name='VertHurlHeight'
        ),
    })
    vert_pop_up_velocity: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x671baecd, original_name='VertPopUpVelocity'
        ),
    })
    vert_pop_down_velocity: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x53366bbd, original_name='VertPopDownVelocity'
        ),
    })
    vert_offset_up: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7619947f, original_name='VertOffsetUp'
        ),
    })
    vert_offset_down: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x09031e47, original_name='VertOffsetDown'
        ),
    })
    vert_rider_offset_up: float = dataclasses.field(default=-0.05000000074505806, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9b741c93, original_name='VertRiderOffsetUp'
        ),
    })
    vert_rider_offset_down: float = dataclasses.field(default=-0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0x18ab44d8, original_name='VertRiderOffsetDown'
        ),
    })
    vert_stop_player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1dc46e4b, original_name='VertStopPlayer'
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
        if property_count != 32:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLH?LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLH?LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLH?')
    
        dec = _FAST_FORMAT.unpack(data.read(311))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51], dec[54], dec[57], dec[60], dec[63], dec[66], dec[69], dec[72], dec[75], dec[78], dec[81], dec[84], dec[87], dec[90], dec[93]) == _FAST_IDS
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
            dec[41],
            dec[44],
            dec[47],
            dec[50],
            dec[53],
            dec[56],
            dec[59],
            dec[62],
            dec[65],
            dec[68],
            dec[71],
            dec[74],
            dec[77],
            dec[80],
            dec[83],
            dec[86],
            dec[89],
            dec[92],
            dec[95],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00 ')  # 32 properties

        data.write(b'u\x89x\x9b')  # 0x7589789b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.shove_limit))

        data.write(b'{B\xfd\xfa')  # 0x7b42fdfa
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pinch_limit))

        data.write(b'G\xf3\xf1\x01')  # 0x47f3f101
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_display_size))

        data.write(b'\x90\xaa\r\x86')  # 0x90aa0d86
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.failsafe_delay))

        data.write(b'\xe8\xc4\xba\x9b')  # 0xe8c4ba9b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.pre_breakout_buffer))

        data.write(b'\xf5K#\x92')  # 0xf54b2392
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.landing_blend_time))

        data.write(b'W\x01\x8c\xf1')  # 0x57018cf1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_crush_push_player))

        data.write(b'\xad\xcb\xb4\x94')  # 0xadcbb494
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_revive_delay))

        data.write(b'\x1b\xf3ZS')  # 0x1bf35a53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_revive_limit))

        data.write(b'\xa3/>\x1c')  # 0xa32f3e1c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_reflate_time))

        data.write(b'B\xe8\xf3\xfd')  # 0x42e8f3fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_knock_back_speed))

        data.write(b'!?3\x0e')  # 0x213f330e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_hurl_height))

        data.write(b"r\xb9'\xf9")  # 0x72b927f9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_pop_right_velocity))

        data.write(b'+2\xb1\xf3')  # 0x2b32b1f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_pop_left_velocity))

        data.write(b'P\x15\x86\x91')  # 0x50158691
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_pop_up_velocity))

        data.write(b"\x17'2]")  # 0x1727325d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_offset_right))

        data.write(b'\xf5\xc7\x08\xa8')  # 0xf5c708a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_offset_left))

        data.write(b'm\xcaC<')  # 0x6dca433c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_rider_offset_right))

        data.write(b'r\xec\xc1#')  # 0x72ecc123
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.horz_rider_offset_left))

        data.write(b'\xf5\x15\xe7\xf6')  # 0xf515e7f6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.horz_stop_player))

        data.write(b'h\xc4\xb74')  # 0x68c4b734
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_revive_delay))

        data.write(b'\xde\xfcY\xf3')  # 0xdefc59f3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_revive_limit))

        data.write(b'f =\xbc')  # 0x66203dbc
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_reflate_time))

        data.write(b' \x02\xe0\n')  # 0x2002e00a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_knock_back_speed))

        data.write(b'\x94\x07-\xb6')  # 0x94072db6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_hurl_height))

        data.write(b'g\x1b\xae\xcd')  # 0x671baecd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_pop_up_velocity))

        data.write(b'S6k\xbd')  # 0x53366bbd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_pop_down_velocity))

        data.write(b'v\x19\x94\x7f')  # 0x7619947f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_offset_up))

        data.write(b'\t\x03\x1eG')  # 0x9031e47
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_offset_down))

        data.write(b'\x9bt\x1c\x93')  # 0x9b741c93
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_rider_offset_up))

        data.write(b'\x18\xabD\xd8')  # 0x18ab44d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.vert_rider_offset_down))

        data.write(b'\x1d\xc4nK')  # 0x1dc46e4b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.vert_stop_player))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerCrushDataJson", data)
        return cls(
            shove_limit=json_data['shove_limit'],
            pinch_limit=json_data['pinch_limit'],
            minimum_display_size=json_data['minimum_display_size'],
            failsafe_delay=json_data['failsafe_delay'],
            pre_breakout_buffer=json_data['pre_breakout_buffer'],
            landing_blend_time=json_data['landing_blend_time'],
            can_crush_push_player=json_data['can_crush_push_player'],
            horz_revive_delay=json_data['horz_revive_delay'],
            horz_revive_limit=json_data['horz_revive_limit'],
            horz_reflate_time=json_data['horz_reflate_time'],
            horz_knock_back_speed=json_data['horz_knock_back_speed'],
            horz_hurl_height=json_data['horz_hurl_height'],
            horz_pop_right_velocity=json_data['horz_pop_right_velocity'],
            horz_pop_left_velocity=json_data['horz_pop_left_velocity'],
            horz_pop_up_velocity=json_data['horz_pop_up_velocity'],
            horz_offset_right=json_data['horz_offset_right'],
            horz_offset_left=json_data['horz_offset_left'],
            horz_rider_offset_right=json_data['horz_rider_offset_right'],
            horz_rider_offset_left=json_data['horz_rider_offset_left'],
            horz_stop_player=json_data['horz_stop_player'],
            vert_revive_delay=json_data['vert_revive_delay'],
            vert_revive_limit=json_data['vert_revive_limit'],
            vert_reflate_time=json_data['vert_reflate_time'],
            vert_knock_back_speed=json_data['vert_knock_back_speed'],
            vert_hurl_height=json_data['vert_hurl_height'],
            vert_pop_up_velocity=json_data['vert_pop_up_velocity'],
            vert_pop_down_velocity=json_data['vert_pop_down_velocity'],
            vert_offset_up=json_data['vert_offset_up'],
            vert_offset_down=json_data['vert_offset_down'],
            vert_rider_offset_up=json_data['vert_rider_offset_up'],
            vert_rider_offset_down=json_data['vert_rider_offset_down'],
            vert_stop_player=json_data['vert_stop_player'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'shove_limit': self.shove_limit,
            'pinch_limit': self.pinch_limit,
            'minimum_display_size': self.minimum_display_size,
            'failsafe_delay': self.failsafe_delay,
            'pre_breakout_buffer': self.pre_breakout_buffer,
            'landing_blend_time': self.landing_blend_time,
            'can_crush_push_player': self.can_crush_push_player,
            'horz_revive_delay': self.horz_revive_delay,
            'horz_revive_limit': self.horz_revive_limit,
            'horz_reflate_time': self.horz_reflate_time,
            'horz_knock_back_speed': self.horz_knock_back_speed,
            'horz_hurl_height': self.horz_hurl_height,
            'horz_pop_right_velocity': self.horz_pop_right_velocity,
            'horz_pop_left_velocity': self.horz_pop_left_velocity,
            'horz_pop_up_velocity': self.horz_pop_up_velocity,
            'horz_offset_right': self.horz_offset_right,
            'horz_offset_left': self.horz_offset_left,
            'horz_rider_offset_right': self.horz_rider_offset_right,
            'horz_rider_offset_left': self.horz_rider_offset_left,
            'horz_stop_player': self.horz_stop_player,
            'vert_revive_delay': self.vert_revive_delay,
            'vert_revive_limit': self.vert_revive_limit,
            'vert_reflate_time': self.vert_reflate_time,
            'vert_knock_back_speed': self.vert_knock_back_speed,
            'vert_hurl_height': self.vert_hurl_height,
            'vert_pop_up_velocity': self.vert_pop_up_velocity,
            'vert_pop_down_velocity': self.vert_pop_down_velocity,
            'vert_offset_up': self.vert_offset_up,
            'vert_offset_down': self.vert_offset_down,
            'vert_rider_offset_up': self.vert_rider_offset_up,
            'vert_rider_offset_down': self.vert_rider_offset_down,
            'vert_stop_player': self.vert_stop_player,
        }


def _decode_shove_limit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pinch_limit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_minimum_display_size(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_failsafe_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pre_breakout_buffer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_landing_blend_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_can_crush_push_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_horz_revive_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_revive_limit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_reflate_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_knock_back_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_hurl_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_pop_right_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_pop_left_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_pop_up_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_offset_right(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_offset_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_rider_offset_right(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_rider_offset_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_horz_stop_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_vert_revive_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_revive_limit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_reflate_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_knock_back_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_hurl_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_pop_up_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_pop_down_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_offset_up(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_offset_down(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_rider_offset_up(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_rider_offset_down(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_vert_stop_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x7589789b: ('shove_limit', _decode_shove_limit),
    0x7b42fdfa: ('pinch_limit', _decode_pinch_limit),
    0x47f3f101: ('minimum_display_size', _decode_minimum_display_size),
    0x90aa0d86: ('failsafe_delay', _decode_failsafe_delay),
    0xe8c4ba9b: ('pre_breakout_buffer', _decode_pre_breakout_buffer),
    0xf54b2392: ('landing_blend_time', _decode_landing_blend_time),
    0x57018cf1: ('can_crush_push_player', _decode_can_crush_push_player),
    0xadcbb494: ('horz_revive_delay', _decode_horz_revive_delay),
    0x1bf35a53: ('horz_revive_limit', _decode_horz_revive_limit),
    0xa32f3e1c: ('horz_reflate_time', _decode_horz_reflate_time),
    0x42e8f3fd: ('horz_knock_back_speed', _decode_horz_knock_back_speed),
    0x213f330e: ('horz_hurl_height', _decode_horz_hurl_height),
    0x72b927f9: ('horz_pop_right_velocity', _decode_horz_pop_right_velocity),
    0x2b32b1f3: ('horz_pop_left_velocity', _decode_horz_pop_left_velocity),
    0x50158691: ('horz_pop_up_velocity', _decode_horz_pop_up_velocity),
    0x1727325d: ('horz_offset_right', _decode_horz_offset_right),
    0xf5c708a8: ('horz_offset_left', _decode_horz_offset_left),
    0x6dca433c: ('horz_rider_offset_right', _decode_horz_rider_offset_right),
    0x72ecc123: ('horz_rider_offset_left', _decode_horz_rider_offset_left),
    0xf515e7f6: ('horz_stop_player', _decode_horz_stop_player),
    0x68c4b734: ('vert_revive_delay', _decode_vert_revive_delay),
    0xdefc59f3: ('vert_revive_limit', _decode_vert_revive_limit),
    0x66203dbc: ('vert_reflate_time', _decode_vert_reflate_time),
    0x2002e00a: ('vert_knock_back_speed', _decode_vert_knock_back_speed),
    0x94072db6: ('vert_hurl_height', _decode_vert_hurl_height),
    0x671baecd: ('vert_pop_up_velocity', _decode_vert_pop_up_velocity),
    0x53366bbd: ('vert_pop_down_velocity', _decode_vert_pop_down_velocity),
    0x7619947f: ('vert_offset_up', _decode_vert_offset_up),
    0x9031e47: ('vert_offset_down', _decode_vert_offset_down),
    0x9b741c93: ('vert_rider_offset_up', _decode_vert_rider_offset_up),
    0x18ab44d8: ('vert_rider_offset_down', _decode_vert_rider_offset_down),
    0x1dc46e4b: ('vert_stop_player', _decode_vert_stop_player),
}
