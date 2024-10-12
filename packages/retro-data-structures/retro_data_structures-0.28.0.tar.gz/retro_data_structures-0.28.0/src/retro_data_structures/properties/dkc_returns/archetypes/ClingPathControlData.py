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
import retro_data_structures.enums.dkc_returns as enums
from retro_data_structures.properties.dkc_returns.archetypes.MaterialType import MaterialType

if typing.TYPE_CHECKING:
    class ClingPathControlDataJson(typing_extensions.TypedDict):
        cling_path_control_struct: json_util.JsonObject
        can_player_walk_off_cling: bool
        lock_distance_override: float
        use_fixed_lateral_jump: int
    

@dataclasses.dataclass()
class ClingPathControlData(BaseProperty):
    cling_path_control_struct: MaterialType = dataclasses.field(default_factory=MaterialType, metadata={
        'reflection': FieldReflection[MaterialType](
            MaterialType, id=0xfa166886, original_name='ClingPathControlStruct', from_json=MaterialType.from_json, to_json=MaterialType.to_json
        ),
    })
    can_player_walk_off_cling: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf70befc0, original_name='CanPlayerWalkOffCling'
        ),
    })
    lock_distance_override: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd7d2b3de, original_name='LockDistanceOverride'
        ),
    })
    use_fixed_lateral_jump: enums.UseFixedLateralJump = dataclasses.field(default=enums.UseFixedLateralJump.Unknown1, metadata={
        'reflection': FieldReflection[enums.UseFixedLateralJump](
            enums.UseFixedLateralJump, id=0x8c9927c2, original_name='UseFixedLateralJump', from_json=enums.UseFixedLateralJump.from_json, to_json=enums.UseFixedLateralJump.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfa166886
        cling_path_control_struct = MaterialType.from_stream(data, property_size, default_override={'material_type': 4042527608})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf70befc0
        can_player_walk_off_cling = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd7d2b3de
        lock_distance_override = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8c9927c2
        use_fixed_lateral_jump = enums.UseFixedLateralJump.from_stream(data)
    
        return cls(cling_path_control_struct, can_player_walk_off_cling, lock_distance_override, use_fixed_lateral_jump)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x04')  # 4 properties

        data.write(b'\xfa\x16h\x86')  # 0xfa166886
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.cling_path_control_struct.to_stream(data, default_override={'material_type': 4042527608})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf7\x0b\xef\xc0')  # 0xf70befc0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_player_walk_off_cling))

        data.write(b'\xd7\xd2\xb3\xde')  # 0xd7d2b3de
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lock_distance_override))

        data.write(b"\x8c\x99'\xc2")  # 0x8c9927c2
        data.write(b'\x00\x04')  # size
        self.use_fixed_lateral_jump.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ClingPathControlDataJson", data)
        return cls(
            cling_path_control_struct=MaterialType.from_json(json_data['cling_path_control_struct']),
            can_player_walk_off_cling=json_data['can_player_walk_off_cling'],
            lock_distance_override=json_data['lock_distance_override'],
            use_fixed_lateral_jump=enums.UseFixedLateralJump.from_json(json_data['use_fixed_lateral_jump']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'cling_path_control_struct': self.cling_path_control_struct.to_json(),
            'can_player_walk_off_cling': self.can_player_walk_off_cling,
            'lock_distance_override': self.lock_distance_override,
            'use_fixed_lateral_jump': self.use_fixed_lateral_jump.to_json(),
        }


def _decode_cling_path_control_struct(data: typing.BinaryIO, property_size: int):
    return MaterialType.from_stream(data, property_size, default_override={'material_type': 4042527608})


def _decode_can_player_walk_off_cling(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_lock_distance_override(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_fixed_lateral_jump(data: typing.BinaryIO, property_size: int):
    return enums.UseFixedLateralJump.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xfa166886: ('cling_path_control_struct', _decode_cling_path_control_struct),
    0xf70befc0: ('can_player_walk_off_cling', _decode_can_player_walk_off_cling),
    0xd7d2b3de: ('lock_distance_override', _decode_lock_distance_override),
    0x8c9927c2: ('use_fixed_lateral_jump', _decode_use_fixed_lateral_jump),
}
