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
from retro_data_structures.properties.dkc_returns.core.AnimationParameters import AnimationParameters
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id
from retro_data_structures.properties.dkc_returns.core.Vector import Vector

if typing.TYPE_CHECKING:
    class BalloonDataJson(typing_extensions.TypedDict):
        balloon_character: json_util.JsonObject
        texture_set: int
        mass: float
        downward_velocity: float
        extra_downward_collision: float
        dk_riding_offset: json_util.JsonValue
        start_offset: float
        drop_height_above_spawn_point: float
        dk_pop_effect: int
        d_kand_diddy_pop_effect: int
        dk_pop_sound: int
        d_kand_diddy_pop_sound: int
        balloonless_mode_drop_timer: float
    

@dataclasses.dataclass()
class BalloonData(BaseProperty):
    balloon_character: AnimationParameters = dataclasses.field(default_factory=AnimationParameters, metadata={
        'reflection': FieldReflection[AnimationParameters](
            AnimationParameters, id=0xf8b3abe0, original_name='BalloonCharacter', from_json=AnimationParameters.from_json, to_json=AnimationParameters.to_json
        ),
    })
    texture_set: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0x6b40acef, original_name='TextureSet'
        ),
    })
    mass: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x75dbb375, original_name='Mass'
        ),
    })
    downward_velocity: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xddb16979, original_name='DownwardVelocity'
        ),
    })
    extra_downward_collision: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9a27ddc3, original_name='ExtraDownwardCollision'
        ),
    })
    dk_riding_offset: Vector = dataclasses.field(default_factory=lambda: Vector(x=0.0, y=0.0, z=-4.0), metadata={
        'reflection': FieldReflection[Vector](
            Vector, id=0xc0fe10c6, original_name='DKRidingOffset', from_json=Vector.from_json, to_json=Vector.to_json
        ),
    })
    start_offset: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x409618b6, original_name='StartOffset'
        ),
    })
    drop_height_above_spawn_point: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x806178b3, original_name='DropHeightAboveSpawnPoint'
        ),
    })
    dk_pop_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf532b5d3, original_name='DKPopEffect'
        ),
    })
    d_kand_diddy_pop_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xcaa9b3f5, original_name='DKandDiddyPopEffect'
        ),
    })
    dk_pop_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x726c839e, original_name='DKPopSound'
        ),
    })
    d_kand_diddy_pop_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5c6c7838, original_name='DKandDiddyPopSound'
        ),
    })
    balloonless_mode_drop_timer: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8069fba6, original_name='BalloonlessModeDropTimer'
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
        if property_count != 13:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf8b3abe0
        balloon_character = AnimationParameters.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6b40acef
        texture_set = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x75dbb375
        mass = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xddb16979
        downward_velocity = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9a27ddc3
        extra_downward_collision = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xc0fe10c6
        dk_riding_offset = Vector.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x409618b6
        start_offset = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806178b3
        drop_height_above_spawn_point = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf532b5d3
        dk_pop_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcaa9b3f5
        d_kand_diddy_pop_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x726c839e
        dk_pop_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5c6c7838
        d_kand_diddy_pop_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8069fba6
        balloonless_mode_drop_timer = struct.unpack('>f', data.read(4))[0]
    
        return cls(balloon_character, texture_set, mass, downward_velocity, extra_downward_collision, dk_riding_offset, start_offset, drop_height_above_spawn_point, dk_pop_effect, d_kand_diddy_pop_effect, dk_pop_sound, d_kand_diddy_pop_sound, balloonless_mode_drop_timer)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xf8\xb3\xab\xe0')  # 0xf8b3abe0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.balloon_character.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'k@\xac\xef')  # 0x6b40acef
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.texture_set))

        data.write(b'u\xdb\xb3u')  # 0x75dbb375
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.mass))

        data.write(b'\xdd\xb1iy')  # 0xddb16979
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.downward_velocity))

        data.write(b"\x9a'\xdd\xc3")  # 0x9a27ddc3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.extra_downward_collision))

        data.write(b'\xc0\xfe\x10\xc6')  # 0xc0fe10c6
        data.write(b'\x00\x0c')  # size
        self.dk_riding_offset.to_stream(data)

        data.write(b'@\x96\x18\xb6')  # 0x409618b6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.start_offset))

        data.write(b'\x80ax\xb3')  # 0x806178b3
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.drop_height_above_spawn_point))

        data.write(b'\xf52\xb5\xd3')  # 0xf532b5d3
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dk_pop_effect))

        data.write(b'\xca\xa9\xb3\xf5')  # 0xcaa9b3f5
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.d_kand_diddy_pop_effect))

        data.write(b'rl\x83\x9e')  # 0x726c839e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.dk_pop_sound))

        data.write(b'\\lx8')  # 0x5c6c7838
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.d_kand_diddy_pop_sound))

        data.write(b'\x80i\xfb\xa6')  # 0x8069fba6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.balloonless_mode_drop_timer))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BalloonDataJson", data)
        return cls(
            balloon_character=AnimationParameters.from_json(json_data['balloon_character']),
            texture_set=json_data['texture_set'],
            mass=json_data['mass'],
            downward_velocity=json_data['downward_velocity'],
            extra_downward_collision=json_data['extra_downward_collision'],
            dk_riding_offset=Vector.from_json(json_data['dk_riding_offset']),
            start_offset=json_data['start_offset'],
            drop_height_above_spawn_point=json_data['drop_height_above_spawn_point'],
            dk_pop_effect=json_data['dk_pop_effect'],
            d_kand_diddy_pop_effect=json_data['d_kand_diddy_pop_effect'],
            dk_pop_sound=json_data['dk_pop_sound'],
            d_kand_diddy_pop_sound=json_data['d_kand_diddy_pop_sound'],
            balloonless_mode_drop_timer=json_data['balloonless_mode_drop_timer'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'balloon_character': self.balloon_character.to_json(),
            'texture_set': self.texture_set,
            'mass': self.mass,
            'downward_velocity': self.downward_velocity,
            'extra_downward_collision': self.extra_downward_collision,
            'dk_riding_offset': self.dk_riding_offset.to_json(),
            'start_offset': self.start_offset,
            'drop_height_above_spawn_point': self.drop_height_above_spawn_point,
            'dk_pop_effect': self.dk_pop_effect,
            'd_kand_diddy_pop_effect': self.d_kand_diddy_pop_effect,
            'dk_pop_sound': self.dk_pop_sound,
            'd_kand_diddy_pop_sound': self.d_kand_diddy_pop_sound,
            'balloonless_mode_drop_timer': self.balloonless_mode_drop_timer,
        }


def _decode_texture_set(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_mass(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_downward_velocity(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_extra_downward_collision(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dk_riding_offset(data: typing.BinaryIO, property_size: int):
    return Vector.from_stream(data)


def _decode_start_offset(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_drop_height_above_spawn_point(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_dk_pop_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_d_kand_diddy_pop_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_dk_pop_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_d_kand_diddy_pop_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_balloonless_mode_drop_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf8b3abe0: ('balloon_character', AnimationParameters.from_stream),
    0x6b40acef: ('texture_set', _decode_texture_set),
    0x75dbb375: ('mass', _decode_mass),
    0xddb16979: ('downward_velocity', _decode_downward_velocity),
    0x9a27ddc3: ('extra_downward_collision', _decode_extra_downward_collision),
    0xc0fe10c6: ('dk_riding_offset', _decode_dk_riding_offset),
    0x409618b6: ('start_offset', _decode_start_offset),
    0x806178b3: ('drop_height_above_spawn_point', _decode_drop_height_above_spawn_point),
    0xf532b5d3: ('dk_pop_effect', _decode_dk_pop_effect),
    0xcaa9b3f5: ('d_kand_diddy_pop_effect', _decode_d_kand_diddy_pop_effect),
    0x726c839e: ('dk_pop_sound', _decode_dk_pop_sound),
    0x5c6c7838: ('d_kand_diddy_pop_sound', _decode_d_kand_diddy_pop_sound),
    0x8069fba6: ('balloonless_mode_drop_timer', _decode_balloonless_mode_drop_timer),
}
