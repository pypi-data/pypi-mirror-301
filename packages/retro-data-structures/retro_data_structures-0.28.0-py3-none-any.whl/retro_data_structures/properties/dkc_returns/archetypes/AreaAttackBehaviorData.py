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
    class AreaAttackBehaviorDataJson(typing_extensions.TypedDict):
        attack_range_max: float
        attack_range_min: float
        initial_attack_delay: float
        attack_interval_max: float
        attack_interval_min: float
        mode: int
    

_FAST_FORMAT = None
_FAST_IDS = (0xe70d0592, 0x16daa73, 0x919a9ee2, 0xd78b5788, 0x31ebf869, 0xb8f60f9a)


@dataclasses.dataclass()
class AreaAttackBehaviorData(BaseProperty):
    attack_range_max: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe70d0592, original_name='AttackRangeMax'
        ),
    })
    attack_range_min: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x016daa73, original_name='AttackRangeMin'
        ),
    })
    initial_attack_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x919a9ee2, original_name='InitialAttackDelay'
        ),
    })
    attack_interval_max: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd78b5788, original_name='AttackIntervalMax'
        ),
    })
    attack_interval_min: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x31ebf869, original_name='AttackIntervalMin'
        ),
    })
    mode: int = dataclasses.field(default=1686810489, metadata={
        'reflection': FieldReflection[int](
            int, id=0xb8f60f9a, original_name='Mode'
        ),
    })  # Choice

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
        if property_count != 6:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHL')
    
        dec = _FAST_FORMAT.unpack(data.read(60))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x06')  # 6 properties

        data.write(b'\xe7\r\x05\x92')  # 0xe70d0592
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_range_max))

        data.write(b'\x01m\xaas')  # 0x16daa73
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_range_min))

        data.write(b'\x91\x9a\x9e\xe2')  # 0x919a9ee2
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_attack_delay))

        data.write(b'\xd7\x8bW\x88')  # 0xd78b5788
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_interval_max))

        data.write(b'1\xeb\xf8i')  # 0x31ebf869
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_interval_min))

        data.write(b'\xb8\xf6\x0f\x9a')  # 0xb8f60f9a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack(">L", self.mode))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("AreaAttackBehaviorDataJson", data)
        return cls(
            attack_range_max=json_data['attack_range_max'],
            attack_range_min=json_data['attack_range_min'],
            initial_attack_delay=json_data['initial_attack_delay'],
            attack_interval_max=json_data['attack_interval_max'],
            attack_interval_min=json_data['attack_interval_min'],
            mode=json_data['mode'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attack_range_max': self.attack_range_max,
            'attack_range_min': self.attack_range_min,
            'initial_attack_delay': self.initial_attack_delay,
            'attack_interval_max': self.attack_interval_max,
            'attack_interval_min': self.attack_interval_min,
            'mode': self.mode,
        }


def _decode_attack_range_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_range_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_attack_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_interval_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_attack_interval_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">L", data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe70d0592: ('attack_range_max', _decode_attack_range_max),
    0x16daa73: ('attack_range_min', _decode_attack_range_min),
    0x919a9ee2: ('initial_attack_delay', _decode_initial_attack_delay),
    0xd78b5788: ('attack_interval_max', _decode_attack_interval_max),
    0x31ebf869: ('attack_interval_min', _decode_attack_interval_min),
    0xb8f60f9a: ('mode', _decode_mode),
}
