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
    class UnknownStruct63Json(typing_extensions.TypedDict):
        unknown_0x348c9d90: float
        flight_sound_deceleration_k: float
        flight_sound: int
        flight_sound_low_pass_filter: json_util.JsonObject
        flight_sound_pitch: json_util.JsonObject
        flight_sound_volume: json_util.JsonObject
        caud: int
        unknown_0xbd894993: json_util.JsonObject
        flight_sound2_pitch: json_util.JsonObject
        flight_sound2_volume: json_util.JsonObject
        hit_player_sound: int
        swoop_interrupted_sound: int
    

@dataclasses.dataclass()
class UnknownStruct63(BaseProperty):
    unknown_0x348c9d90: float = dataclasses.field(default=20.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x348c9d90, original_name='Unknown'
        ),
    })
    flight_sound_deceleration_k: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7a7df6e3, original_name='FlightSoundDecelerationK'
        ),
    })
    flight_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe1e66b24, original_name='FlightSound'
        ),
    })
    flight_sound_low_pass_filter: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xb413c45f, original_name='FlightSoundLowPassFilter', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    flight_sound_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x76c7464c, original_name='FlightSoundPitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    flight_sound_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x10e05aaf, original_name='FlightSoundVolume', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    caud: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb0c2f5f6, original_name='CAUD'
        ),
    })
    unknown_0xbd894993: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xbd894993, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    flight_sound2_pitch: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x05291ef7, original_name='FlightSound2Pitch', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    flight_sound2_volume: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x4c20def3, original_name='FlightSound2Volume', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    hit_player_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x259c0939, original_name='HitPlayerSound'
        ),
    })
    swoop_interrupted_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xbe5f118d, original_name='SwoopInterruptedSound'
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
        assert property_id == 0x348c9d90
        unknown_0x348c9d90 = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7a7df6e3
        flight_sound_deceleration_k = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe1e66b24
        flight_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb413c45f
        flight_sound_low_pass_filter = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76c7464c
        flight_sound_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x10e05aaf
        flight_sound_volume = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0c2f5f6
        caud = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbd894993
        unknown_0xbd894993 = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x05291ef7
        flight_sound2_pitch = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4c20def3
        flight_sound2_volume = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x259c0939
        hit_player_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbe5f118d
        swoop_interrupted_sound = struct.unpack(">Q", data.read(8))[0]
    
        return cls(unknown_0x348c9d90, flight_sound_deceleration_k, flight_sound, flight_sound_low_pass_filter, flight_sound_pitch, flight_sound_volume, caud, unknown_0xbd894993, flight_sound2_pitch, flight_sound2_volume, hit_player_sound, swoop_interrupted_sound)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'4\x8c\x9d\x90')  # 0x348c9d90
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.unknown_0x348c9d90))

        data.write(b'z}\xf6\xe3')  # 0x7a7df6e3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.flight_sound_deceleration_k))

        data.write(b'\xe1\xe6k$')  # 0xe1e66b24
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.flight_sound))

        data.write(b'\xb4\x13\xc4_')  # 0xb413c45f
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_low_pass_filter.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xc7FL')  # 0x76c7464c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x10\xe0Z\xaf')  # 0x10e05aaf
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xc2\xf5\xf6')  # 0xb0c2f5f6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.caud))

        data.write(b'\xbd\x89I\x93')  # 0xbd894993
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_0xbd894993.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x05)\x1e\xf7')  # 0x5291ef7
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound2_pitch.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'L \xde\xf3')  # 0x4c20def3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.flight_sound2_volume.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'%\x9c\t9')  # 0x259c0939
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.hit_player_sound))

        data.write(b'\xbe_\x11\x8d')  # 0xbe5f118d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.swoop_interrupted_sound))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct63Json", data)
        return cls(
            unknown_0x348c9d90=json_data['unknown_0x348c9d90'],
            flight_sound_deceleration_k=json_data['flight_sound_deceleration_k'],
            flight_sound=json_data['flight_sound'],
            flight_sound_low_pass_filter=Spline.from_json(json_data['flight_sound_low_pass_filter']),
            flight_sound_pitch=Spline.from_json(json_data['flight_sound_pitch']),
            flight_sound_volume=Spline.from_json(json_data['flight_sound_volume']),
            caud=json_data['caud'],
            unknown_0xbd894993=Spline.from_json(json_data['unknown_0xbd894993']),
            flight_sound2_pitch=Spline.from_json(json_data['flight_sound2_pitch']),
            flight_sound2_volume=Spline.from_json(json_data['flight_sound2_volume']),
            hit_player_sound=json_data['hit_player_sound'],
            swoop_interrupted_sound=json_data['swoop_interrupted_sound'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown_0x348c9d90': self.unknown_0x348c9d90,
            'flight_sound_deceleration_k': self.flight_sound_deceleration_k,
            'flight_sound': self.flight_sound,
            'flight_sound_low_pass_filter': self.flight_sound_low_pass_filter.to_json(),
            'flight_sound_pitch': self.flight_sound_pitch.to_json(),
            'flight_sound_volume': self.flight_sound_volume.to_json(),
            'caud': self.caud,
            'unknown_0xbd894993': self.unknown_0xbd894993.to_json(),
            'flight_sound2_pitch': self.flight_sound2_pitch.to_json(),
            'flight_sound2_volume': self.flight_sound2_volume.to_json(),
            'hit_player_sound': self.hit_player_sound,
            'swoop_interrupted_sound': self.swoop_interrupted_sound,
        }


def _decode_unknown_0x348c9d90(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound_deceleration_k(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_flight_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_caud(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_hit_player_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_swoop_interrupted_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x348c9d90: ('unknown_0x348c9d90', _decode_unknown_0x348c9d90),
    0x7a7df6e3: ('flight_sound_deceleration_k', _decode_flight_sound_deceleration_k),
    0xe1e66b24: ('flight_sound', _decode_flight_sound),
    0xb413c45f: ('flight_sound_low_pass_filter', Spline.from_stream),
    0x76c7464c: ('flight_sound_pitch', Spline.from_stream),
    0x10e05aaf: ('flight_sound_volume', Spline.from_stream),
    0xb0c2f5f6: ('caud', _decode_caud),
    0xbd894993: ('unknown_0xbd894993', Spline.from_stream),
    0x5291ef7: ('flight_sound2_pitch', Spline.from_stream),
    0x4c20def3: ('flight_sound2_volume', Spline.from_stream),
    0x259c0939: ('hit_player_sound', _decode_hit_player_sound),
    0xbe5f118d: ('swoop_interrupted_sound', _decode_swoop_interrupted_sound),
}
