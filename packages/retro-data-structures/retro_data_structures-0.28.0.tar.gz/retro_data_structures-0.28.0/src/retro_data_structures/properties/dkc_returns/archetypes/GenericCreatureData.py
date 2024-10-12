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
from retro_data_structures.properties.dkc_returns.archetypes.AnimGridModifierData import AnimGridModifierData
from retro_data_structures.properties.dkc_returns.archetypes.CollisionActorModifierData import CollisionActorModifierData
from retro_data_structures.properties.dkc_returns.archetypes.DashModifierData import DashModifierData
from retro_data_structures.properties.dkc_returns.archetypes.DespawnRules import DespawnRules
from retro_data_structures.properties.dkc_returns.archetypes.FixedDelayRules import FixedDelayRules
from retro_data_structures.properties.dkc_returns.archetypes.HurlHeightRules import HurlHeightRules
from retro_data_structures.properties.dkc_returns.archetypes.ModifyContactRuleData import ModifyContactRuleData
from retro_data_structures.properties.dkc_returns.archetypes.SkinSwapModifierData import SkinSwapModifierData
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct132 import UnknownStruct132
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct133 import UnknownStruct133
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct134 import UnknownStruct134
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct135 import UnknownStruct135
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class GenericCreatureDataJson(typing_extensions.TypedDict):
        movement_type: int
        contact_rules: int
        contact_rule_delay: float
        pass_collision_events_to_all_behaviors: bool
        disable_collision_on_death: bool
        backtrace_velocity_on_collision_check: bool
        initial_delay_is_handled_by_behaviors: bool
        initial_delay_min: float
        initial_delay_max: float
        movement_speed_modifier: float
        supress_movement_speed_messages: bool
        gravity: float
        snap_to_spline: bool
        snap_orientation_to_spline_on_creation: bool
        snap_orientation_to_spline_on_death: bool
        use_terrain_alignment: bool
        terrain_alignment_on_ground_rotation_speed: float
        terrain_alignment_off_ground_rotation_speed: float
        terrain_alignment_on_ground_root_speed: float
        terrain_alignment_off_ground_root_speed: float
        terrain_alignment_search_radius: float
        terrain_alignment_search_surface_up_offset: float
        terrain_alignment_flat_ground_disable_frames: int
        eligible_for_render_sorting: bool
        use_render_push: bool
        render_push_amount: float
        render_sort_priority: int
        render_texture_set: int
        always_faces_camera: bool
        uses_mirrored_anims: bool
        peanuts_pass_through: bool
        peanuts_burn_on_contact: bool
        moves_screen_left: bool
        generation_facing: int
        use_alternate_damage_effect: bool
        can_collide_with_mine_cart_track: bool
        can_collide_with_other_creatures: bool
        can_collide_with_invulnerable_player: bool
        ignored_by_triggers: bool
        damage_bounds_scale_z: float
        single_bop_particle_effect: int
        single_bop_particle_effect_uses_creature_orientation: bool
        is_rider: bool
        rider_vertical_offset: float
        interact_with_reactive_actor: bool
        use_creators_bounds: bool
        radial_damage_uses_contact_rules: bool
        modify_contact_rules: json_util.JsonObject
        despawn_rules: json_util.JsonObject
        fixed_delay_rules: json_util.JsonObject
        hurl_height_rules: json_util.JsonObject
        unknown_struct132: json_util.JsonObject
        collision_actors: json_util.JsonObject
        unknown_struct133: json_util.JsonObject
        anim_grid: json_util.JsonObject
        unknown_struct134: json_util.JsonObject
        unknown_struct135: json_util.JsonObject
        use_dash_modifier: bool
        dash_modifier: json_util.JsonObject
        use_orientation_modifier: bool
        use_skin_swap_modifier: bool
        skin_swap_modifier: json_util.JsonObject
    

