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
    class ProjectileAttackBehaviorDataJson(typing_extensions.TypedDict):
        attack_range_squared: float
        use_horizontal_range_only: bool
        projectile_interval: float
        projectiles_in_salvo: int
        salvo_interval: float
        initial_projectile_delay: float
        launcher_specifies_launch_transform: bool
        fire_if_target_is_behind: bool
        fire_if_target_is_tar_inhibited: bool
        stop_while_firing: bool
        enforce_attack_requirements_at_launch_time: bool
        enforce_range_requirement_at_launch_time: bool
    

_FAST_FORMAT = None
_FAST_IDS = (0xde5bfc61, 0x7c16e269, 0xd4903c98, 0x2229b37e, 0x19d7ae87, 0xfc9c77d8, 0xbbd455d6, 0xaf452276, 0xf1004c52, 0xa19db1df, 0xf5a53cc1, 0x9d06b0fe)


@dataclasses.dataclass()
class ProjectileAttackBehaviorData(BaseProperty):
    attack_range_squared: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xde5bfc61, original_name='AttackRangeSquared'
        ),
    })
    use_horizontal_range_only: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7c16e269, original_name='UseHorizontalRangeOnly'
        ),
    })
    projectile_interval: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xd4903c98, original_name='ProjectileInterval'
        ),
    })
    projectiles_in_salvo: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x2229b37e, original_name='ProjectilesInSalvo'
        ),
    })
    salvo_interval: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x19d7ae87, original_name='SalvoInterval'
        ),
    })
    initial_projectile_delay: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xfc9c77d8, original_name='InitialProjectileDelay'
        ),
    })
    launcher_specifies_launch_transform: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xbbd455d6, original_name='LauncherSpecifiesLaunchTransform'
        ),
    })
    fire_if_target_is_behind: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xaf452276, original_name='FireIfTargetIsBehind'
        ),
    })
    fire_if_target_is_tar_inhibited: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf1004c52, original_name='FireIfTargetIsTarInhibited'
        ),
    })
    stop_while_firing: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xa19db1df, original_name='StopWhileFiring'
        ),
    })
    enforce_attack_requirements_at_launch_time: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xf5a53cc1, original_name='EnforceAttackRequirementsAtLaunchTime'
        ),
    })
    enforce_range_requirement_at_launch_time: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9d06b0fe, original_name='EnforceRangeRequirementAtLaunchTime'
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
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHfLH?LHfLHlLHfLHfLH?LH?LH?LH?LH?LH?')
    
        dec = _FAST_FORMAT.unpack(data.read(99))
        assert (dec[0], dec[3], dec[6], dec[9], dec[12], dec[15], dec[18], dec[21], dec[24], dec[27], dec[30], dec[33]) == _FAST_IDS
        return cls(
            dec[2],
            dec[5],
            dec[8],
            dec[11],
            dec[14],
            dec[17],
            dec[20],
            dec[23],
            dec[26],
            dec[29],
            dec[32],
            dec[35],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xde[\xfca')  # 0xde5bfc61
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.attack_range_squared))

        data.write(b'|\x16\xe2i')  # 0x7c16e269
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_horizontal_range_only))

        data.write(b'\xd4\x90<\x98')  # 0xd4903c98
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.projectile_interval))

        data.write(b'")\xb3~')  # 0x2229b37e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.projectiles_in_salvo))

        data.write(b'\x19\xd7\xae\x87')  # 0x19d7ae87
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.salvo_interval))

        data.write(b'\xfc\x9cw\xd8')  # 0xfc9c77d8
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.initial_projectile_delay))

        data.write(b'\xbb\xd4U\xd6')  # 0xbbd455d6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.launcher_specifies_launch_transform))

        data.write(b'\xafE"v')  # 0xaf452276
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.fire_if_target_is_behind))

        data.write(b'\xf1\x00LR')  # 0xf1004c52
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.fire_if_target_is_tar_inhibited))

        data.write(b'\xa1\x9d\xb1\xdf')  # 0xa19db1df
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.stop_while_firing))

        data.write(b'\xf5\xa5<\xc1')  # 0xf5a53cc1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enforce_attack_requirements_at_launch_time))

        data.write(b'\x9d\x06\xb0\xfe')  # 0x9d06b0fe
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enforce_range_requirement_at_launch_time))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ProjectileAttackBehaviorDataJson", data)
        return cls(
            attack_range_squared=json_data['attack_range_squared'],
            use_horizontal_range_only=json_data['use_horizontal_range_only'],
            projectile_interval=json_data['projectile_interval'],
            projectiles_in_salvo=json_data['projectiles_in_salvo'],
            salvo_interval=json_data['salvo_interval'],
            initial_projectile_delay=json_data['initial_projectile_delay'],
            launcher_specifies_launch_transform=json_data['launcher_specifies_launch_transform'],
            fire_if_target_is_behind=json_data['fire_if_target_is_behind'],
            fire_if_target_is_tar_inhibited=json_data['fire_if_target_is_tar_inhibited'],
            stop_while_firing=json_data['stop_while_firing'],
            enforce_attack_requirements_at_launch_time=json_data['enforce_attack_requirements_at_launch_time'],
            enforce_range_requirement_at_launch_time=json_data['enforce_range_requirement_at_launch_time'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attack_range_squared': self.attack_range_squared,
            'use_horizontal_range_only': self.use_horizontal_range_only,
            'projectile_interval': self.projectile_interval,
            'projectiles_in_salvo': self.projectiles_in_salvo,
            'salvo_interval': self.salvo_interval,
            'initial_projectile_delay': self.initial_projectile_delay,
            'launcher_specifies_launch_transform': self.launcher_specifies_launch_transform,
            'fire_if_target_is_behind': self.fire_if_target_is_behind,
            'fire_if_target_is_tar_inhibited': self.fire_if_target_is_tar_inhibited,
            'stop_while_firing': self.stop_while_firing,
            'enforce_attack_requirements_at_launch_time': self.enforce_attack_requirements_at_launch_time,
            'enforce_range_requirement_at_launch_time': self.enforce_range_requirement_at_launch_time,
        }


def _decode_attack_range_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_horizontal_range_only(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_projectile_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_projectiles_in_salvo(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_salvo_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_initial_projectile_delay(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_launcher_specifies_launch_transform(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fire_if_target_is_behind(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_fire_if_target_is_tar_inhibited(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_stop_while_firing(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enforce_attack_requirements_at_launch_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enforce_range_requirement_at_launch_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xde5bfc61: ('attack_range_squared', _decode_attack_range_squared),
    0x7c16e269: ('use_horizontal_range_only', _decode_use_horizontal_range_only),
    0xd4903c98: ('projectile_interval', _decode_projectile_interval),
    0x2229b37e: ('projectiles_in_salvo', _decode_projectiles_in_salvo),
    0x19d7ae87: ('salvo_interval', _decode_salvo_interval),
    0xfc9c77d8: ('initial_projectile_delay', _decode_initial_projectile_delay),
    0xbbd455d6: ('launcher_specifies_launch_transform', _decode_launcher_specifies_launch_transform),
    0xaf452276: ('fire_if_target_is_behind', _decode_fire_if_target_is_behind),
    0xf1004c52: ('fire_if_target_is_tar_inhibited', _decode_fire_if_target_is_tar_inhibited),
    0xa19db1df: ('stop_while_firing', _decode_stop_while_firing),
    0xf5a53cc1: ('enforce_attack_requirements_at_launch_time', _decode_enforce_attack_requirements_at_launch_time),
    0x9d06b0fe: ('enforce_range_requirement_at_launch_time', _decode_enforce_range_requirement_at_launch_time),
}
