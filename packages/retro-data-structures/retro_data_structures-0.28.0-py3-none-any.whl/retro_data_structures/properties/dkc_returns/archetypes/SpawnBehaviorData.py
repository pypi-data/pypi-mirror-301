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
    class SpawnBehaviorDataJson(typing_extensions.TypedDict):
        play_spawn_animation: bool
        use_animation_to_drive_movement: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xa33cd77e, 0x80e700bd)


@dataclasses.dataclass()
class SpawnBehaviorData(BaseProperty):
    play_spawn_animation: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa33cd77e, original_name='PlaySpawnAnimation'
        ),
    })
    use_animation_to_drive_movement: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x80e700bd, original_name='UseAnimationToDriveMovement'
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
        if property_count != 2:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(14))
        assert (dec[0], dec[3]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xa3<\xd7~')  # 0xa33cd77e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.play_spawn_animation))

        data.write(b'\x80\xe7\x00\xbd')  # 0x80e700bd
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_animation_to_drive_movement))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("SpawnBehaviorDataJson", data)
        return cls(
            play_spawn_animation=json_data['play_spawn_animation'],
            use_animation_to_drive_movement=json_data['use_animation_to_drive_movement'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'play_spawn_animation': self.play_spawn_animation,
            'use_animation_to_drive_movement': self.use_animation_to_drive_movement,
        }


def _decode_play_spawn_animation(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_animation_to_drive_movement(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa33cd77e: ('play_spawn_animation', _decode_play_spawn_animation),
    0x80e700bd: ('use_animation_to_drive_movement', _decode_use_animation_to_drive_movement),
}
