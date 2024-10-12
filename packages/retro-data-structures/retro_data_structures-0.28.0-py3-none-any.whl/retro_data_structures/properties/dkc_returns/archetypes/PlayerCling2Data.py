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
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class PlayerCling2DataJson(typing_extensions.TypedDict):
        run_half_cone_for_stick: float
        off_angle_stick_response: json_util.JsonObject
        acceleration_factor: json_util.JsonObject
        max_velocity_factor: json_util.JsonObject
        search_distance: float
        close_distance: float
        close_speed: float
        lock_distance: float
        ground_pound_window: float
        orientation_turn_speed: float
        surface_alignment_turn_speed: float
        air_surface_alignment_turn_speed: float
        jump_lateral_speed_multiplier: float
        jump_lateral_initial_vert_speed: float
        jump_lateral_modify_gravity_time: float
        jump_angled_speed_multiplier: float
        damage_effect: int
        damage_effect_offset: json_util.JsonValue
        shield_damage_effect: int
        shield_damage_effect_offset: json_util.JsonValue
        angled_jump_launch_sound: int
        on_edge_range: float
    

@dataclasses.dataclass()
class PlayerCling2Data(BaseProperty):
    run_half_cone_for_stick: float = dataclasses.field(default=50.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x29a73264, original_name='RunHalfConeForStick'
        ),
    })
    off_angle_stick_response: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0x6bd22c75, original_name='OffAngleStickResponse', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    acceleration_factor: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xb0b17d58, original_name='AccelerationFactor', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    max_velocity_factor: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xc47fe8aa, original_name='MaxVelocityFactor', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    search_distance: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xa8ac80dd, original_name='SearchDistance'
        ),
    })
    close_distance: float = dataclasses.field(default=6.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xb5d2e300, original_name='CloseDistance'
        ),
    })
    close_speed: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x71b142ca, original_name='CloseSpeed'
        ),
    })
    lock_distance: float = dataclasses.field(default=0.800000011920929, metadata={
        'reflection': FieldReflection[float](
            float, id=0xea7788c7, original_name='LockDistance'
        ),
    })
    ground_pound_window: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x68d787b4, original_name='GroundPoundWindow'
        ),
    })
    orientation_turn_speed: float = dataclasses.field(default=900.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xcd3b5f5c, original_name='OrientationTurnSpeed'
        ),
    })
    surface_alignment_turn_speed: float = dataclasses.field(default=10800.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x790ff19f, original_name='SurfaceAlignmentTurnSpeed'
        ),
    })
    air_surface_alignment_turn_speed: float = dataclasses.field(default=500.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x42774887, original_name='AirSurfaceAlignmentTurnSpeed'
        ),
    })
    jump_lateral_speed_multiplier: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xaa3e2346, original_name='JumpLateralSpeedMultiplier'
        ),
    })
    jump_lateral_initial_vert_speed: float = dataclasses.field(default=0.4000000059604645, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc43d659a, original_name='JumpLateralInitialVertSpeed'
        ),
    })
    jump_lateral_modify_gravity_time: float = dataclasses.field(default=0.25, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5e810459, original_name='JumpLateralModifyGravityTime'
        ),
    })
    jump_angled_speed_multiplier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe5a5160e, original_name='JumpAngledSpeedMultiplier'
        ),
    })
    damage_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc110ed44, original_name='DamageEffect'
        ),
    })
    damage_effect_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=-2.0, y=0.4000000059604645, z=1.600000023841858), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x81457fac, original_name='DamageEffectOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    shield_damage_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x49395e36, original_name='ShieldDamageEffect'
        ),
    })
    shield_damage_effect_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=0.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x82d00cd4, original_name='ShieldDamageEffectOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    angled_jump_launch_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1999e3d7, original_name='AngledJumpLaunchSound'
        ),
    })
    on_edge_range: float = dataclasses.field(default=1.100000023841858, metadata={
        'reflection': FieldReflection[float](
            float, id=0x40b3da44, original_name='OnEdgeRange'
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
        if property_count != 22:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x29a73264
        run_half_cone_for_stick = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6bd22c75
        off_angle_stick_response = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0b17d58
        acceleration_factor = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc47fe8aa
        max_velocity_factor = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa8ac80dd
        search_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb5d2e300
        close_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x71b142ca
        close_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xea7788c7
        lock_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68d787b4
        ground_pound_window = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcd3b5f5c
        orientation_turn_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x790ff19f
        surface_alignment_turn_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x42774887
        air_surface_alignment_turn_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xaa3e2346
        jump_lateral_speed_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc43d659a
        jump_lateral_initial_vert_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5e810459
        jump_lateral_modify_gravity_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe5a5160e
        jump_angled_speed_multiplier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc110ed44
        damage_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x81457fac
        damage_effect_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x49395e36
        shield_damage_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x82d00cd4
        shield_damage_effect_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1999e3d7
        angled_jump_launch_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x40b3da44
        on_edge_range = struct.unpack('>f', data.read(4))[0]
    
        return cls(run_half_cone_for_stick, off_angle_stick_response, acceleration_factor, max_velocity_factor, search_distance, close_distance, close_speed, lock_distance, ground_pound_window, orientation_turn_speed, surface_alignment_turn_speed, air_surface_alignment_turn_speed, jump_lateral_speed_multiplier, jump_lateral_initial_vert_speed, jump_lateral_modify_gravity_time, jump_angled_speed_multiplier, damage_effect, damage_effect_offset, shield_damage_effect, shield_damage_effect_offset, angled_jump_launch_sound, on_edge_range)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x16')  # 22 properties

        data.write(b')\xa72d')  # 0x29a73264
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.run_half_cone_for_stick))

        data.write(b'k\xd2,u')  # 0x6bd22c75
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.off_angle_stick_response.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb0\xb1}X')  # 0xb0b17d58
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.acceleration_factor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc4\x7f\xe8\xaa')  # 0xc47fe8aa
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.max_velocity_factor.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa8\xac\x80\xdd')  # 0xa8ac80dd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.search_distance))

        data.write(b'\xb5\xd2\xe3\x00')  # 0xb5d2e300
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.close_distance))

        data.write(b'q\xb1B\xca')  # 0x71b142ca
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.close_speed))

        data.write(b'\xeaw\x88\xc7')  # 0xea7788c7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_distance))

        data.write(b'h\xd7\x87\xb4')  # 0x68d787b4
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_window))

        data.write(b'\xcd;_\\')  # 0xcd3b5f5c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.orientation_turn_speed))

        data.write(b'y\x0f\xf1\x9f')  # 0x790ff19f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.surface_alignment_turn_speed))

        data.write(b'BwH\x87')  # 0x42774887
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.air_surface_alignment_turn_speed))

        data.write(b'\xaa>#F')  # 0xaa3e2346
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_lateral_speed_multiplier))

        data.write(b'\xc4=e\x9a')  # 0xc43d659a
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_lateral_initial_vert_speed))

        data.write(b'^\x81\x04Y')  # 0x5e810459
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_lateral_modify_gravity_time))

        data.write(b'\xe5\xa5\x16\x0e')  # 0xe5a5160e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.jump_angled_speed_multiplier))

        data.write(b'\xc1\x10\xedD')  # 0xc110ed44
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.damage_effect))

        data.write(b'\x81E\x7f\xac')  # 0x81457fac
        data.write(b'\x00\x0c')  # size
        self.damage_effect_offset.to_stream(data)

        data.write(b'I9^6')  # 0x49395e36
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.shield_damage_effect))

        data.write(b'\x82\xd0\x0c\xd4')  # 0x82d00cd4
        data.write(b'\x00\x0c')  # size
        self.shield_damage_effect_offset.to_stream(data)

        data.write(b'\x19\x99\xe3\xd7')  # 0x1999e3d7
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.angled_jump_launch_sound))

        data.write(b'@\xb3\xdaD')  # 0x40b3da44
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.on_edge_range))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerCling2DataJson", data)
        return cls(
            run_half_cone_for_stick=json_data['run_half_cone_for_stick'],
            off_angle_stick_response=Spline.from_json(json_data['off_angle_stick_response']),
            acceleration_factor=Spline.from_json(json_data['acceleration_factor']),
            max_velocity_factor=Spline.from_json(json_data['max_velocity_factor']),
            search_distance=json_data['search_distance'],
            close_distance=json_data['close_distance'],
            close_speed=json_data['close_speed'],
            lock_distance=json_data['lock_distance'],
            ground_pound_window=json_data['ground_pound_window'],
            orientation_turn_speed=json_data['orientation_turn_speed'],
            surface_alignment_turn_speed=json_data['surface_alignment_turn_speed'],
            air_surface_alignment_turn_speed=json_data['air_surface_alignment_turn_speed'],
            jump_lateral_speed_multiplier=json_data['jump_lateral_speed_multiplier'],
            jump_lateral_initial_vert_speed=json_data['jump_lateral_initial_vert_speed'],
            jump_lateral_modify_gravity_time=json_data['jump_lateral_modify_gravity_time'],
            jump_angled_speed_multiplier=json_data['jump_angled_speed_multiplier'],
            damage_effect=json_data['damage_effect'],
            damage_effect_offset=Vector.from_json(json_data['damage_effect_offset']),
            shield_damage_effect=json_data['shield_damage_effect'],
            shield_damage_effect_offset=Vector.from_json(json_data['shield_damage_effect_offset']),
            angled_jump_launch_sound=json_data['angled_jump_launch_sound'],
            on_edge_range=json_data['on_edge_range'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'run_half_cone_for_stick': self.run_half_cone_for_stick,
            'off_angle_stick_response': self.off_angle_stick_response.to_json(),
            'acceleration_factor': self.acceleration_factor.to_json(),
            'max_velocity_factor': self.max_velocity_factor.to_json(),
            'search_distance': self.search_distance,
            'close_distance': self.close_distance,
            'close_speed': self.close_speed,
            'lock_distance': self.lock_distance,
            'ground_pound_window': self.ground_pound_window,
            'orientation_turn_speed': self.orientation_turn_speed,
            'surface_alignment_turn_speed': self.surface_alignment_turn_speed,
            'air_surface_alignment_turn_speed': self.air_surface_alignment_turn_speed,
            'jump_lateral_speed_multiplier': self.jump_lateral_speed_multiplier,
            'jump_lateral_initial_vert_speed': self.jump_lateral_initial_vert_speed,
            'jump_lateral_modify_gravity_time': self.jump_lateral_modify_gravity_time,
            'jump_angled_speed_multiplier': self.jump_angled_speed_multiplier,
            'damage_effect': self.damage_effect,
            'damage_effect_offset': self.damage_effect_offset.to_json(),
            'shield_damage_effect': self.shield_damage_effect,
            'shield_damage_effect_offset': self.shield_damage_effect_offset.to_json(),
            'angled_jump_launch_sound': self.angled_jump_launch_sound,
            'on_edge_range': self.on_edge_range,
        }


def _decode_run_half_cone_for_stick(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_search_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_close_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_close_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_lock_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ground_pound_window(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_orientation_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_surface_alignment_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_air_surface_alignment_turn_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_lateral_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_lateral_initial_vert_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_lateral_modify_gravity_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_jump_angled_speed_multiplier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_damage_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_damage_effect_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_shield_damage_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_shield_damage_effect_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_angled_jump_launch_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_on_edge_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x29a73264: ('run_half_cone_for_stick', _decode_run_half_cone_for_stick),
    0x6bd22c75: ('off_angle_stick_response', Spline.from_stream),
    0xb0b17d58: ('acceleration_factor', Spline.from_stream),
    0xc47fe8aa: ('max_velocity_factor', Spline.from_stream),
    0xa8ac80dd: ('search_distance', _decode_search_distance),
    0xb5d2e300: ('close_distance', _decode_close_distance),
    0x71b142ca: ('close_speed', _decode_close_speed),
    0xea7788c7: ('lock_distance', _decode_lock_distance),
    0x68d787b4: ('ground_pound_window', _decode_ground_pound_window),
    0xcd3b5f5c: ('orientation_turn_speed', _decode_orientation_turn_speed),
    0x790ff19f: ('surface_alignment_turn_speed', _decode_surface_alignment_turn_speed),
    0x42774887: ('air_surface_alignment_turn_speed', _decode_air_surface_alignment_turn_speed),
    0xaa3e2346: ('jump_lateral_speed_multiplier', _decode_jump_lateral_speed_multiplier),
    0xc43d659a: ('jump_lateral_initial_vert_speed', _decode_jump_lateral_initial_vert_speed),
    0x5e810459: ('jump_lateral_modify_gravity_time', _decode_jump_lateral_modify_gravity_time),
    0xe5a5160e: ('jump_angled_speed_multiplier', _decode_jump_angled_speed_multiplier),
    0xc110ed44: ('damage_effect', _decode_damage_effect),
    0x81457fac: ('damage_effect_offset', _decode_damage_effect_offset),
    0x49395e36: ('shield_damage_effect', _decode_shield_damage_effect),
    0x82d00cd4: ('shield_damage_effect_offset', _decode_shield_damage_effect_offset),
    0x1999e3d7: ('angled_jump_launch_sound', _decode_angled_jump_launch_sound),
    0x40b3da44: ('on_edge_range', _decode_on_edge_range),
}
