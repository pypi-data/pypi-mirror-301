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
from retro_data_structures.properties.dkc_returns.archetypes.IslandAreaStruct import IslandAreaStruct
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct184Json(typing_extensions.TypedDict):
        title: int
        item_names: int
        descriptions: int
        confirm: int
        entry_strings: int
        exit_strings: int
        island_area_struct_0x57cb6052: json_util.JsonObject
        island_area_struct_0x4c256cd9: json_util.JsonObject
        island_area_struct_0xfa4dc52c: json_util.JsonObject
        island_area_struct_0x7803ae46: json_util.JsonObject
        island_area_struct_0x2ed30bdd: json_util.JsonObject
        island_area_struct_0xcfbdcf70: json_util.JsonObject
        island_area_struct_0xd611406b: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct184(BaseProperty):
    title: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xa4f20c17, original_name='Title'
        ),
    })
    item_names: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x8067fe4e, original_name='ItemNames'
        ),
    })
    descriptions: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xb9b18ef6, original_name='Descriptions'
        ),
    })
    confirm: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x241839d4, original_name='Confirm'
        ),
    })
    entry_strings: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf9529b46, original_name='EntryStrings'
        ),
    })
    exit_strings: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1359360d, original_name='ExitStrings'
        ),
    })
    island_area_struct_0x57cb6052: IslandAreaStruct = dataclasses.field(default_factory=IslandAreaStruct, metadata={
        'reflection': FieldReflection[IslandAreaStruct](
            IslandAreaStruct, id=0x57cb6052, original_name='IslandAreaStruct', from_json=IslandAreaStruct.from_json, to_json=IslandAreaStruct.to_json
        ),
    })
    island_area_struct_0x4c256cd9: IslandAreaStruct = dataclasses.field(default_factory=IslandAreaStruct, metadata={
        'reflection': FieldReflection[IslandAreaStruct](
            IslandAreaStruct, id=0x4c256cd9, original_name='IslandAreaStruct', from_json=IslandAreaStruct.from_json, to_json=IslandAreaStruct.to_json
        ),
    })
    island_area_struct_0xfa4dc52c: IslandAreaStruct = dataclasses.field(default_factory=IslandAreaStruct, metadata={
        'reflection': FieldReflection[IslandAreaStruct](
            IslandAreaStruct, id=0xfa4dc52c, original_name='IslandAreaStruct', from_json=IslandAreaStruct.from_json, to_json=IslandAreaStruct.to_json
        ),
    })
    island_area_struct_0x7803ae46: IslandAreaStruct = dataclasses.field(default_factory=IslandAreaStruct, metadata={
        'reflection': FieldReflection[IslandAreaStruct](
            IslandAreaStruct, id=0x7803ae46, original_name='IslandAreaStruct', from_json=IslandAreaStruct.from_json, to_json=IslandAreaStruct.to_json
        ),
    })
    island_area_struct_0x2ed30bdd: IslandAreaStruct = dataclasses.field(default_factory=IslandAreaStruct, metadata={
        'reflection': FieldReflection[IslandAreaStruct](
            IslandAreaStruct, id=0x2ed30bdd, original_name='IslandAreaStruct', from_json=IslandAreaStruct.from_json, to_json=IslandAreaStruct.to_json
        ),
    })
    island_area_struct_0xcfbdcf70: IslandAreaStruct = dataclasses.field(default_factory=IslandAreaStruct, metadata={
        'reflection': FieldReflection[IslandAreaStruct](
            IslandAreaStruct, id=0xcfbdcf70, original_name='IslandAreaStruct', from_json=IslandAreaStruct.from_json, to_json=IslandAreaStruct.to_json
        ),
    })
    island_area_struct_0xd611406b: IslandAreaStruct = dataclasses.field(default_factory=IslandAreaStruct, metadata={
        'reflection': FieldReflection[IslandAreaStruct](
            IslandAreaStruct, id=0xd611406b, original_name='IslandAreaStruct', from_json=IslandAreaStruct.from_json, to_json=IslandAreaStruct.to_json
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
        assert property_id == 0xa4f20c17
        title = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8067fe4e
        item_names = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xb9b18ef6
        descriptions = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x241839d4
        confirm = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf9529b46
        entry_strings = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1359360d
        exit_strings = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x57cb6052
        island_area_struct_0x57cb6052 = IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 1})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4c256cd9
        island_area_struct_0x4c256cd9 = IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 30})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xfa4dc52c
        island_area_struct_0xfa4dc52c = IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 10})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7803ae46
        island_area_struct_0x7803ae46 = IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 20})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2ed30bdd
        island_area_struct_0x2ed30bdd = IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 7})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcfbdcf70
        island_area_struct_0xcfbdcf70 = IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 20})
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd611406b
        island_area_struct_0xd611406b = IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 40})
    
        return cls(title, item_names, descriptions, confirm, entry_strings, exit_strings, island_area_struct_0x57cb6052, island_area_struct_0x4c256cd9, island_area_struct_0xfa4dc52c, island_area_struct_0x7803ae46, island_area_struct_0x2ed30bdd, island_area_struct_0xcfbdcf70, island_area_struct_0xd611406b)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xa4\xf2\x0c\x17')  # 0xa4f20c17
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title))

        data.write(b'\x80g\xfeN')  # 0x8067fe4e
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.item_names))

        data.write(b'\xb9\xb1\x8e\xf6')  # 0xb9b18ef6
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.descriptions))

        data.write(b'$\x189\xd4')  # 0x241839d4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.confirm))

        data.write(b'\xf9R\x9bF')  # 0xf9529b46
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.entry_strings))

        data.write(b'\x13Y6\r')  # 0x1359360d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.exit_strings))

        data.write(b'W\xcb`R')  # 0x57cb6052
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_area_struct_0x57cb6052.to_stream(data, default_override={'cost': 1})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'L%l\xd9')  # 0x4c256cd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_area_struct_0x4c256cd9.to_stream(data, default_override={'cost': 30})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xfaM\xc5,')  # 0xfa4dc52c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_area_struct_0xfa4dc52c.to_stream(data, default_override={'cost': 10})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'x\x03\xaeF')  # 0x7803ae46
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_area_struct_0x7803ae46.to_stream(data, default_override={'cost': 20})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'.\xd3\x0b\xdd')  # 0x2ed30bdd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_area_struct_0x2ed30bdd.to_stream(data, default_override={'cost': 7})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xcf\xbd\xcfp')  # 0xcfbdcf70
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_area_struct_0xcfbdcf70.to_stream(data, default_override={'cost': 20})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd6\x11@k')  # 0xd611406b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.island_area_struct_0xd611406b.to_stream(data, default_override={'cost': 40})
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct184Json", data)
        return cls(
            title=json_data['title'],
            item_names=json_data['item_names'],
            descriptions=json_data['descriptions'],
            confirm=json_data['confirm'],
            entry_strings=json_data['entry_strings'],
            exit_strings=json_data['exit_strings'],
            island_area_struct_0x57cb6052=IslandAreaStruct.from_json(json_data['island_area_struct_0x57cb6052']),
            island_area_struct_0x4c256cd9=IslandAreaStruct.from_json(json_data['island_area_struct_0x4c256cd9']),
            island_area_struct_0xfa4dc52c=IslandAreaStruct.from_json(json_data['island_area_struct_0xfa4dc52c']),
            island_area_struct_0x7803ae46=IslandAreaStruct.from_json(json_data['island_area_struct_0x7803ae46']),
            island_area_struct_0x2ed30bdd=IslandAreaStruct.from_json(json_data['island_area_struct_0x2ed30bdd']),
            island_area_struct_0xcfbdcf70=IslandAreaStruct.from_json(json_data['island_area_struct_0xcfbdcf70']),
            island_area_struct_0xd611406b=IslandAreaStruct.from_json(json_data['island_area_struct_0xd611406b']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'title': self.title,
            'item_names': self.item_names,
            'descriptions': self.descriptions,
            'confirm': self.confirm,
            'entry_strings': self.entry_strings,
            'exit_strings': self.exit_strings,
            'island_area_struct_0x57cb6052': self.island_area_struct_0x57cb6052.to_json(),
            'island_area_struct_0x4c256cd9': self.island_area_struct_0x4c256cd9.to_json(),
            'island_area_struct_0xfa4dc52c': self.island_area_struct_0xfa4dc52c.to_json(),
            'island_area_struct_0x7803ae46': self.island_area_struct_0x7803ae46.to_json(),
            'island_area_struct_0x2ed30bdd': self.island_area_struct_0x2ed30bdd.to_json(),
            'island_area_struct_0xcfbdcf70': self.island_area_struct_0xcfbdcf70.to_json(),
            'island_area_struct_0xd611406b': self.island_area_struct_0xd611406b.to_json(),
        }


def _decode_title(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_item_names(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_descriptions(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_confirm(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_entry_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_exit_strings(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_island_area_struct_0x57cb6052(data: typing.BinaryIO, property_size: int):
    return IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 1})


def _decode_island_area_struct_0x4c256cd9(data: typing.BinaryIO, property_size: int):
    return IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 30})


def _decode_island_area_struct_0xfa4dc52c(data: typing.BinaryIO, property_size: int):
    return IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 10})


