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
    class BouncyTireJumpHeightsJson(typing_extensions.TypedDict):
        min_jump_height: float
        max_jump_height: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x22398a4f, 0x719f92ab)


@dataclasses.dataclass()
class BouncyTireJumpHeights(BaseProperty):
    min_jump_height: float = dataclasses.field(default=4.640200138092041, metadata={
        'reflection': FieldReflection[float](
            float, id=0x22398a4f, original_name='MinJumpHeight'
        ),
    })
    max_jump_height: float = dataclasses.field(default=7.640200138092041, metadata={
        'reflection': FieldReflection[float](
            float, id=0x719f92ab, original_name='MaxJumpHeight'
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
        if property_count != 2:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(20))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'"9\x8aO')  # 0x22398a4f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_jump_height))

        data.write(b'q\x9f\x92\xab')  # 0x719f92ab
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_jump_height))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BouncyTireJumpHeightsJson", data)
        return cls(
            min_jump_height=json_data['min_jump_height'],
            max_jump_height=json_data['max_jump_height'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'min_jump_height': self.min_jump_height,
            'max_jump_height': self.max_jump_height,
        }


def _decode_min_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_jump_height(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x22398a4f: ('min_jump_height', _decode_min_jump_height),
    0x719f92ab: ('max_jump_height', _decode_max_jump_height),
}
