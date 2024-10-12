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

if typing.TYPE_CHECKING:
    class PlayerTarInteractionDataJson(typing_extensions.TypedDict):
        uses_tar_in_this_level: bool
        inhibit_player_on_tar_pit_exit: bool
        num_tar_inhibitors_for_tar_mode: int
        num_ground_pounds_to_break_tar_mode: int
        ground_pound_cool_down: float
        tar_ground_pound_effect: int
        tar_ground_pound_effect_locator: str
        tar_jump_land_effect: int
        tar_jump_land_effect_locator: str
        tar_liberation_effect: int
        tar_liberation_sound: int
        tar_liberation_effect_locator: str
    

@dataclasses.dataclass()
class PlayerTarInteractionData(BaseProperty):
    uses_tar_in_this_level: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xb54eefd1, original_name='UsesTarInThisLevel'
        ),
    })
    inhibit_player_on_tar_pit_exit: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7c94aa3b, original_name='InhibitPlayerOnTarPitExit'
        ),
    })
    num_tar_inhibitors_for_tar_mode: int = dataclasses.field(default=3, metadata={
        'reflection': FieldReflection[int](
            int, id=0x00f49200, original_name='NumTarInhibitorsForTarMode'
        ),
    })
    num_ground_pounds_to_break_tar_mode: int = dataclasses.field(default=3, metadata={
        'reflection': FieldReflection[int](
            int, id=0x20ab95e5, original_name='NumGroundPoundsToBreakTarMode'
        ),
    })
    ground_pound_cool_down: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x5db3fa1f, original_name='GroundPoundCoolDown'
        ),
    })
    tar_ground_pound_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x798f7740, original_name='TarGroundPoundEffect'
        ),
    })
    tar_ground_pound_effect_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x1c6b87a3, original_name='TarGroundPoundEffectLocator'
        ),
    })
    tar_jump_land_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x51ea29b6, original_name='TarJumpLandEffect'
        ),
    })
    tar_jump_land_effect_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0xff0df2a8, original_name='TarJumpLandEffectLocator'
        ),
    })
    tar_liberation_effect: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['PART'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x7ee095e2, original_name='TarLiberationEffect'
        ),
    })
    tar_liberation_sound: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['CAUD'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1ef458c4, original_name='TarLiberationSound'
        ),
    })
    tar_liberation_effect_locator: str = dataclasses.field(default='', metadata={
        'reflection': FieldReflection[str](
            str, id=0x2bbeb1f3, original_name='TarLiberationEffectLocator'
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb54eefd1
        uses_tar_in_this_level = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7c94aa3b
        inhibit_player_on_tar_pit_exit = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x00f49200
        num_tar_inhibitors_for_tar_mode = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x20ab95e5
        num_ground_pounds_to_break_tar_mode = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5db3fa1f
        ground_pound_cool_down = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x798f7740
        tar_ground_pound_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1c6b87a3
        tar_ground_pound_effect_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x51ea29b6
        tar_jump_land_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xff0df2a8
        tar_jump_land_effect_locator = data.read(property_size)[:-1].decode("utf-8")
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7ee095e2
        tar_liberation_effect = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1ef458c4
        tar_liberation_sound = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2bbeb1f3
        tar_liberation_effect_locator = data.read(property_size)[:-1].decode("utf-8")
    
        return cls(uses_tar_in_this_level, inhibit_player_on_tar_pit_exit, num_tar_inhibitors_for_tar_mode, num_ground_pounds_to_break_tar_mode, ground_pound_cool_down, tar_ground_pound_effect, tar_ground_pound_effect_locator, tar_jump_land_effect, tar_jump_land_effect_locator, tar_liberation_effect, tar_liberation_sound, tar_liberation_effect_locator)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0c')  # 12 properties

        data.write(b'\xb5N\xef\xd1')  # 0xb54eefd1
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.uses_tar_in_this_level))

        data.write(b'|\x94\xaa;')  # 0x7c94aa3b
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.inhibit_player_on_tar_pit_exit))

        data.write(b'\x00\xf4\x92\x00')  # 0xf49200
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_tar_inhibitors_for_tar_mode))

        data.write(b' \xab\x95\xe5')  # 0x20ab95e5
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_ground_pounds_to_break_tar_mode))

        data.write(b']\xb3\xfa\x1f')  # 0x5db3fa1f
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.ground_pound_cool_down))

        data.write(b'y\x8fw@')  # 0x798f7740
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tar_ground_pound_effect))

        data.write(b'\x1ck\x87\xa3')  # 0x1c6b87a3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.tar_ground_pound_effect_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'Q\xea)\xb6')  # 0x51ea29b6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tar_jump_land_effect))

        data.write(b'\xff\r\xf2\xa8')  # 0xff0df2a8
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.tar_jump_land_effect_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'~\xe0\x95\xe2')  # 0x7ee095e2
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tar_liberation_effect))

        data.write(b'\x1e\xf4X\xc4')  # 0x1ef458c4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.tar_liberation_sound))

        data.write(b'+\xbe\xb1\xf3')  # 0x2bbeb1f3
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        data.write(self.tar_liberation_effect_locator.encode("utf-8"))
        data.write(b'\x00')
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("PlayerTarInteractionDataJson", data)
        return cls(
            uses_tar_in_this_level=json_data['uses_tar_in_this_level'],
            inhibit_player_on_tar_pit_exit=json_data['inhibit_player_on_tar_pit_exit'],
            num_tar_inhibitors_for_tar_mode=json_data['num_tar_inhibitors_for_tar_mode'],
            num_ground_pounds_to_break_tar_mode=json_data['num_ground_pounds_to_break_tar_mode'],
            ground_pound_cool_down=json_data['ground_pound_cool_down'],
            tar_ground_pound_effect=json_data['tar_ground_pound_effect'],
            tar_ground_pound_effect_locator=json_data['tar_ground_pound_effect_locator'],
            tar_jump_land_effect=json_data['tar_jump_land_effect'],
            tar_jump_land_effect_locator=json_data['tar_jump_land_effect_locator'],
            tar_liberation_effect=json_data['tar_liberation_effect'],
            tar_liberation_sound=json_data['tar_liberation_sound'],
            tar_liberation_effect_locator=json_data['tar_liberation_effect_locator'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'uses_tar_in_this_level': self.uses_tar_in_this_level,
            'inhibit_player_on_tar_pit_exit': self.inhibit_player_on_tar_pit_exit,
            'num_tar_inhibitors_for_tar_mode': self.num_tar_inhibitors_for_tar_mode,
            'num_ground_pounds_to_break_tar_mode': self.num_ground_pounds_to_break_tar_mode,
            'ground_pound_cool_down': self.ground_pound_cool_down,
            'tar_ground_pound_effect': self.tar_ground_pound_effect,
            'tar_ground_pound_effect_locator': self.tar_ground_pound_effect_locator,
            'tar_jump_land_effect': self.tar_jump_land_effect,
            'tar_jump_land_effect_locator': self.tar_jump_land_effect_locator,
            'tar_liberation_effect': self.tar_liberation_effect,
            'tar_liberation_sound': self.tar_liberation_sound,
            'tar_liberation_effect_locator': self.tar_liberation_effect_locator,
        }


def _decode_uses_tar_in_this_level(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_inhibit_player_on_tar_pit_exit(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_num_tar_inhibitors_for_tar_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_num_ground_pounds_to_break_tar_mode(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_ground_pound_cool_down(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_tar_ground_pound_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tar_ground_pound_effect_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_tar_jump_land_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tar_jump_land_effect_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


def _decode_tar_liberation_effect(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tar_liberation_sound(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_tar_liberation_effect_locator(data: typing.BinaryIO, property_size: int):
    return data.read(property_size)[:-1].decode("utf-8")


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb54eefd1: ('uses_tar_in_this_level', _decode_uses_tar_in_this_level),
    0x7c94aa3b: ('inhibit_player_on_tar_pit_exit', _decode_inhibit_player_on_tar_pit_exit),
    0xf49200: ('num_tar_inhibitors_for_tar_mode', _decode_num_tar_inhibitors_for_tar_mode),
    0x20ab95e5: ('num_ground_pounds_to_break_tar_mode', _decode_num_ground_pounds_to_break_tar_mode),
    0x5db3fa1f: ('ground_pound_cool_down', _decode_ground_pound_cool_down),
    0x798f7740: ('tar_ground_pound_effect', _decode_tar_ground_pound_effect),
    0x1c6b87a3: ('tar_ground_pound_effect_locator', _decode_tar_ground_pound_effect_locator),
    0x51ea29b6: ('tar_jump_land_effect', _decode_tar_jump_land_effect),
    0xff0df2a8: ('tar_jump_land_effect_locator', _decode_tar_jump_land_effect_locator),
    0x7ee095e2: ('tar_liberation_effect', _decode_tar_liberation_effect),
    0x1ef458c4: ('tar_liberation_sound', _decode_tar_liberation_sound),
    0x2bbeb1f3: ('tar_liberation_effect_locator', _decode_tar_liberation_effect_locator),
}
