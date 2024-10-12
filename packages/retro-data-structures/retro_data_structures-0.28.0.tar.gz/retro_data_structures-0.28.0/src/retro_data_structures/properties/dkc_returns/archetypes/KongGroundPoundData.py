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
    class KongGroundPoundDataJson(typing_extensions.TypedDict):
        ground_pound_box_scale: json_util.JsonValue
        min_delay_between_slaps: float
        delay_between_same_hand_slaps: float
        delay_horizontal_movement_after_slap: float
        delay_jumping_after_slap: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xdbb13e19, 0x458f7b04, 0xa6a1cd8f, 0x3d233e53, 0xa4ab00a8)


@dataclasses.dataclass()
class KongGroundPoundData(BaseProperty):
    ground_pound_box_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=30.0, y=30.0, z=30.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xdbb13e19, original_name='GroundPoundBoxScale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    min_delay_between_slaps: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x458f7b04, original_name='MinDelayBetweenSlaps'
        ),
    })
    delay_between_same_hand_slaps: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa6a1cd8f, original_name='DelayBetweenSameHandSlaps'
        ),
    })
    delay_horizontal_movement_after_slap: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3d233e53, original_name='DelayHorizontalMovementAfterSlap'
        ),
    })
    delay_jumping_after_slap: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa4ab00a8, original_name='DelayJumpingAfterSlap'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfffLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(58))
        assert (dec[0], dec[5], dec[8], dec[11], dec[14]) == _FAST_IDS
        return cls(
            Vector(*dec[2:5]),
            dec[7],
            dec[10],
            dec[13],
            dec[16],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'\xdb\xb1>\x19')  # 0xdbb13e19
        data.write(b'\x00\x0c')  # size
        self.ground_pound_box_scale.to_stream(data)

        data.write(b'E\x8f{\x04')  # 0x458f7b04
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_delay_between_slaps))

        data.write(b'\xa6\xa1\xcd\x8f')  # 0xa6a1cd8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_between_same_hand_slaps))

        data.write(b'=#>S')  # 0x3d233e53
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_horizontal_movement_after_slap))

        data.write(b'\xa4\xab\x00\xa8')  # 0xa4ab00a8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.delay_jumping_after_slap))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("KongGroundPoundDataJson", data)
        return cls(
            ground_pound_box_scale=Vector.from_json(json_data['ground_pound_box_scale']),
            min_delay_between_slaps=json_data['min_delay_between_slaps'],
            delay_between_same_hand_slaps=json_data['delay_between_same_hand_slaps'],
            delay_horizontal_movement_after_slap=json_data['delay_horizontal_movement_after_slap'],
            delay_jumping_after_slap=json_data['delay_jumping_after_slap'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'ground_pound_box_scale': self.ground_pound_box_scale.to_json(),
            'min_delay_between_slaps': self.min_delay_between_slaps,
            'delay_between_same_hand_slaps': self.delay_between_same_hand_slaps,
            'delay_horizontal_movement_after_slap': self.delay_horizontal_movement_after_slap,
            'delay_jumping_after_slap': self.delay_jumping_after_slap,
        }


def _decode_ground_pound_box_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_min_delay_between_slaps(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_between_same_hand_slaps(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_horizontal_movement_after_slap(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_delay_jumping_after_slap(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdbb13e19: ('ground_pound_box_scale', _decode_ground_pound_box_scale),
    0x458f7b04: ('min_delay_between_slaps', _decode_min_delay_between_slaps),
    0xa6a1cd8f: ('delay_between_same_hand_slaps', _decode_delay_between_same_hand_slaps),
    0x3d233e53: ('delay_horizontal_movement_after_slap', _decode_delay_horizontal_movement_after_slap),
    0xa4ab00a8: ('delay_jumping_after_slap', _decode_delay_jumping_after_slap),
}
