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
from retro_data_structures.properties.dkc_returns.archetypes.TriggerShape import TriggerShape
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class GroundPoundDetectorDataJson(typing_extensions.TypedDict):
        use_detection_shape_and_ignore_radius: bool
        trigger_shape: json_util.JsonObject
        detection_vector: json_util.JsonValue
        detection_angle_tolerance: float
        radius: float
        ignore_dk: bool
        ignore_diddy: bool
        ignore_rambi: bool
        use_originator_transform: bool
    

@dataclasses.dataclass()
class GroundPoundDetectorData(BaseProperty):
    use_detection_shape_and_ignore_radius: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf29db958, original_name='UseDetectionShapeAndIgnoreRadius'
        ),
    })
    trigger_shape: TriggerShape = dataclasses.field(default_factory=TriggerShape, metadata={
        'reflection': FieldReflection[TriggerShape](
            TriggerShape, id=0xbb2c54e1, original_name='TriggerShape', from_json=TriggerShape.from_json, to_json=TriggerShape.to_json
        ),
    })
    detection_vector: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x45a46d11, original_name='DetectionVector', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    detection_angle_tolerance: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xba48e853, original_name='DetectionAngleTolerance'
        ),
    })
    radius: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x78c507eb, original_name='Radius'
        ),
    })
    ignore_dk: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x25ee5ffb, original_name='IgnoreDk'
        ),
    })
    ignore_diddy: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x62a71363, original_name='IgnoreDiddy'
        ),
    })
    ignore_rambi: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4db90261, original_name='IgnoreRambi'
        ),
    })
    use_originator_transform: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x035a5e10, original_name='UseOriginatorTransform'
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
        if property_count != 9:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf29db958
        use_detection_shape_and_ignore_radius = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbb2c54e1
        trigger_shape = TriggerShape.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x45a46d11
        detection_vector = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xba48e853
        detection_angle_tolerance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x78c507eb
        radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x25ee5ffb
        ignore_dk = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x62a71363
        ignore_diddy = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4db90261
        ignore_rambi = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x035a5e10
        use_originator_transform = struct.unpack('>?', data.read(1))[0]
    
        return cls(use_detection_shape_and_ignore_radius, trigger_shape, detection_vector, detection_angle_tolerance, radius, ignore_dk, ignore_diddy, ignore_rambi, use_originator_transform)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\xf2\x9d\xb9X')  # 0xf29db958
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_detection_shape_and_ignore_radius))

        data.write(b'\xbb,T\xe1')  # 0xbb2c54e1
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.trigger_shape.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'E\xa4m\x11')  # 0x45a46d11
        data.write(b'\x00\x0c')  # size
        self.detection_vector.to_stream(data)

        data.write(b'\xbaH\xe8S')  # 0xba48e853
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.detection_angle_tolerance))

        data.write(b'x\xc5\x07\xeb')  # 0x78c507eb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.radius))

        data.write(b'%\xee_\xfb')  # 0x25ee5ffb
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_dk))

        data.write(b'b\xa7\x13c')  # 0x62a71363
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_diddy))

        data.write(b'M\xb9\x02a')  # 0x4db90261
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_rambi))

        data.write(b'\x03Z^\x10')  # 0x35a5e10
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_originator_transform))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("GroundPoundDetectorDataJson", data)
        return cls(
            use_detection_shape_and_ignore_radius=json_data['use_detection_shape_and_ignore_radius'],
            trigger_shape=TriggerShape.from_json(json_data['trigger_shape']),
            detection_vector=Vector.from_json(json_data['detection_vector']),
            detection_angle_tolerance=json_data['detection_angle_tolerance'],
            radius=json_data['radius'],
            ignore_dk=json_data['ignore_dk'],
            ignore_diddy=json_data['ignore_diddy'],
            ignore_rambi=json_data['ignore_rambi'],
            use_originator_transform=json_data['use_originator_transform'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'use_detection_shape_and_ignore_radius': self.use_detection_shape_and_ignore_radius,
            'trigger_shape': self.trigger_shape.to_json(),
            'detection_vector': self.detection_vector.to_json(),
            'detection_angle_tolerance': self.detection_angle_tolerance,
            'radius': self.radius,
            'ignore_dk': self.ignore_dk,
            'ignore_diddy': self.ignore_diddy,
            'ignore_rambi': self.ignore_rambi,
            'use_originator_transform': self.use_originator_transform,
        }


def _decode_use_detection_shape_and_ignore_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_detection_vector(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_detection_angle_tolerance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_dk(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_diddy(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignore_rambi(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_originator_transform(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf29db958: ('use_detection_shape_and_ignore_radius', _decode_use_detection_shape_and_ignore_radius),
    0xbb2c54e1: ('trigger_shape', TriggerShape.from_stream),
    0x45a46d11: ('detection_vector', _decode_detection_vector),
    0xba48e853: ('detection_angle_tolerance', _decode_detection_angle_tolerance),
    0x78c507eb: ('radius', _decode_radius),
    0x25ee5ffb: ('ignore_dk', _decode_ignore_dk),
    0x62a71363: ('ignore_diddy', _decode_ignore_diddy),
    0x4db90261: ('ignore_rambi', _decode_ignore_rambi),
    0x35a5e10: ('use_originator_transform', _decode_use_originator_transform),
}
