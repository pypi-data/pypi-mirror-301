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

if typing.TYPE_CHECKING:
    class DespawnRulesJson(typing_extensions.TypedDict):
        can_despawn: bool
        respawn_after_death: bool
        wait_for_despawn_after_death: bool
        respawn_after_despawn: bool
        wait_for_despawn_after_child_despawn: bool
        spawns_on_screen: bool
        set_facing_on_respawn: bool
        respect_player_respawn_break: bool
        screen_planes: int
        despawn_timer: float
        despawn_distance: float
        far_despawn_distance: float
        activation_distance: float
        use_minimum_activation_distance: bool
        minimum_activation_distance: float
        respawn_after_despawn_delay: float
        use_player_activation_distance: bool
        player_activation_distance_squared: float
    

_FAST_FORMAT = None
_FAST_IDS = (0x5c9a798c, 0x77869a76, 0x7aee0c0a, 0xc26d7475, 0xe8be10dc, 0x826952e9, 0x78badfc1, 0x100ebf3a, 0x62249fb, 0xbc2f0b41, 0xe7655628, 0xebe02cd7, 0xf90a4fe9, 0x50c31684, 0xd64eff80, 0x1745dd26, 0x6a9ad7df, 0xf5495f77)


@dataclasses.dataclass()
class DespawnRules(BaseProperty):
    can_despawn: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x5c9a798c, original_name='CanDespawn'
        ),
    })
    respawn_after_death: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x77869a76, original_name='RespawnAfterDeath'
        ),
    })
    wait_for_despawn_after_death: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7aee0c0a, original_name='WaitForDespawnAfterDeath'
        ),
    })
    respawn_after_despawn: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xc26d7475, original_name='RespawnAfterDespawn'
        ),
    })
    wait_for_despawn_after_child_despawn: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xe8be10dc, original_name='WaitForDespawnAfterChildDespawn'
        ),
    })
    spawns_on_screen: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x826952e9, original_name='SpawnsOnScreen'
        ),
    })
    set_facing_on_respawn: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x78badfc1, original_name='SetFacingOnRespawn'
        ),
    })
    respect_player_respawn_break: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x100ebf3a, original_name='RespectPlayerRespawnBreak'
        ),
    })
    screen_planes: enums.ScreenPlanes = dataclasses.field(default=enums.ScreenPlanes.Unknown1, metadata={
        'reflection': FieldReflection[enums.ScreenPlanes](
            enums.ScreenPlanes, id=0x062249fb, original_name='ScreenPlanes', from_json=enums.ScreenPlanes.from_json, to_json=enums.ScreenPlanes.to_json
        ),
    })
    despawn_timer: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xbc2f0b41, original_name='DespawnTimer'
        ),
    })
    despawn_distance: float = dataclasses.field(default=15.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe7655628, original_name='DespawnDistance'
        ),
    })
    far_despawn_distance: float = dataclasses.field(default=25.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xebe02cd7, original_name='FarDespawnDistance'
        ),
    })
    activation_distance: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf90a4fe9, original_name='ActivationDistance'
        ),
    })
    use_minimum_activation_distance: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x50c31684, original_name='UseMinimumActivationDistance'
        ),
    })
    minimum_activation_distance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd64eff80, original_name='MinimumActivationDistance'
        ),
    })
    respawn_after_despawn_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x1745dd26, original_name='RespawnAfterDespawnDelay'
        ),
    })
    use_player_activation_distance: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6a9ad7df, original_name='UsePlayerActivationDistance'
        ),
    })
    player_activation_distance_squared: float = dataclasses.field(default=4.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf5495f77, original_name='PlayerActivationDistanceSquared'
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
        if property_count != 18:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LH?LH?LH?LH?LH?LH?LH?LH?LHLLHfLHfLHfLHfLH?LHfLHfLH?LHf')
    
        dec = _FAST_FORMAT.unpack(data.read(150))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33], dec[36], dec[39], dec[42], dec[45], dec[48], dec[51]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            enums.ScreenPlanes(dec[26]),
            dec[29],
            dec[32],
            dec[35],
            dec[38],
            dec[41],
            dec[44],
            dec[47],
            dec[50],
            dec[53],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x12')  # 18 properties

        data.write(b'\\\x9ay\x8c')  # 0x5c9a798c
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.can_despawn))

        data.write(b'w\x86\x9av')  # 0x77869a76
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.respawn_after_death))

        data.write(b'z\xee\x0c\n')  # 0x7aee0c0a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.wait_for_despawn_after_death))

        data.write(b'\xc2mtu')  # 0xc26d7475
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.respawn_after_despawn))

        data.write(b'\xe8\xbe\x10\xdc')  # 0xe8be10dc
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.wait_for_despawn_after_child_despawn))

        data.write(b'\x82iR\xe9')  # 0x826952e9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.spawns_on_screen))

        data.write(b'x\xba\xdf\xc1')  # 0x78badfc1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.set_facing_on_respawn))

        data.write(b'\x10\x0e\xbf:')  # 0x100ebf3a
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.respect_player_respawn_break))

        data.write(b'\x06"I\xfb')  # 0x62249fb
        data.write(b'\x00\x04')  # size
        self.screen_planes.to_stream(data)

        data.write(b'\xbc/\x0bA')  # 0xbc2f0b41
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.despawn_timer))

        data.write(b'\xe7eV(')  # 0xe7655628
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.despawn_distance))

        data.write(b'\xeb\xe0,\xd7')  # 0xebe02cd7
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.far_despawn_distance))

        data.write(b'\xf9\nO\xe9')  # 0xf90a4fe9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.activation_distance))

        data.write(b'P\xc3\x16\x84')  # 0x50c31684
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_minimum_activation_distance))

        data.write(b'\xd6N\xff\x80')  # 0xd64eff80
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_activation_distance))

        data.write(b'\x17E\xdd&')  # 0x1745dd26
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.respawn_after_despawn_delay))

        data.write(b'j\x9a\xd7\xdf')  # 0x6a9ad7df
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_player_activation_distance))

        data.write(b'\xf5I_w')  # 0xf5495f77
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.player_activation_distance_squared))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("DespawnRulesJson", data)
        return cls(
            can_despawn=json_data['can_despawn'],
            respawn_after_death=json_data['respawn_after_death'],
            wait_for_despawn_after_death=json_data['wait_for_despawn_after_death'],
            respawn_after_despawn=json_data['respawn_after_despawn'],
            wait_for_despawn_after_child_despawn=json_data['wait_for_despawn_after_child_despawn'],
            spawns_on_screen=json_data['spawns_on_screen'],
            set_facing_on_respawn=json_data['set_facing_on_respawn'],
            respect_player_respawn_break=json_data['respect_player_respawn_break'],
            screen_planes=enums.ScreenPlanes.from_json(json_data['screen_planes']),
            despawn_timer=json_data['despawn_timer'],
            despawn_distance=json_data['despawn_distance'],
            far_despawn_distance=json_data['far_despawn_distance'],
            activation_distance=json_data['activation_distance'],
            use_minimum_activation_distance=json_data['use_minimum_activation_distance'],
            minimum_activation_distance=json_data['minimum_activation_distance'],
            respawn_after_despawn_delay=json_data['respawn_after_despawn_delay'],
            use_player_activation_distance=json_data['use_player_activation_distance'],
            player_activation_distance_squared=json_data['player_activation_distance_squared'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'can_despawn': self.can_despawn,
            'respawn_after_death': self.respawn_after_death,
            'wait_for_despawn_after_death': self.wait_for_despawn_after_death,
            'respawn_after_despawn': self.respawn_after_despawn,
            'wait_for_despawn_after_child_despawn': self.wait_for_despawn_after_child_despawn,
            'spawns_on_screen': self.spawns_on_screen,
            'set_facing_on_respawn': self.set_facing_on_respawn,
            'respect_player_respawn_break': self.respect_player_respawn_break,
            'screen_planes': self.screen_planes.to_json(),
            'despawn_timer': self.despawn_timer,
            'despawn_distance': self.despawn_distance,
            'far_despawn_distance': self.far_despawn_distance,
            'activation_distance': self.activation_distance,
            'use_minimum_activation_distance': self.use_minimum_activation_distance,
            'minimum_activation_distance': self.minimum_activation_distance,
            'respawn_after_despawn_delay': self.respawn_after_despawn_delay,
            'use_player_activation_distance': self.use_player_activation_distance,
            'player_activation_distance_squared': self.player_activation_distance_squared,
        }


def _decode_can_despawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_respawn_after_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_wait_for_despawn_after_death(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_respawn_after_despawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_wait_for_despawn_after_child_despawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_spawns_on_screen(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_set_facing_on_respawn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_respect_player_respawn_break(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_screen_planes(data: typing.BinaryIO, property_size: int):
    return enums.ScreenPlanes.from_stream(data)


def _decode_despawn_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_despawn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_far_despawn_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_activation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_minimum_activation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_activation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_respawn_after_despawn_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_player_activation_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_player_activation_distance_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x5c9a798c: ('can_despawn', _decode_can_despawn),
    0x77869a76: ('respawn_after_death', _decode_respawn_after_death),
    0x7aee0c0a: ('wait_for_despawn_after_death', _decode_wait_for_despawn_after_death),
    0xc26d7475: ('respawn_after_despawn', _decode_respawn_after_despawn),
    0xe8be10dc: ('wait_for_despawn_after_child_despawn', _decode_wait_for_despawn_after_child_despawn),
    0x826952e9: ('spawns_on_screen', _decode_spawns_on_screen),
    0x78badfc1: ('set_facing_on_respawn', _decode_set_facing_on_respawn),
    0x100ebf3a: ('respect_player_respawn_break', _decode_respect_player_respawn_break),
    0x62249fb: ('screen_planes', _decode_screen_planes),
    0xbc2f0b41: ('despawn_timer', _decode_despawn_timer),
    0xe7655628: ('despawn_distance', _decode_despawn_distance),
    0xebe02cd7: ('far_despawn_distance', _decode_far_despawn_distance),
    0xf90a4fe9: ('activation_distance', _decode_activation_distance),
    0x50c31684: ('use_minimum_activation_distance', _decode_use_minimum_activation_distance),
    0xd64eff80: ('minimum_activation_distance', _decode_minimum_activation_distance),
    0x1745dd26: ('respawn_after_despawn_delay', _decode_respawn_after_despawn_delay),
    0x6a9ad7df: ('use_player_activation_distance', _decode_use_player_activation_distance),
    0xf5495f77: ('player_activation_distance_squared', _decode_player_activation_distance_squared),
}
