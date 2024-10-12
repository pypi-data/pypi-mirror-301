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
from retro_data_structures.properties.dkc_returns.archetypes.DebrisPropertiesOrientationEnum import DebrisPropertiesOrientationEnum
from retro_data_structures.properties.dkc_returns.archetypes.PeanutMaterialEffects import PeanutMaterialEffects
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct17 import UnknownStruct17
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class PeanutPropertiesJson(typing_extensions.TypedDict):
        sort_position_in_world: bool
        initial_direction: json_util.JsonValue
        speed: float
        spin_speed: json_util.JsonValue
        lifetime: float
        fade_out_start_percentage: float
        gravity: float
        model: int
        created_sound: int
        bounce_sound: int
        particle_system1: int
        particle_system1_scale: json_util.JsonValue
        particle_system1_uses_global_translation: bool
        particle_system1_uses_global_orientation: bool
        particle_system1_wait_for_particles_to_die: bool
        particle_system1_orientation: json_util.JsonObject
        bounce_particle_effect: int
        bounce_particle_scale: json_util.JsonValue
        bounce_effect_transform: json_util.JsonObject
        peanut_burn_effect: int
        peanut_kill_effect: int
        peanut_deflection_effect: int
        stun_sound: int
        fixed_bounce_speed_x: float
        fixed_bounce_speed_y: float
        num_material_effects: int
        material_effects1: json_util.JsonObject
        material_effects2: json_util.JsonObject
        material_effects3: json_util.JsonObject
        material_effects4: json_util.JsonObject
        material_effects5: json_util.JsonObject
        material_effects6: json_util.JsonObject
        material_effects7: json_util.JsonObject
        material_effects8: json_util.JsonObject
    