@dataclasses.dataclass()
class GenericCreatureData(BaseProperty):
    movement_type: enums.MovementType = dataclasses.field(default=enums.MovementType.Unknown1, metadata={
        'reflection': FieldReflection[enums.MovementType](
            enums.MovementType, id=0x0b3e0a3a, original_name='MovementType', from_json=enums.MovementType.from_json, to_json=enums.MovementType.to_json
        ),
    })
    contact_rules: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['RULE'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x019ff362, original_name='ContactRules'
        ),
    })
    contact_rule_delay: float = dataclasses.field(default=0.10000000149011612, metadata={
        'reflection': FieldReflection[float](
            float, id=0x52ab1f08, original_name='ContactRuleDelay'
        ),
    })
    pass_collision_events_to_all_behaviors: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4b004257, original_name='PassCollisionEventsToAllBehaviors'
        ),
    })
    disable_collision_on_death: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x24e95d15, original_name='DisableCollisionOnDeath'
        ),
    })
    backtrace_velocity_on_collision_check: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x558147c0, original_name='BacktraceVelocityOnCollisionCheck'
        ),
    })
    initial_delay_is_handled_by_behaviors: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd342942f, original_name='InitialDelayIsHandledByBehaviors'
        ),
    })
    initial_delay_min: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x17dd78df, original_name='InitialDelayMin'
        ),
    })
    initial_delay_max: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf1bdd73e, original_name='InitialDelayMax'
        ),
    })
    movement_speed_modifier: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x374c17ba, original_name='MovementSpeedModifier'
        ),
    })
    supress_movement_speed_messages: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x490572f8, original_name='SupressMovementSpeedMessages'
        ),
    })
    gravity: float = dataclasses.field(default=55.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2f2ae3e5, original_name='Gravity'
        ),
    })
    snap_to_spline: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x26ecb939, original_name='SnapToSpline'
        ),
    })
    snap_orientation_to_spline_on_creation: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3c7de892, original_name='SnapOrientationToSplineOnCreation'
        ),
    })
    snap_orientation_to_spline_on_death: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbbfe7d9b, original_name='SnapOrientationToSplineOnDeath'
        ),
    })
    use_terrain_alignment: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6117e78f, original_name='UseTerrainAlignment'
        ),
    })
    terrain_alignment_on_ground_rotation_speed: float = dataclasses.field(default=60.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6a1af7f6, original_name='TerrainAlignmentOnGroundRotationSpeed'
        ),
    })
    terrain_alignment_off_ground_rotation_speed: float = dataclasses.field(default=720.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x689df179, original_name='TerrainAlignmentOffGroundRotationSpeed'
        ),
    })
    terrain_alignment_on_ground_root_speed: float = dataclasses.field(default=2.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x0d1aeaed, original_name='TerrainAlignmentOnGroundRootSpeed'
        ),
    })
    terrain_alignment_off_ground_root_speed: float = dataclasses.field(default=9.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x4be864fd, original_name='TerrainAlignmentOffGroundRootSpeed'
        ),
    })
    terrain_alignment_search_radius: float = dataclasses.field(default=1.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc2aeacd5, original_name='TerrainAlignmentSearchRadius'
        ),
    })
    terrain_alignment_search_surface_up_offset: float = dataclasses.field(default=0.75, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd90e7c5c, original_name='TerrainAlignmentSearchSurfaceUpOffset'
        ),
    })
    terrain_alignment_flat_ground_disable_frames: int = dataclasses.field(default=6, metadata={
        'reflection': FieldReflection[int](
            int, id=0x5ea8ac2b, original_name='TerrainAlignmentFlatGroundDisableFrames'
        ),
    })
    eligible_for_render_sorting: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x91ffefed, original_name='EligibleForRenderSorting'
        ),
    })
    use_render_push: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa9b55c55, original_name='UseRenderPush'
        ),
    })
    render_push_amount: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf496803d, original_name='RenderPushAmount'
        ),
    })
    render_sort_priority: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x43920481, original_name='RenderSortPriority'
        ),
    })
    render_texture_set: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x32fab97e, original_name='RenderTextureSet'
        ),
    })
    always_faces_camera: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x47649c1b, original_name='AlwaysFacesCamera'
        ),
    })
    uses_mirrored_anims: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe041bee6, original_name='UsesMirroredAnims'
        ),
    })
    peanuts_pass_through: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc339fbb5, original_name='PeanutsPassThrough'
        ),
    })
    peanuts_burn_on_contact: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbc1a9077, original_name='PeanutsBurnOnContact'
        ),
    })
    moves_screen_left: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7a91a063, original_name='MovesScreenLeft'
        ),
    })
    generation_facing: enums.GenerationFacing = dataclasses.field(default=enums.GenerationFacing.Unknown2, metadata={
        'reflection': FieldReflection[enums.GenerationFacing](
            enums.GenerationFacing, id=0x271f46a0, original_name='GenerationFacing', from_json=enums.GenerationFacing.from_json, to_json=enums.GenerationFacing.to_json
        ),
    })
    use_alternate_damage_effect: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf0993bfe, original_name='UseAlternateDamageEffect'
        ),
    })
    can_collide_with_mine_cart_track: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa2671d83, original_name='CanCollideWithMineCartTrack'
        ),
    })
    can_collide_with_other_creatures: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x936b2c8a, original_name='CanCollideWithOtherCreatures'
        ),
    })
    can_collide_with_invulnerable_player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xfeff7d43, original_name='CanCollideWithInvulnerablePlayer'
        ),
    })
    ignored_by_triggers: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x756d7cc9, original_name='IgnoredByTriggers'
        ),
    })
    damage_bounds_scale_z: float = dataclasses.field(default=0.5, metadata={
        'reflection': FieldReflection[float](
            float, id=0xc336a4ef, original_name='DamageBoundsScaleZ'
        ),
    })
    single_bop_particle_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x89cf2281, original_name='SingleBopParticleEffect'
        ),
    })
    single_bop_particle_effect_uses_creature_orientation: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xee727579, original_name='SingleBopParticleEffectUsesCreatureOrientation'
        ),
    })
    is_rider: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x671429bc, original_name='IsRider'
        ),
    })
    rider_vertical_offset: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x26c15c60, original_name='RiderVerticalOffset'
        ),
    })
    interact_with_reactive_actor: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3ee78313, original_name='InteractWithReactiveActor'
        ),
    })
    use_creators_bounds: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xeb61c9c1, original_name='UseCreatorsBounds'
        ),
    })
    radial_damage_uses_contact_rules: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x1bf83306, original_name='RadialDamageUsesContactRules'
        ),
    })
    modify_contact_rules: ModifyContactRuleData = dataclasses.field(default_factory=ModifyContactRuleData, metadata={
        'reflection': FieldReflection[ModifyContactRuleData](
            ModifyContactRuleData, id=0x6b32e09e, original_name='ModifyContactRules', from_json=ModifyContactRuleData.from_json, to_json=ModifyContactRuleData.to_json
        ),
    })
    despawn_rules: DespawnRules = dataclasses.field(default_factory=DespawnRules, metadata={
        'reflection': FieldReflection[DespawnRules](
            DespawnRules, id=0xb6af2d99, original_name='DespawnRules', from_json=DespawnRules.from_json, to_json=DespawnRules.to_json
        ),
    })
    fixed_delay_rules: FixedDelayRules = dataclasses.field(default_factory=FixedDelayRules, metadata={
        'reflection': FieldReflection[FixedDelayRules](
            FixedDelayRules, id=0xae27f052, original_name='FixedDelayRules', from_json=FixedDelayRules.from_json, to_json=FixedDelayRules.to_json
        ),
    })
    hurl_height_rules: HurlHeightRules = dataclasses.field(default_factory=HurlHeightRules, metadata={
        'reflection': FieldReflection[HurlHeightRules](
            HurlHeightRules, id=0x5400b556, original_name='HurlHeightRules', from_json=HurlHeightRules.from_json, to_json=HurlHeightRules.to_json
        ),
    })
    unknown_struct132: UnknownStruct132 = dataclasses.field(default_factory=UnknownStruct132, metadata={
        'reflection': FieldReflection[UnknownStruct132](
            UnknownStruct132, id=0x24f41dcb, original_name='UnknownStruct132', from_json=UnknownStruct132.from_json, to_json=UnknownStruct132.to_json
        ),
    })
    collision_actors: CollisionActorModifierData = dataclasses.field(default_factory=CollisionActorModifierData, metadata={
        'reflection': FieldReflection[CollisionActorModifierData](
            CollisionActorModifierData, id=0x55c89b60, original_name='CollisionActors', from_json=CollisionActorModifierData.from_json, to_json=CollisionActorModifierData.to_json
        ),
    })
    unknown_struct133: UnknownStruct133 = dataclasses.field(default_factory=UnknownStruct133, metadata={
        'reflection': FieldReflection[UnknownStruct133](
            UnknownStruct133, id=0x1a5ba8da, original_name='UnknownStruct133', from_json=UnknownStruct133.from_json, to_json=UnknownStruct133.to_json
        ),
    })
    anim_grid: AnimGridModifierData = dataclasses.field(default_factory=AnimGridModifierData, metadata={
        'reflection': FieldReflection[AnimGridModifierData](
            AnimGridModifierData, id=0x68fd49ae, original_name='AnimGrid', from_json=AnimGridModifierData.from_json, to_json=AnimGridModifierData.to_json
        ),
    })
    unknown_struct134: UnknownStruct134 = dataclasses.field(default_factory=UnknownStruct134, metadata={
        'reflection': FieldReflection[UnknownStruct134](
            UnknownStruct134, id=0x5d8916ea, original_name='UnknownStruct134', from_json=UnknownStruct134.from_json, to_json=UnknownStruct134.to_json
        ),
    })
    unknown_struct135: UnknownStruct135 = dataclasses.field(default_factory=UnknownStruct135, metadata={
        'reflection': FieldReflection[UnknownStruct135](
            UnknownStruct135, id=0xe22fbdc4, original_name='UnknownStruct135', from_json=UnknownStruct135.from_json, to_json=UnknownStruct135.to_json
        ),
    })
    use_dash_modifier: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc08e06ac, original_name='UseDashModifier'
        ),
    })
    dash_modifier: DashModifierData = dataclasses.field(default_factory=DashModifierData, metadata={
        'reflection': FieldReflection[DashModifierData](
            DashModifierData, id=0x2e42a623, original_name='DashModifier', from_json=DashModifierData.from_json, to_json=DashModifierData.to_json
        ),
    })
    use_orientation_modifier: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf4acf493, original_name='UseOrientationModifier'
        ),
    })
    use_skin_swap_modifier: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x8dfb1669, original_name='UseSkinSwapModifier'
        ),
    })
    skin_swap_modifier: SkinSwapModifierData = dataclasses.field(default_factory=SkinSwapModifierData, metadata={
        'reflection': FieldReflection[SkinSwapModifierData](
            SkinSwapModifierData, id=0xb0ced792, original_name='SkinSwapModifier', from_json=SkinSwapModifierData.from_json, to_json=SkinSwapModifierData.to_json
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
        if property_count != 62:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0b3e0a3a
        movement_type = enums.MovementType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x019ff362
        contact_rules = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x52ab1f08
        contact_rule_delay = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4b004257
        pass_collision_events_to_all_behaviors = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x24e95d15
        disable_collision_on_death = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x558147c0
        backtrace_velocity_on_collision_check = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd342942f
        initial_delay_is_handled_by_behaviors = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x17dd78df
        initial_delay_min = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf1bdd73e
        initial_delay_max = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x374c17ba
        movement_speed_modifier = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x490572f8
        supress_movement_speed_messages = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2f2ae3e5
        gravity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26ecb939
        snap_to_spline = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3c7de892
        snap_orientation_to_spline_on_creation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbbfe7d9b
        snap_orientation_to_spline_on_death = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6117e78f
        use_terrain_alignment = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a1af7f6
        terrain_alignment_on_ground_rotation_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x689df179
        terrain_alignment_off_ground_rotation_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x0d1aeaed
        terrain_alignment_on_ground_root_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4be864fd
        terrain_alignment_off_ground_root_speed = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc2aeacd5
        terrain_alignment_search_radius = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd90e7c5c
        terrain_alignment_search_surface_up_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5ea8ac2b
        terrain_alignment_flat_ground_disable_frames = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x91ffefed
        eligible_for_render_sorting = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa9b55c55
        use_render_push = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf496803d
        render_push_amount = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x43920481
        render_sort_priority = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x32fab97e
        render_texture_set = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x47649c1b
        always_faces_camera = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe041bee6
        uses_mirrored_anims = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc339fbb5
        peanuts_pass_through = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xbc1a9077
        peanuts_burn_on_contact = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7a91a063
        moves_screen_left = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x271f46a0
        generation_facing = enums.GenerationFacing.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0993bfe
        use_alternate_damage_effect = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xa2671d83
        can_collide_with_mine_cart_track = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x936b2c8a
        can_collide_with_other_creatures = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfeff7d43
        can_collide_with_invulnerable_player = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x756d7cc9
        ignored_by_triggers = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc336a4ef
        damage_bounds_scale_z = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x89cf2281
        single_bop_particle_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xee727579
        single_bop_particle_effect_uses_creature_orientation = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x671429bc
        is_rider = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x26c15c60
        rider_vertical_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3ee78313
        interact_with_reactive_actor = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xeb61c9c1
        use_creators_bounds = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1bf83306
        radial_damage_uses_contact_rules = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b32e09e
        modify_contact_rules = ModifyContactRuleData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb6af2d99
        despawn_rules = DespawnRules.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xae27f052
        fixed_delay_rules = FixedDelayRules.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5400b556
        hurl_height_rules = HurlHeightRules.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x24f41dcb
        unknown_struct132 = UnknownStruct132.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x55c89b60
        collision_actors = CollisionActorModifierData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1a5ba8da
        unknown_struct133 = UnknownStruct133.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x68fd49ae
        anim_grid = AnimGridModifierData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5d8916ea
        unknown_struct134 = UnknownStruct134.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe22fbdc4
        unknown_struct135 = UnknownStruct135.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc08e06ac
        use_dash_modifier = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2e42a623
        dash_modifier = DashModifierData.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf4acf493
        use_orientation_modifier = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8dfb1669
        use_skin_swap_modifier = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb0ced792
        skin_swap_modifier = SkinSwapModifierData.from_stream(data, property_size)
    
        return cls(movement_type, contact_rules, contact_rule_delay, pass_collision_events_to_all_behaviors, disable_collision_on_death, backtrace_velocity_on_collision_check, initial_delay_is_handled_by_behaviors, initial_delay_min, initial_delay_max, movement_speed_modifier, supress_movement_speed_messages, gravity, snap_to_spline, snap_orientation_to_spline_on_creation, snap_orientation_to_spline_on_death, use_terrain_alignment, terrain_alignment_on_ground_rotation_speed, terrain_alignment_off_ground_rotation_speed, terrain_alignment_on_ground_root_speed, terrain_alignment_off_ground_root_speed, terrain_alignment_search_radius, terrain_alignment_search_surface_up_offset, terrain_alignment_flat_ground_disable_frames, eligible_for_render_sorting, use_render_push, render_push_amount, render_sort_priority, render_texture_set, always_faces_camera, uses_mirrored_anims, peanuts_pass_through, peanuts_burn_on_contact, moves_screen_left, generation_facing, use_alternate_damage_effect, can_collide_with_mine_cart_track, can_collide_with_other_creatures, can_collide_with_invulnerable_player, ignored_by_triggers, damage_bounds_scale_z, single_bop_particle_effect, single_bop_particle_effect_uses_creature_orientation, is_rider, rider_vertical_offset, interact_with_reactive_actor, use_creators_bounds, radial_damage_uses_contact_rules, modify_contact_rules, despawn_rules, fixed_delay_rules, hurl_height_rules, unknown_struct132, collision_actors, unknown_struct133, anim_grid, unknown_struct134, unknown_struct135, use_dash_modifier, dash_modifier, use_orientation_modifier, use_skin_swap_modifier, skin_swap_modifier)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00>')  # 62 properties

        data.write(b'\x0b>\n:')  # 0xb3e0a3a
        data.write(b'\x00\x04')  # size
        self.movement_type.to_stream(data)

        data.write(b'\x01\x9f\xf3b')  # 0x19ff362
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.contact_rules))

        data.write(b'R\xab\x1f\x08')  # 0x52ab1f08
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.contact_rule_delay))

        data.write(b'K\x00BW')  # 0x4b004257
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.pass_collision_events_to_all_behaviors))

        data.write(b'$\xe9]\x15')  # 0x24e95d15
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.disable_collision_on_death))

        data.write(b'U\x81G\xc0')  # 0x558147c0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.backtrace_velocity_on_collision_check))

        data.write(b'\xd3B\x94/')  # 0xd342942f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.initial_delay_is_handled_by_behaviors))

        data.write(b'\x17\xddx\xdf')  # 0x17dd78df
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_delay_min))

        data.write(b'\xf1\xbd\xd7>')  # 0xf1bdd73e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_delay_max))

        data.write(b'7L\x17\xba')  # 0x374c17ba
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.movement_speed_modifier))

        data.write(b'I\x05r\xf8')  # 0x490572f8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.supress_movement_speed_messages))

        data.write(b'/*\xe3\xe5')  # 0x2f2ae3e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.gravity))

        data.write(b'&\xec\xb99')  # 0x26ecb939
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_to_spline))

        data.write(b'<}\xe8\x92')  # 0x3c7de892
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_orientation_to_spline_on_creation))

        data.write(b'\xbb\xfe}\x9b')  # 0xbbfe7d9b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.snap_orientation_to_spline_on_death))

        data.write(b'a\x17\xe7\x8f')  # 0x6117e78f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_terrain_alignment))

        data.write(b'j\x1a\xf7\xf6')  # 0x6a1af7f6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_on_ground_rotation_speed))

        data.write(b'h\x9d\xf1y')  # 0x689df179
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_off_ground_rotation_speed))

        data.write(b'\r\x1a\xea\xed')  # 0xd1aeaed
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_on_ground_root_speed))

        data.write(b'K\xe8d\xfd')  # 0x4be864fd
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_off_ground_root_speed))

        data.write(b'\xc2\xae\xac\xd5')  # 0xc2aeacd5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_search_radius))

        data.write(b'\xd9\x0e|\\')  # 0xd90e7c5c
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.terrain_alignment_search_surface_up_offset))

        data.write(b'^\xa8\xac+')  # 0x5ea8ac2b
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.terrain_alignment_flat_ground_disable_frames))

        data.write(b'\x91\xff\xef\xed')  # 0x91ffefed
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.eligible_for_render_sorting))

        data.write(b'\xa9\xb5\\U')  # 0xa9b55c55
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_render_push))

        data.write(b'\xf4\x96\x80=')  # 0xf496803d
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.render_push_amount))

        data.write(b'C\x92\x04\x81')  # 0x43920481
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.render_sort_priority))

        data.write(b'2\xfa\xb9~')  # 0x32fab97e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.render_texture_set))

        data.write(b'Gd\x9c\x1b')  # 0x47649c1b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.always_faces_camera))

        data.write(b'\xe0A\xbe\xe6')  # 0xe041bee6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.uses_mirrored_anims))

        data.write(b'\xc39\xfb\xb5')  # 0xc339fbb5
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.peanuts_pass_through))

        data.write(b'\xbc\x1a\x90w')  # 0xbc1a9077
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.peanuts_burn_on_contact))

        data.write(b'z\x91\xa0c')  # 0x7a91a063
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.moves_screen_left))

        data.write(b"'\x1fF\xa0")  # 0x271f46a0
        data.write(b'\x00\x04')  # size
        self.generation_facing.to_stream(data)

        data.write(b'\xf0\x99;\xfe')  # 0xf0993bfe
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_alternate_damage_effect))

        data.write(b'\xa2g\x1d\x83')  # 0xa2671d83
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_collide_with_mine_cart_track))

        data.write(b'\x93k,\x8a')  # 0x936b2c8a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_collide_with_other_creatures))

        data.write(b'\xfe\xff}C')  # 0xfeff7d43
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_collide_with_invulnerable_player))

        data.write(b'um|\xc9')  # 0x756d7cc9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignored_by_triggers))

        data.write(b'\xc36\xa4\xef')  # 0xc336a4ef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.damage_bounds_scale_z))

        data.write(b'\x89\xcf"\x81')  # 0x89cf2281
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.single_bop_particle_effect))

        data.write(b'\xeeruy')  # 0xee727579
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.single_bop_particle_effect_uses_creature_orientation))

        data.write(b'g\x14)\xbc')  # 0x671429bc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.is_rider))

        data.write(b'&\xc1\\`')  # 0x26c15c60
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.rider_vertical_offset))

        data.write(b'>\xe7\x83\x13')  # 0x3ee78313
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.interact_with_reactive_actor))

        data.write(b'\xeba\xc9\xc1')  # 0xeb61c9c1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_creators_bounds))

        data.write(b'\x1b\xf83\x06')  # 0x1bf83306
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.radial_damage_uses_contact_rules))

        data.write(b'k2\xe0\x9e')  # 0x6b32e09e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.modify_contact_rules.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xb6\xaf-\x99')  # 0xb6af2d99
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.despawn_rules.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b"\xae'\xf0R")  # 0xae27f052
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.fixed_delay_rules.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'T\x00\xb5V')  # 0x5400b556
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.hurl_height_rules.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'$\xf4\x1d\xcb')  # 0x24f41dcb
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct132.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'U\xc8\x9b`')  # 0x55c89b60
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.collision_actors.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x1a[\xa8\xda')  # 0x1a5ba8da
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct133.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'h\xfdI\xae')  # 0x68fd49ae
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.anim_grid.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b']\x89\x16\xea')  # 0x5d8916ea
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct134.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe2/\xbd\xc4')  # 0xe22fbdc4
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct135.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xc0\x8e\x06\xac')  # 0xc08e06ac
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_dash_modifier))

        data.write(b'.B\xa6#')  # 0x2e42a623
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.dash_modifier.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf4\xac\xf4\x93')  # 0xf4acf493
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_orientation_modifier))

        data.write(b'\x8d\xfb\x16i')  # 0x8dfb1669
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_skin_swap_modifier))

        data.write(b'\xb0\xce\xd7\x92')  # 0xb0ced792
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.skin_swap_modifier.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("GenericCreatureDataJson", data)
        return cls(
            movement_type=enums.MovementType.from_json(json_data['movement_type']),
            contact_rules=json_data['contact_rules'],
            contact_rule_delay=json_data['contact_rule_delay'],
            pass_collision_events_to_all_behaviors=json_data['pass_collision_events_to_all_behaviors'],
            disable_collision_on_death=json_data['disable_collision_on_death'],
            backtrace_velocity_on_collision_check=json_data['backtrace_velocity_on_collision_check'],
            initial_delay_is_handled_by_behaviors=json_data['initial_delay_is_handled_by_behaviors'],
            initial_delay_min=json_data['initial_delay_min'],
            initial_delay_max=json_data['initial_delay_max'],
            movement_speed_modifier=json_data['movement_speed_modifier'],
            supress_movement_speed_messages=json_data['supress_movement_speed_messages'],
            gravity=json_data['gravity'],
            snap_to_spline=json_data['snap_to_spline'],
            snap_orientation_to_spline_on_creation=json_data['snap_orientation_to_spline_on_creation'],
            snap_orientation_to_spline_on_death=json_data['snap_orientation_to_spline_on_death'],
            use_terrain_alignment=json_data['use_terrain_alignment'],
            terrain_alignment_on_ground_rotation_speed=json_data['terrain_alignment_on_ground_rotation_speed'],
            terrain_alignment_off_ground_rotation_speed=json_data['terrain_alignment_off_ground_rotation_speed'],
            terrain_alignment_on_ground_root_speed=json_data['terrain_alignment_on_ground_root_speed'],
            terrain_alignment_off_ground_root_speed=json_data['terrain_alignment_off_ground_root_speed'],
            terrain_alignment_search_radius=json_data['terrain_alignment_search_radius'],
            terrain_alignment_search_surface_up_offset=json_data['terrain_alignment_search_surface_up_offset'],
            terrain_alignment_flat_ground_disable_frames=json_data['terrain_alignment_flat_ground_disable_frames'],
            eligible_for_render_sorting=json_data['eligible_for_render_sorting'],
            use_render_push=json_data['use_render_push'],
            render_push_amount=json_data['render_push_amount'],
            render_sort_priority=json_data['render_sort_priority'],
            render_texture_set=json_data['render_texture_set'],
            always_faces_camera=json_data['always_faces_camera'],
            uses_mirrored_anims=json_data['uses_mirrored_anims'],
            peanuts_pass_through=json_data['peanuts_pass_through'],
            peanuts_burn_on_contact=json_data['peanuts_burn_on_contact'],
            moves_screen_left=json_data['moves_screen_left'],
            generation_facing=enums.GenerationFacing.from_json(json_data['generation_facing']),
            use_alternate_damage_effect=json_data['use_alternate_damage_effect'],
            can_collide_with_mine_cart_track=json_data['can_collide_with_mine_cart_track'],
            can_collide_with_other_creatures=json_data['can_collide_with_other_creatures'],
            can_collide_with_invulnerable_player=json_data['can_collide_with_invulnerable_player'],
            ignored_by_triggers=json_data['ignored_by_triggers'],
            damage_bounds_scale_z=json_data['damage_bounds_scale_z'],
            single_bop_particle_effect=json_data['single_bop_particle_effect'],
            single_bop_particle_effect_uses_creature_orientation=json_data['single_bop_particle_effect_uses_creature_orientation'],
            is_rider=json_data['is_rider'],
            rider_vertical_offset=json_data['rider_vertical_offset'],
            interact_with_reactive_actor=json_data['interact_with_reactive_actor'],
            use_creators_bounds=json_data['use_creators_bounds'],
            radial_damage_uses_contact_rules=json_data['radial_damage_uses_contact_rules'],
            modify_contact_rules=ModifyContactRuleData.from_json(json_data['modify_contact_rules']),
            despawn_rules=DespawnRules.from_json(json_data['despawn_rules']),
            fixed_delay_rules=FixedDelayRules.from_json(json_data['fixed_delay_rules']),
            hurl_height_rules=HurlHeightRules.from_json(json_data['hurl_height_rules']),
            unknown_struct132=UnknownStruct132.from_json(json_data['unknown_struct132']),
            collision_actors=CollisionActorModifierData.from_json(json_data['collision_actors']),
            unknown_struct133=UnknownStruct133.from_json(json_data['unknown_struct133']),
            anim_grid=AnimGridModifierData.from_json(json_data['anim_grid']),
            unknown_struct134=UnknownStruct134.from_json(json_data['unknown_struct134']),
            unknown_struct135=UnknownStruct135.from_json(json_data['unknown_struct135']),
            use_dash_modifier=json_data['use_dash_modifier'],
            dash_modifier=DashModifierData.from_json(json_data['dash_modifier']),
            use_orientation_modifier=json_data['use_orientation_modifier'],
            use_skin_swap_modifier=json_data['use_skin_swap_modifier'],
            skin_swap_modifier=SkinSwapModifierData.from_json(json_data['skin_swap_modifier']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'movement_type': self.movement_type.to_json(),
            'contact_rules': self.contact_rules,
            'contact_rule_delay': self.contact_rule_delay,
            'pass_collision_events_to_all_behaviors': self.pass_collision_events_to_all_behaviors,
            'disable_collision_on_death': self.disable_collision_on_death,
            'backtrace_velocity_on_collision_check': self.backtrace_velocity_on_collision_check,
            'initial_delay_is_handled_by_behaviors': self.initial_delay_is_handled_by_behaviors,
            'initial_delay_min': self.initial_delay_min,
            'initial_delay_max': self.initial_delay_max,
            'movement_speed_modifier': self.movement_speed_modifier,
            'supress_movement_speed_messages': self.supress_movement_speed_messages,
            'gravity': self.gravity,
            'snap_to_spline': self.snap_to_spline,
            'snap_orientation_to_spline_on_creation': self.snap_orientation_to_spline_on_creation,
            'snap_orientation_to_spline_on_death': self.snap_orientation_to_spline_on_death,
            'use_terrain_alignment': self.use_terrain_alignment,
            'terrain_alignment_on_ground_rotation_speed': self.terrain_alignment_on_ground_rotation_speed,
            'terrain_alignment_off_ground_rotation_speed': self.terrain_alignment_off_ground_rotation_speed,
            'terrain_alignment_on_ground_root_speed': self.terrain_alignment_on_ground_root_speed,
            'terrain_alignment_off_ground_root_speed': self.terrain_alignment_off_ground_root_speed,
            'terrain_alignment_search_radius': self.terrain_alignment_search_radius,
            'terrain_alignment_search_surface_up_offset': self.terrain_alignment_search_surface_up_offset,
            'terrain_alignment_flat_ground_disable_frames': self.terrain_alignment_flat_ground_disable_frames,
            'eligible_for_render_sorting': self.eligible_for_render_sorting,
            'use_render_push': self.use_render_push,
            'render_push_amount': self.render_push_amount,
            'render_sort_priority': self.render_sort_priority,
            'render_texture_set': self.render_texture_set,
            'always_faces_camera': self.always_faces_camera,
            'uses_mirrored_anims': self.uses_mirrored_anims,
            'peanuts_pass_through': self.peanuts_pass_through,
            'peanuts_burn_on_contact': self.peanuts_burn_on_contact,
            'moves_screen_left': self.moves_screen_left,
            'generation_facing': self.generation_facing.to_json(),
            'use_alternate_damage_effect': self.use_alternate_damage_effect,
            'can_collide_with_mine_cart_track': self.can_collide_with_mine_cart_track,
            'can_collide_with_other_creatures': self.can_collide_with_other_creatures,
            'can_collide_with_invulnerable_player': self.can_collide_with_invulnerable_player,
            'ignored_by_triggers': self.ignored_by_triggers,
            'damage_bounds_scale_z': self.damage_bounds_scale_z,
            'single_bop_particle_effect': self.single_bop_particle_effect,
            'single_bop_particle_effect_uses_creature_orientation': self.single_bop_particle_effect_uses_creature_orientation,
            'is_rider': self.is_rider,
            'rider_vertical_offset': self.rider_vertical_offset,
            'interact_with_reactive_actor': self.interact_with_reactive_actor,
            'use_creators_bounds': self.use_creators_bounds,
            'radial_damage_uses_contact_rules': self.radial_damage_uses_contact_rules,
            'modify_contact_rules': self.modify_contact_rules.to_json(),
            'despawn_rules': self.despawn_rules.to_json(),
            'fixed_delay_rules': self.fixed_delay_rules.to_json(),
            'hurl_height_rules': self.hurl_height_rules.to_json(),
            'unknown_struct132': self.unknown_struct132.to_json(),
            'collision_actors': self.collision_actors.to_json(),
            'unknown_struct133': self.unknown_struct133.to_json(),
            'anim_grid': self.anim_grid.to_json(),
            'unknown_struct134': self.unknown_struct134.to_json(),
            'unknown_struct135': self.unknown_struct135.to_json(),
            'use_dash_modifier': self.use_dash_modifier,
            'dash_modifier': self.dash_modifier.to_json(),
            'use_orientation_modifier': self.use_orientation_modifier,
            'use_skin_swap_modifier': self.use_skin_swap_modifier,
            'skin_swap_modifier': self.skin_swap_modifier.to_json(),
        }


def _decode_movement_type(data: typing.BinaryIO, property_size: int):
    return enums.MovementType.from_stream(data)


def _decode_contact_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_contact_rule_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_pass_collision_events_to_all_behaviors(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_disable_collision_on_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_backtrace_velocity_on_collision_check(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initial_delay_is_handled_by_behaviors(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_initial_delay_min(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_delay_max(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_movement_speed_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_supress_movement_speed_messages(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_gravity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_snap_to_spline(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_snap_orientation_to_spline_on_creation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_snap_orientation_to_spline_on_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_terrain_alignment(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_terrain_alignment_on_ground_rotation_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_off_ground_rotation_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_on_ground_root_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_off_ground_root_speed(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_search_radius(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_search_surface_up_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_terrain_alignment_flat_ground_disable_frames(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_eligible_for_render_sorting(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_render_push(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_render_push_amount(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_render_sort_priority(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_render_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_always_faces_camera(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_uses_mirrored_anims(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_peanuts_pass_through(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_peanuts_burn_on_contact(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_moves_screen_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_generation_facing(data: typing.BinaryIO, property_size: int):
    return enums.GenerationFacing.from_stream(data)


def _decode_use_alternate_damage_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_collide_with_mine_cart_track(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_collide_with_other_creatures(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_can_collide_with_invulnerable_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_ignored_by_triggers(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_damage_bounds_scale_z(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_single_bop_particle_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_single_bop_particle_effect_uses_creature_orientation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_is_rider(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_rider_vertical_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_interact_with_reactive_actor(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_creators_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_radial_damage_uses_contact_rules(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_dash_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_orientation_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_skin_swap_modifier(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb3e0a3a: ('movement_type', _decode_movement_type),
    0x19ff362: ('contact_rules', _decode_contact_rules),
    0x52ab1f08: ('contact_rule_delay', _decode_contact_rule_delay),
    0x4b004257: ('pass_collision_events_to_all_behaviors', _decode_pass_collision_events_to_all_behaviors),
    0x24e95d15: ('disable_collision_on_death', _decode_disable_collision_on_death),
    0x558147c0: ('backtrace_velocity_on_collision_check', _decode_backtrace_velocity_on_collision_check),
    0xd342942f: ('initial_delay_is_handled_by_behaviors', _decode_initial_delay_is_handled_by_behaviors),
    0x17dd78df: ('initial_delay_min', _decode_initial_delay_min),
    0xf1bdd73e: ('initial_delay_max', _decode_initial_delay_max),
    0x374c17ba: ('movement_speed_modifier', _decode_movement_speed_modifier),
    0x490572f8: ('supress_movement_speed_messages', _decode_supress_movement_speed_messages),
    0x2f2ae3e5: ('gravity', _decode_gravity),
    0x26ecb939: ('snap_to_spline', _decode_snap_to_spline),
    0x3c7de892: ('snap_orientation_to_spline_on_creation', _decode_snap_orientation_to_spline_on_creation),
    0xbbfe7d9b: ('snap_orientation_to_spline_on_death', _decode_snap_orientation_to_spline_on_death),
    0x6117e78f: ('use_terrain_alignment', _decode_use_terrain_alignment),
    0x6a1af7f6: ('terrain_alignment_on_ground_rotation_speed', _decode_terrain_alignment_on_ground_rotation_speed),
    0x689df179: ('terrain_alignment_off_ground_rotation_speed', _decode_terrain_alignment_off_ground_rotation_speed),
    0xd1aeaed: ('terrain_alignment_on_ground_root_speed', _decode_terrain_alignment_on_ground_root_speed),
    0x4be864fd: ('terrain_alignment_off_ground_root_speed', _decode_terrain_alignment_off_ground_root_speed),
    0xc2aeacd5: ('terrain_alignment_search_radius', _decode_terrain_alignment_search_radius),
    0xd90e7c5c: ('terrain_alignment_search_surface_up_offset', _decode_terrain_alignment_search_surface_up_offset),
    0x5ea8ac2b: ('terrain_alignment_flat_ground_disable_frames', _decode_terrain_alignment_flat_ground_disable_frames),
    0x91ffefed: ('eligible_for_render_sorting', _decode_eligible_for_render_sorting),
    0xa9b55c55: ('use_render_push', _decode_use_render_push),
    0xf496803d: ('render_push_amount', _decode_render_push_amount),
    0x43920481: ('render_sort_priority', _decode_render_sort_priority),
    0x32fab97e: ('render_texture_set', _decode_render_texture_set),
    0x47649c1b: ('always_faces_camera', _decode_always_faces_camera),
    0xe041bee6: ('uses_mirrored_anims', _decode_uses_mirrored_anims),
    0xc339fbb5: ('peanuts_pass_through', _decode_peanuts_pass_through),
    0xbc1a9077: ('peanuts_burn_on_contact', _decode_peanuts_burn_on_contact),
    0x7a91a063: ('moves_screen_left', _decode_moves_screen_left),
    0x271f46a0: ('generation_facing', _decode_generation_facing),
    0xf0993bfe: ('use_alternate_damage_effect', _decode_use_alternate_damage_effect),
    0xa2671d83: ('can_collide_with_mine_cart_track', _decode_can_collide_with_mine_cart_track),
    0x936b2c8a: ('can_collide_with_other_creatures', _decode_can_collide_with_other_creatures),
    0xfeff7d43: ('can_collide_with_invulnerable_player', _decode_can_collide_with_invulnerable_player),
    0x756d7cc9: ('ignored_by_triggers', _decode_ignored_by_triggers),
    0xc336a4ef: ('damage_bounds_scale_z', _decode_damage_bounds_scale_z),
    0x89cf2281: ('single_bop_particle_effect', _decode_single_bop_particle_effect),
    0xee727579: ('single_bop_particle_effect_uses_creature_orientation', _decode_single_bop_particle_effect_uses_creature_orientation),
    0x671429bc: ('is_rider', _decode_is_rider),
    0x26c15c60: ('rider_vertical_offset', _decode_rider_vertical_offset),
    0x3ee78313: ('interact_with_reactive_actor', _decode_interact_with_reactive_actor),
    0xeb61c9c1: ('use_creators_bounds', _decode_use_creators_bounds),
    0x1bf83306: ('radial_damage_uses_contact_rules', _decode_radial_damage_uses_contact_rules),
    0x6b32e09e: ('modify_contact_rules', ModifyContactRuleData.from_stream),
    0xb6af2d99: ('despawn_rules', DespawnRules.from_stream),
    0xae27f052: ('fixed_delay_rules', FixedDelayRules.from_stream),
    0x5400b556: ('hurl_height_rules', HurlHeightRules.from_stream),
    0x24f41dcb: ('unknown_struct132', UnknownStruct132.from_stream),
    0x55c89b60: ('collision_actors', CollisionActorModifierData.from_stream),
    0x1a5ba8da: ('unknown_struct133', UnknownStruct133.from_stream),
    0x68fd49ae: ('anim_grid', AnimGridModifierData.from_stream),
    0x5d8916ea: ('unknown_struct134', UnknownStruct134.from_stream),
    0xe22fbdc4: ('unknown_struct135', UnknownStruct135.from_stream),
    0xc08e06ac: ('use_dash_modifier', _decode_use_dash_modifier),
    0x2e42a623: ('dash_modifier', DashModifierData.from_stream),
    0xf4acf493: ('use_orientation_modifier', _decode_use_orientation_modifier),
    0x8dfb1669: ('use_skin_swap_modifier', _decode_use_skin_swap_modifier),
    0xb0ced792: ('skin_swap_modifier', SkinSwapModifierData.from_stream),
}
