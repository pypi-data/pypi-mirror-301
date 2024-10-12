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
    class UnknownStruct288Json(typing_extensions.TypedDict):
        stage_width: float
        unknown_0xf2ec945d: float
        unknown_0xceebc469: float
        unknown_0x90ef04a5: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xe6892623, 0xf2ec945d, 0xceebc469, 0x90ef04a5)


@dataclasses.dataclass()
class UnknownStruct288(BaseProperty):
    stage_width: float = dataclasses.field(default=32.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe6892623, original_name='StageWidth'
        ),
    })
    unknown_0xf2ec945d: float = dataclasses.field(default=8.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf2ec945d, original_name='Unknown'
        ),
    })
    unknown_0xceebc469: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xceebc469, original_name='Unknown'
        ),
    })
    unknown_0x90ef04a5: float = dataclasses.field(default=50.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x90ef04a5, original_name='Unknown'
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
        if property_count != 4:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(40))
        assert (dec[0], dec[3], dec[6], dec[9]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xe6\x89&#')  # 0xe6892623
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.stage_width))

        data.write(b'\xf2\xec\x94]')  # 0xf2ec945d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf2ec945d))

        data.write(b'\xce\xeb\xc4i')  # 0xceebc469
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xceebc469))

        data.write(b'\x90\xef\x04\xa5')  # 0x90ef04a5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x90ef04a5))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct288Json", data)
        return cls(
            stage_width=json_data['stage_width'],
            unknown_0xf2ec945d=json_data['unknown_0xf2ec945d'],
            unknown_0xceebc469=json_data['unknown_0xceebc469'],
            unknown_0x90ef04a5=json_data['unknown_0x90ef04a5'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'stage_width': self.stage_width,
            'unknown_0xf2ec945d': self.unknown_0xf2ec945d,
            'unknown_0xceebc469': self.unknown_0xceebc469,
            'unknown_0x90ef04a5': self.unknown_0x90ef04a5,
        }


def _decode_stage_width(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf2ec945d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xceebc469(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x90ef04a5(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xe6892623: ('stage_width', _decode_stage_width),
    0xf2ec945d: ('unknown_0xf2ec945d', _decode_unknown_0xf2ec945d),
    0xceebc469: ('unknown_0xceebc469', _decode_unknown_0xceebc469),
    0x90ef04a5: ('unknown_0x90ef04a5', _decode_unknown_0x90ef04a5),
}