@dataclasses.dataclass()
class PeanutProperties(BaseProperty):
    sort_position_in_world: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x97ab7629, original_name='SortPositionInWorld'
        ),
    })
    initial_direction: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x01a0dfe6, original_name='InitialDirection', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    speed: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6392404e, original_name='Speed'
        ),
    })
    spin_speed: Vector = dataclasses.field(default_factory=lambda: Vector(x=-1.0, y=-1.0, z=-1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x5eb17e07, original_name='SpinSpeed', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    lifetime: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x32dc67f6, original_name='Lifetime'
        ),
    })
    fade_out_start_percentage: float = dataclasses.field(default=80.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6353c409, original_name='FadeOutStartPercentage'
        ),
    })
    gravity: float = dataclasses.field(default=25.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    model: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CMDL'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xc27ffa8f, original_name='Model'
        ),
    })
    created_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x93f8e0b0, original_name='CreatedSound'
        ),
    })
    bounce_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf1925576, original_name='BounceSound'
        ),
    })
    particle_system1: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x478d0aa3, original_name='ParticleSystem1'
        ),
    })
    particle_system1_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x19a6f71f, original_name='ParticleSystem1Scale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    particle_system1_uses_global_translation: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3b03a01e, original_name='ParticleSystem1UsesGlobalTranslation'
        ),
    })
    particle_system1_uses_global_orientation: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xdb1fa61c, original_name='ParticleSystem1UsesGlobalOrientation'
        ),
    })
    particle_system1_wait_for_particles_to_die: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3bdd2fed, original_name='ParticleSystem1WaitForParticlesToDie'
        ),
    })
    particle_system1_orientation: DebrisPropertiesOrientationEnum = dataclasses.field(default_factory=DebrisPropertiesOrientationEnum, metadata={
        'reflection': FieldReflection[DebrisPropertiesOrientationEnum](
            DebrisPropertiesOrientationEnum, id=0xf5dd4690, original_name='ParticleSystem1Orientation', from_json=DebrisPropertiesOrientationEnum.from_json, to_json=DebrisPropertiesOrientationEnum.to_json
        ),
    })
    bounce_particle_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x217c37c2, original_name='BounceParticleEffect'
        ),
    })
    bounce_particle_scale: Vector = dataclasses.field(default_factory=lambda: Vector(x=1.0, y=1.0, z=1.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0x60d6bf8e, original_name='BounceParticleScale', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    bounce_effect_transform: UnknownStruct17 = dataclasses.field(default_factory=UnknownStruct17, metadata={
        'reflection': FieldReflection[UnknownStruct17](
            UnknownStruct17, id=0xce59ebff, original_name='BounceEffectTransform', from_json=UnknownStruct17.from_json, to_json=UnknownStruct17.to_json
        ),
    })
    peanut_burn_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe93b1a2f, original_name='PeanutBurnEffect'
        ),
    })
    peanut_kill_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x71d494f4, original_name='PeanutKillEffect'
        ),
    })
    peanut_deflection_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xbd1a42af, original_name='PeanutDeflectionEffect'
        ),
    })
    stun_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x08000ec9, original_name='StunSound'
        ),
    })
    fixed_bounce_speed_x: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9bd94326, original_name='FixedBounceSpeedX'
        ),
    })
    fixed_bounce_speed_y: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x50859083, original_name='FixedBounceSpeedY'
        ),
    })
    num_material_effects: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x05a79779, original_name='NumMaterialEffects'
        ),
    })
    material_effects1: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0xe8d26bae, original_name='MaterialEffects1', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
        ),
    })
    material_effects2: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0xd1aac6ee, original_name='MaterialEffects2', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
        ),
    })
    material_effects3: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0xc682a22e, original_name='MaterialEffects3', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
        ),
    })
    material_effects4: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0xa35b9c6e, original_name='MaterialEffects4', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
        ),
    })
    material_effects5: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0xb473f8ae, original_name='MaterialEffects5', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
        ),
    })
    material_effects6: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0x8d0b55ee, original_name='MaterialEffects6', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
        ),
    })
    material_effects7: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0x9a23312e, original_name='MaterialEffects7', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
        ),
    })
    material_effects8: PeanutMaterialEffects = dataclasses.field(default_factory=PeanutMaterialEffects, metadata={
        'reflection': FieldReflection[PeanutMaterialEffects](
            PeanutMaterialEffects, id=0x46b9296e, original_name='MaterialEffects8', from_json=PeanutMaterialEffects.from_json, to_json=PeanutMaterialEffects.to_json
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
        if property_count != 34:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x97ab7629
        sort_position_in_world = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x01a0dfe6
        initial_direction = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6392404e
        speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5eb17e07
        spin_speed = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x32dc67f6
        lifetime = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6353c409
        fade_out_start_percentage = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc27ffa8f
        model = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x93f8e0b0
        created_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf1925576
        bounce_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x478d0aa3
        particle_system1 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x19a6f71f
        particle_system1_scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3b03a01e
        particle_system1_uses_global_translation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdb1fa61c
        particle_system1_uses_global_orientation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3bdd2fed
        particle_system1_wait_for_particles_to_die = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf5dd4690
        particle_system1_orientation = DebrisPropertiesOrientationEnum.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x217c37c2
        bounce_particle_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x60d6bf8e
        bounce_particle_scale = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xce59ebff
        bounce_effect_transform = UnknownStruct17.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe93b1a2f
        peanut_burn_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x71d494f4
        peanut_kill_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbd1a42af
        peanut_deflection_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x08000ec9
        stun_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9bd94326
        fixed_bounce_speed_x = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x50859083
        fixed_bounce_speed_y = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x05a79779
        num_material_effects = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe8d26bae
        material_effects1 = PeanutMaterialEffects.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd1aac6ee
        material_effects2 = PeanutMaterialEffects.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc682a22e
        material_effects3 = PeanutMaterialEffects.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa35b9c6e
        material_effects4 = PeanutMaterialEffects.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb473f8ae
        material_effects5 = PeanutMaterialEffects.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8d0b55ee
        material_effects6 = PeanutMaterialEffects.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9a23312e
        material_effects7 = PeanutMaterialEffects.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x46b9296e
        material_effects8 = PeanutMaterialEffects.from_stream(data, property_size)
    
        return cls(sort_position_in_world, initial_direction, speed, spin_speed, lifetime, fade_out_start_percentage, gravity, model, created_sound, bounce_sound, particle_system1, particle_system1_scale, particle_system1_uses_global_translation, particle_system1_uses_global_orientation, particle_system1_wait_for_particles_to_die, particle_system1_orientation, bounce_particle_effect, bounce_particle_scale, bounce_effect_transform, peanut_burn_effect, peanut_kill_effect, peanut_deflection_effect, stun_sound, fixed_bounce_speed_x, fixed_bounce_speed_y, num_material_effects, material_effects1, material_effects2, material_effects3, material_effects4, material_effects5, material_effects6, material_effects7, material_effects8)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00"')  # 34 properties

        data.write(b'\x97\xabv)')  # 0x97ab7629
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.sort_position_in_world))

        data.write(b'\x01\xa0\xdf\xe6')  # 0x1a0dfe6
        data.write(b'\x00\x0c')  # size
        self.initial_direction.to_stream(data)

        data.write(b'c\x92@N')  # 0x6392404e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.speed))

        data.write(b'^\xb1~\x07')  # 0x5eb17e07
        data.write(b'\x00\x0c')  # size
        self.spin_speed.to_stream(data)

        data.write(b'2\xdcg\xf6')  # 0x32dc67f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.lifetime))

        data.write(b'cS\xc4\t')  # 0x6353c409
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fade_out_start_percentage))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'\xc2\x7f\xfa\x8f')  # 0xc27ffa8f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.model))

        data.write(b'\x93\xf8\xe0\xb0')  # 0x93f8e0b0
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.created_sound))

        data.write(b'\xf1\x92Uv')  # 0xf1925576
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_sound))

        data.write(b'G\x8d\n\xa3')  # 0x478d0aa3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.particle_system1))

        data.write(b'\x19\xa6\xf7\x1f')  # 0x19a6f71f
        data.write(b'\x00\x0c')  # size
        self.particle_system1_scale.to_stream(data)

        data.write(b';\x03\xa0\x1e')  # 0x3b03a01e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_uses_global_translation))

        data.write(b'\xdb\x1f\xa6\x1c')  # 0xdb1fa61c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_uses_global_orientation))

        data.write(b';\xdd/\xed')  # 0x3bdd2fed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.particle_system1_wait_for_particles_to_die))

        data.write(b'\xf5\xddF\x90')  # 0xf5dd4690
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.particle_system1_orientation.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!|7\xc2')  # 0x217c37c2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.bounce_particle_effect))

        data.write(b'`\xd6\xbf\x8e')  # 0x60d6bf8e
        data.write(b'\x00\x0c')  # size
        self.bounce_particle_scale.to_stream(data)

        data.write(b'\xceY\xeb\xff')  # 0xce59ebff
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.bounce_effect_transform.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe9;\x1a/')  # 0xe93b1a2f
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.peanut_burn_effect))

        data.write(b'q\xd4\x94\xf4')  # 0x71d494f4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.peanut_kill_effect))

        data.write(b'\xbd\x1aB\xaf')  # 0xbd1a42af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.peanut_deflection_effect))

        data.write(b'\x08\x00\x0e\xc9')  # 0x8000ec9
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.stun_sound))

        data.write(b'\x9b\xd9C&')  # 0x9bd94326
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_bounce_speed_x))

        data.write(b'P\x85\x90\x83')  # 0x50859083
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.fixed_bounce_speed_y))

        data.write(b'\x05\xa7\x97y')  # 0x5a79779
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_material_effects))

        data.write(b'\xe8\xd2k\xae')  # 0xe8d26bae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects1.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd1\xaa\xc6\xee')  # 0xd1aac6ee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects2.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc6\x82\xa2.')  # 0xc682a22e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xa3[\x9cn')  # 0xa35b9c6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects4.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb4s\xf8\xae')  # 0xb473f8ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects5.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x8d\x0bU\xee')  # 0x8d0b55ee
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects6.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9a#1.')  # 0x9a23312e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects7.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'F\xb9)n')  # 0x46b9296e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.material_effects8.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PeanutPropertiesJson", data)
        return cls(
            sort_position_in_world=json_data['sort_position_in_world'],
            initial_direction=Vector.from_json(json_data['initial_direction']),
            speed=json_data['speed'],
            spin_speed=Vector.from_json(json_data['spin_speed']),
            lifetime=json_data['lifetime'],
            fade_out_start_percentage=json_data['fade_out_start_percentage'],
            gravity=json_data['gravity'],
            model=json_data['model'],
            created_sound=json_data['created_sound'],
            bounce_sound=json_data['bounce_sound'],
            particle_system1=json_data['particle_system1'],
            particle_system1_scale=Vector.from_json(json_data['particle_system1_scale']),
            particle_system1_uses_global_translation=json_data['particle_system1_uses_global_translation'],
            particle_system1_uses_global_orientation=json_data['particle_system1_uses_global_orientation'],
            particle_system1_wait_for_particles_to_die=json_data['particle_system1_wait_for_particles_to_die'],
            particle_system1_orientation=DebrisPropertiesOrientationEnum.from_json(json_data['particle_system1_orientation']),
            bounce_particle_effect=json_data['bounce_particle_effect'],
            bounce_particle_scale=Vector.from_json(json_data['bounce_particle_scale']),
            bounce_effect_transform=UnknownStruct17.from_json(json_data['bounce_effect_transform']),
            peanut_burn_effect=json_data['peanut_burn_effect'],
            peanut_kill_effect=json_data['peanut_kill_effect'],
            peanut_deflection_effect=json_data['peanut_deflection_effect'],
            stun_sound=json_data['stun_sound'],
            fixed_bounce_speed_x=json_data['fixed_bounce_speed_x'],
            fixed_bounce_speed_y=json_data['fixed_bounce_speed_y'],
            num_material_effects=json_data['num_material_effects'],
            material_effects1=PeanutMaterialEffects.from_json(json_data['material_effects1']),
            material_effects2=PeanutMaterialEffects.from_json(json_data['material_effects2']),
            material_effects3=PeanutMaterialEffects.from_json(json_data['material_effects3']),
            material_effects4=PeanutMaterialEffects.from_json(json_data['material_effects4']),
            material_effects5=PeanutMaterialEffects.from_json(json_data['material_effects5']),
            material_effects6=PeanutMaterialEffects.from_json(json_data['material_effects6']),
            material_effects7=PeanutMaterialEffects.from_json(json_data['material_effects7']),
            material_effects8=PeanutMaterialEffects.from_json(json_data['material_effects8']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'sort_position_in_world': self.sort_position_in_world,
            'initial_direction': self.initial_direction.to_json(),
            'speed': self.speed,
            'spin_speed': self.spin_speed.to_json(),
            'lifetime': self.lifetime,
            'fade_out_start_percentage': self.fade_out_start_percentage,
            'gravity': self.gravity,
            'model': self.model,
            'created_sound': self.created_sound,
            'bounce_sound': self.bounce_sound,
            'particle_system1': self.particle_system1,
            'particle_system1_scale': self.particle_system1_scale.to_json(),
            'particle_system1_uses_global_translation': self.particle_system1_uses_global_translation,
            'particle_system1_uses_global_orientation': self.particle_system1_uses_global_orientation,
            'particle_system1_wait_for_particles_to_die': self.particle_system1_wait_for_particles_to_die,
            'particle_system1_orientation': self.particle_system1_orientation.to_json(),
            'bounce_particle_effect': self.bounce_particle_effect,
            'bounce_particle_scale': self.bounce_particle_scale.to_json(),
            'bounce_effect_transform': self.bounce_effect_transform.to_json(),
            'peanut_burn_effect': self.peanut_burn_effect,
            'peanut_kill_effect': self.peanut_kill_effect,
            'peanut_deflection_effect': self.peanut_deflection_effect,
            'stun_sound': self.stun_sound,
            'fixed_bounce_speed_x': self.fixed_bounce_speed_x,
            'fixed_bounce_speed_y': self.fixed_bounce_speed_y,
            'num_material_effects': self.num_material_effects,
            'material_effects1': self.material_effects1.to_json(),
            'material_effects2': self.material_effects2.to_json(),
            'material_effects3': self.material_effects3.to_json(),
            'material_effects4': self.material_effects4.to_json(),
            'material_effects5': self.material_effects5.to_json(),
            'material_effects6': self.material_effects6.to_json(),
            'material_effects7': self.material_effects7.to_json(),
            'material_effects8': self.material_effects8.to_json(),
        }


def _decode_sort_position_in_world(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initial_direction(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_spin_speed(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_lifetime(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fade_out_start_percentage(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_model(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_created_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bounce_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_particle_system1(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_particle_system1_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_particle_system1_uses_global_translation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_uses_global_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_particle_system1_wait_for_particles_to_die(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_bounce_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_bounce_particle_scale(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_peanut_burn_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_peanut_kill_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_peanut_deflection_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_stun_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_fixed_bounce_speed_x(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_fixed_bounce_speed_y(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_num_material_effects(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97ab7629: ('sort_position_in_world', _decode_sort_position_in_world),
    0x1a0dfe6: ('initial_direction', _decode_initial_direction),
    0x6392404e: ('speed', _decode_speed),
    0x5eb17e07: ('spin_speed', _decode_spin_speed),
    0x32dc67f6: ('lifetime', _decode_lifetime),
    0x6353c409: ('fade_out_start_percentage', _decode_fade_out_start_percentage),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0xc27ffa8f: ('model', _decode_model),
    0x93f8e0b0: ('created_sound', _decode_created_sound),
    0xf1925576: ('bounce_sound', _decode_bounce_sound),
    0x478d0aa3: ('particle_system1', _decode_particle_system1),
    0x19a6f71f: ('particle_system1_scale', _decode_particle_system1_scale),
    0x3b03a01e: ('particle_system1_uses_global_translation', _decode_particle_system1_uses_global_translation),
    0xdb1fa61c: ('particle_system1_uses_global_orientation', _decode_particle_system1_uses_global_orientation),
    0x3bdd2fed: ('particle_system1_wait_for_particles_to_die', _decode_particle_system1_wait_for_particles_to_die),
    0xf5dd4690: ('particle_system1_orientation', DebrisPropertiesOrientationEnum.from_stream),
    0x217c37c2: ('bounce_particle_effect', _decode_bounce_particle_effect),
    0x60d6bf8e: ('bounce_particle_scale', _decode_bounce_particle_scale),
    0xce59ebff: ('bounce_effect_transform', UnknownStruct17.from_stream),
    0xe93b1a2f: ('peanut_burn_effect', _decode_peanut_burn_effect),
    0x71d494f4: ('peanut_kill_effect', _decode_peanut_kill_effect),
    0xbd1a42af: ('peanut_deflection_effect', _decode_peanut_deflection_effect),
    0x8000ec9: ('stun_sound', _decode_stun_sound),
    0x9bd94326: ('fixed_bounce_speed_x', _decode_fixed_bounce_speed_x),
    0x50859083: ('fixed_bounce_speed_y', _decode_fixed_bounce_speed_y),
    0x5a79779: ('num_material_effects', _decode_num_material_effects),
    0xe8d26bae: ('material_effects1', PeanutMaterialEffects.from_stream),
    0xd1aac6ee: ('material_effects2', PeanutMaterialEffects.from_stream),
    0xc682a22e: ('material_effects3', PeanutMaterialEffects.from_stream),
    0xa35b9c6e: ('material_effects4', PeanutMaterialEffects.from_stream),
    0xb473f8ae: ('material_effects5', PeanutMaterialEffects.from_stream),
    0x8d0b55ee: ('material_effects6', PeanutMaterialEffects.from_stream),
    0x9a23312e: ('material_effects7', PeanutMaterialEffects.from_stream),
    0x46b9296e: ('material_effects8', PeanutMaterialEffects.from_stream),
}
