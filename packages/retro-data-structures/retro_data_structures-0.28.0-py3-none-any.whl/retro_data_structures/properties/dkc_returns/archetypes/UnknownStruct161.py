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
    class UnknownStruct161Json(typing_extensions.TypedDict):
        unknown_0xac6cbf9d: float
        initial_duration: float
        reveal_title_duration: float
        unknown_0x34e18255: float
        unknown_0x892ae90a: float
        unknown_0x5bed9219: float
        unknown_0x039bddff: float
        unknown_0x48b54a2f: float
        unknown_0x81402f46: float
        unknown_0xe328a2c3: float
        unknown_0xcab973a9: float
        unknown_0x407911ad: float
        reveal_buttons_duration: float
        unknown_0xf0c51c84: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xac6cbf9d, 0x8e6c42f, 0x4a4ac4c, 0x34e18255, 0x892ae90a, 0x5bed9219, 0x39bddff, 0x48b54a2f, 0x81402f46, 0xe328a2c3, 0xcab973a9, 0x407911ad, 0x6d5fd457, 0xf0c51c84)


@dataclasses.dataclass()
class UnknownStruct161(BaseProperty):
    unknown_0xac6cbf9d: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xac6cbf9d, original_name='Unknown'
        ),
    })
    initial_duration: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x08e6c42f, original_name='InitialDuration'
        ),
    })
    reveal_title_duration: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x04a4ac4c, original_name='RevealTitleDuration'
        ),
    })
    unknown_0x34e18255: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x34e18255, original_name='Unknown'
        ),
    })
    unknown_0x892ae90a: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x892ae90a, original_name='Unknown'
        ),
    })
    unknown_0x5bed9219: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5bed9219, original_name='Unknown'
        ),
    })
    unknown_0x039bddff: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x039bddff, original_name='Unknown'
        ),
    })
    unknown_0x48b54a2f: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x48b54a2f, original_name='Unknown'
        ),
    })
    unknown_0x81402f46: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x81402f46, original_name='Unknown'
        ),
    })
    unknown_0xe328a2c3: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe328a2c3, original_name='Unknown'
        ),
    })
    unknown_0xcab973a9: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcab973a9, original_name='Unknown'
        ),
    })
    unknown_0x407911ad: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x407911ad, original_name='Unknown'
        ),
    })
    reveal_buttons_duration: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6d5fd457, original_name='RevealButtonsDuration'
        ),
    })
    unknown_0xf0c51c84: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf0c51c84, original_name='Unknown'
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
        if property_count != 14:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHfLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(140))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39]) == _FAST_IDS
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
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'\xacl\xbf\x9d')  # 0xac6cbf9d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xac6cbf9d))

        data.write(b'\x08\xe6\xc4/')  # 0x8e6c42f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_duration))

        data.write(b'\x04\xa4\xacL')  # 0x4a4ac4c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reveal_title_duration))

        data.write(b'4\xe1\x82U')  # 0x34e18255
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x34e18255))

        data.write(b'\x89*\xe9\n')  # 0x892ae90a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x892ae90a))

        data.write(b'[\xed\x92\x19')  # 0x5bed9219
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x5bed9219))

        data.write(b'\x03\x9b\xdd\xff')  # 0x39bddff
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x039bddff))

        data.write(b'H\xb5J/')  # 0x48b54a2f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x48b54a2f))

        data.write(b'\x81@/F')  # 0x81402f46
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x81402f46))

        data.write(b'\xe3(\xa2\xc3')  # 0xe328a2c3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xe328a2c3))

        data.write(b'\xca\xb9s\xa9')  # 0xcab973a9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xcab973a9))

        data.write(b'@y\x11\xad')  # 0x407911ad
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x407911ad))

        data.write(b'm_\xd4W')  # 0x6d5fd457
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.reveal_buttons_duration))

        data.write(b'\xf0\xc5\x1c\x84')  # 0xf0c51c84
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0xf0c51c84))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct161Json", data)
        return cls(
            unknown_0xac6cbf9d=json_data['unknown_0xac6cbf9d'],
            initial_duration=json_data['initial_duration'],
            reveal_title_duration=json_data['reveal_title_duration'],
            unknown_0x34e18255=json_data['unknown_0x34e18255'],
            unknown_0x892ae90a=json_data['unknown_0x892ae90a'],
            unknown_0x5bed9219=json_data['unknown_0x5bed9219'],
            unknown_0x039bddff=json_data['unknown_0x039bddff'],
            unknown_0x48b54a2f=json_data['unknown_0x48b54a2f'],
            unknown_0x81402f46=json_data['unknown_0x81402f46'],
            unknown_0xe328a2c3=json_data['unknown_0xe328a2c3'],
            unknown_0xcab973a9=json_data['unknown_0xcab973a9'],
            unknown_0x407911ad=json_data['unknown_0x407911ad'],
            reveal_buttons_duration=json_data['reveal_buttons_duration'],
            unknown_0xf0c51c84=json_data['unknown_0xf0c51c84'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0xac6cbf9d': self.unknown_0xac6cbf9d,
            'initial_duration': self.initial_duration,
            'reveal_title_duration': self.reveal_title_duration,
            'unknown_0x34e18255': self.unknown_0x34e18255,
            'unknown_0x892ae90a': self.unknown_0x892ae90a,
            'unknown_0x5bed9219': self.unknown_0x5bed9219,
            'unknown_0x039bddff': self.unknown_0x039bddff,
            'unknown_0x48b54a2f': self.unknown_0x48b54a2f,
            'unknown_0x81402f46': self.unknown_0x81402f46,
            'unknown_0xe328a2c3': self.unknown_0xe328a2c3,
            'unknown_0xcab973a9': self.unknown_0xcab973a9,
            'unknown_0x407911ad': self.unknown_0x407911ad,
            'reveal_buttons_duration': self.reveal_buttons_duration,
            'unknown_0xf0c51c84': self.unknown_0xf0c51c84,
        }


def _decode_unknown_0xac6cbf9d(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reveal_title_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x34e18255(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x892ae90a(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x5bed9219(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x039bddff(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x48b54a2f(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x81402f46(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xe328a2c3(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xcab973a9(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0x407911ad(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_reveal_buttons_duration(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_unknown_0xf0c51c84(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xac6cbf9d: ('unknown_0xac6cbf9d', _decode_unknown_0xac6cbf9d),
    0x8e6c42f: ('initial_duration', _decode_initial_duration),
    0x4a4ac4c: ('reveal_title_duration', _decode_reveal_title_duration),
    0x34e18255: ('unknown_0x34e18255', _decode_unknown_0x34e18255),
    0x892ae90a: ('unknown_0x892ae90a', _decode_unknown_0x892ae90a),
    0x5bed9219: ('unknown_0x5bed9219', _decode_unknown_0x5bed9219),
    0x39bddff: ('unknown_0x039bddff', _decode_unknown_0x039bddff),
    0x48b54a2f: ('unknown_0x48b54a2f', _decode_unknown_0x48b54a2f),
    0x81402f46: ('unknown_0x81402f46', _decode_unknown_0x81402f46),
    0xe328a2c3: ('unknown_0xe328a2c3', _decode_unknown_0xe328a2c3),
    0xcab973a9: ('unknown_0xcab973a9', _decode_unknown_0xcab973a9),
    0x407911ad: ('unknown_0x407911ad', _decode_unknown_0x407911ad),
    0x6d5fd457: ('reveal_buttons_duration', _decode_reveal_buttons_duration),
    0xf0c51c84: ('unknown_0xf0c51c84', _decode_unknown_0xf0c51c84),
}
