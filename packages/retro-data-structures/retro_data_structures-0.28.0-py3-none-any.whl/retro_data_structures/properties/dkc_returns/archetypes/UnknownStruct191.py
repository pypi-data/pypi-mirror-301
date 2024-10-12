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
    class UnknownStruct191Json(typing_extensions.TypedDict):
        unknown_0x8a58a7f8: int
        initial_launch_delay: float
        launch_delay: float
        unknown_0xe828e54e: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x8a58a7f8, 0xcca8af3d, 0x4655a9c5, 0xe828e54e)


@dataclasses.dataclass()
class UnknownStruct191(BaseProperty):
    unknown_0x8a58a7f8: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8a58a7f8, original_name='Unknown'
        ),
    })
    initial_launch_delay: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcca8af3d, original_name='InitialLaunchDelay'
        ),
    })
    launch_delay: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4655a9c5, original_name='LaunchDelay'
        ),
    })
    unknown_0xe828e54e: float = dataclasses.field(default=6.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe828e54e, original_name='Unknown'
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
            _FAST_FORMAT = struct.Struct('>LHlLHfLHfLHf')
    
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

        data.write(b'\x8aX\xa7\xf8')  # 0x8a58a7f8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown_0x8a58a7f8))

        data.write(b'\xcc\xa8\xaf=')  # 0xcca8af3d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_launch_delay))

        data.write(b'FU\xa9\xc5')  # 0x4655a9c5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.launch_delay))

        data.write(b'\xe8(\xe5N')  # 0xe828e54e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe828e54e))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct191Json", data)
        return cls(
            unknown_0x8a58a7f8=json_data['unknown_0x8a58a7f8'],
            initial_launch_delay=json_data['initial_launch_delay'],
            launch_delay=json_data['launch_delay'],
            unknown_0xe828e54e=json_data['unknown_0xe828e54e'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x8a58a7f8': self.unknown_0x8a58a7f8,
            'initial_launch_delay': self.initial_launch_delay,
            'launch_delay': self.launch_delay,
            'unknown_0xe828e54e': self.unknown_0xe828e54e,
        }


def _decode_unknown_0x8a58a7f8(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_initial_launch_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launch_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe828e54e(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x8a58a7f8: ('unknown_0x8a58a7f8', _decode_unknown_0x8a58a7f8),
    0xcca8af3d: ('initial_launch_delay', _decode_initial_launch_delay),
    0x4655a9c5: ('launch_delay', _decode_launch_delay),
    0xe828e54e: ('unknown_0xe828e54e', _decode_unknown_0xe828e54e),
}
