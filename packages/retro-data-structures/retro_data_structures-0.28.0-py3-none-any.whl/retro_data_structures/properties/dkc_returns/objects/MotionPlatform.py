# Generated File
from __future__ import annotations

import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.field_reflection import FieldReflection
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.Convergence import Convergence
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties
from retro_data_structures.properties.dkc_returns.archetypes.PlatformMotionProperties import PlatformMotionProperties

if typing.TYPE_CHECKING:
    class MotionPlatformJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        motion_properties: json_util.JsonObject
        max_velocity: float
        elevation_velocity: float
        radius: float
        elevation: float
        max_elevation: float
        min_elevation: float
        direction: int
        convergence: json_util.JsonObject
    

@dataclasses.dataclass()
class MotionPlatform(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    motion_properties: PlatformMotionProperties = dataclasses.field(default_factory=PlatformMotionProperties, metadata={
        'reflection': FieldReflection[PlatformMotionProperties](
            PlatformMotionProperties, id=0x0a9dbf91, original_name='MotionProperties', from_json=PlatformMotionProperties.from_json, to_json=PlatformMotionProperties.to_json
        ),
    })
    max_velocity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe4f89c8f, original_name='MaxVelocity'
        ),
    })
    elevation_velocity: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x3b3b92a6, original_name='ElevationVelocity'
        ),
    })
    radius: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x78c507eb, original_name='Radius'
        ),
    })
    elevation: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc5384200, original_name='Elevation'
        ),
    })
    max_elevation: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcc6806a1, original_name='MaxElevation'
        ),
    })
    min_elevation: float = dataclasses.field(default=-1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd9e3d253, original_name='MinElevation'
        ),
    })
    direction: enums.Direction = dataclasses.field(default=enums.Direction.Unknown1, metadata={
        'reflection': FieldReflection[enums.Direction](
            enums.Direction, id=0x0a441e0c, original_name='Direction', from_json=enums.Direction.from_json, to_json=enums.Direction.to_json
        ),
    })
    convergence: Convergence = dataclasses.field(default_factory=Convergence, metadata={
        'reflection': FieldReflection[Convergence](
            Convergence, id=0x56f4bc93, original_name='Convergence', from_json=Convergence.from_json, to_json=Convergence.to_json
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> str | None:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'MNPL'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    @classmethod
    def _fast_decode(cls, data: typing.BinaryIO, property_count: int) -> typing_extensions.Self | None:
        if property_count != 10:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0a9dbf91
        motion_properties = PlatformMotionProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe4f89c8f
        max_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3b3b92a6
        elevation_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x78c507eb
        radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc5384200
        elevation = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcc6806a1
        max_elevation = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd9e3d253
        min_elevation = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0a441e0c
        direction = enums.Direction.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x56f4bc93
        convergence = Convergence.from_stream(data, property_size)
    
        return cls(editor_properties, motion_properties, max_velocity, elevation_velocity, radius, elevation, max_elevation, min_elevation, direction, convergence)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\n')  # 10 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\n\x9d\xbf\x91')  # 0xa9dbf91
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.motion_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe4\xf8\x9c\x8f')  # 0xe4f89c8f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_velocity))

        data.write(b';;\x92\xa6')  # 0x3b3b92a6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.elevation_velocity))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'\xc58B\x00')  # 0xc5384200
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.elevation))

        data.write(b'\xcch\x06\xa1')  # 0xcc6806a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.max_elevation))

        data.write(b'\xd9\xe3\xd2S')  # 0xd9e3d253
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_elevation))

        data.write(b'\nD\x1e\x0c')  # 0xa441e0c
        data.write(b'\x00\x04')  # size
        self.direction.to_stream(data)

        data.write(b'V\xf4\xbc\x93')  # 0x56f4bc93
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.convergence.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("MotionPlatformJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            motion_properties=PlatformMotionProperties.from_json(json_data['motion_properties']),
            max_velocity=json_data['max_velocity'],
            elevation_velocity=json_data['elevation_velocity'],
            radius=json_data['radius'],
            elevation=json_data['elevation'],
            max_elevation=json_data['max_elevation'],
            min_elevation=json_data['min_elevation'],
            direction=enums.Direction.from_json(json_data['direction']),
            convergence=Convergence.from_json(json_data['convergence']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'motion_properties': self.motion_properties.to_json(),
            'max_velocity': self.max_velocity,
            'elevation_velocity': self.elevation_velocity,
            'radius': self.radius,
            'elevation': self.elevation,
            'max_elevation': self.max_elevation,
            'min_elevation': self.min_elevation,
            'direction': self.direction.to_json(),
            'convergence': self.convergence.to_json(),
        }


def _decode_max_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_elevation_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_max_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_elevation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_direction(data: typing.BinaryIO, property_size: int):
    return enums.Direction.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xa9dbf91: ('motion_properties', PlatformMotionProperties.from_stream),
    0xe4f89c8f: ('max_velocity', _decode_max_velocity),
    0x3b3b92a6: ('elevation_velocity', _decode_elevation_velocity),
    0x78c507eb: ('radius', _decode_radius),
    0xc5384200: ('elevation', _decode_elevation),
    0xcc6806a1: ('max_elevation', _decode_max_elevation),
    0xd9e3d253: ('min_elevation', _decode_min_elevation),
    0xa441e0c: ('direction', _decode_direction),
    0x56f4bc93: ('convergence', Convergence.from_stream),
}