def _decode_island_area_struct_0x7803ae46(data: typing.BinaryIO, property_size: int):
    return IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 20})


def _decode_island_area_struct_0x2ed30bdd(data: typing.BinaryIO, property_size: int):
    return IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 7})


def _decode_island_area_struct_0xcfbdcf70(data: typing.BinaryIO, property_size: int):
    return IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 20})


def _decode_island_area_struct_0xd611406b(data: typing.BinaryIO, property_size: int):
    return IslandAreaStruct.from_stream(data, property_size, default_override={'cost': 40})


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa4f20c17: ('title', _decode_title),
    0x8067fe4e: ('item_names', _decode_item_names),
    0xb9b18ef6: ('descriptions', _decode_descriptions),
    0x241839d4: ('confirm', _decode_confirm),
    0xf9529b46: ('entry_strings', _decode_entry_strings),
    0x1359360d: ('exit_strings', _decode_exit_strings),
    0x57cb6052: ('island_area_struct_0x57cb6052', _decode_island_area_struct_0x57cb6052),
    0x4c256cd9: ('island_area_struct_0x4c256cd9', _decode_island_area_struct_0x4c256cd9),
    0xfa4dc52c: ('island_area_struct_0xfa4dc52c', _decode_island_area_struct_0xfa4dc52c),
    0x7803ae46: ('island_area_struct_0x7803ae46', _decode_island_area_struct_0x7803ae46),
    0x2ed30bdd: ('island_area_struct_0x2ed30bdd', _decode_island_area_struct_0x2ed30bdd),
    0xcfbdcf70: ('island_area_struct_0xcfbdcf70', _decode_island_area_struct_0xcfbdcf70),
    0xd611406b: ('island_area_struct_0xd611406b', _decode_island_area_struct_0xd611406b),
}
