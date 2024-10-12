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
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct160 import UnknownStruct160
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct161 import UnknownStruct161
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct26 import UnknownStruct26
from retro_data_structures.properties.dkc_returns.core.AssetId import AssetId, default_asset_id

if typing.TYPE_CHECKING:
    class UnknownStruct162Json(typing_extensions.TypedDict):
        gui_frame: int
        title_text: int
        continue_text: int
        core_continue_text: int
        retry_text: int
        core_retry_text: int
        retry_confirm_text: int
        best_time_text: int
        strg_0x42ba06cd: int
        strg_0xcff13915: int
        strg_0x8f791468: int
        strg_0x5e56e087: int
        strg_0xe38b44af: int
        right_reaching_location: int
        unknown_struct160: json_util.JsonObject
        unknown_struct161: json_util.JsonObject
        unknown_struct26_0x860139ad: json_util.JsonObject
        unknown_struct26_0x6a598a9b: json_util.JsonObject
        unknown_struct26_0xf24649ec: json_util.JsonObject
        unknown_struct26_0x4ed7e487: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct162(BaseProperty):
    gui_frame: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['FRME'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x806052cb, original_name='GuiFrame'
        ),
    })
    title_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xefc5a137, original_name='TitleText'
        ),
    })
    continue_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x1f5b271d, original_name='ContinueText'
        ),
    })
    core_continue_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x449f5275, original_name='CoreContinueText'
        ),
    })
    retry_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4cafddd1, original_name='RetryText'
        ),
    })
    core_retry_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x361ccf90, original_name='CoreRetryText'
        ),
    })
    retry_confirm_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4a5cb6ef, original_name='RetryConfirmText'
        ),
    })
    best_time_text: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xf4dafa61, original_name='BestTimeText'
        ),
    })
    strg_0x42ba06cd: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x42ba06cd, original_name='STRG'
        ),
    })
    strg_0xcff13915: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xcff13915, original_name='STRG'
        ),
    })
    strg_0x8f791468: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x8f791468, original_name='STRG'
        ),
    })
    strg_0x5e56e087: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x5e56e087, original_name='STRG'
        ),
    })
    strg_0xe38b44af: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0xe38b44af, original_name='STRG'
        ),
    })
    right_reaching_location: AssetId = dataclasses.field(default=default_asset_id, metadata={
        'asset_types': ['STRG'], 'reflection': FieldReflection[AssetId](
            AssetId, id=0x4a2bede4, original_name='RightReachingLocation'
        ),
    })
    unknown_struct160: UnknownStruct160 = dataclasses.field(default_factory=UnknownStruct160, metadata={
        'reflection': FieldReflection[UnknownStruct160](
            UnknownStruct160, id=0xacf22673, original_name='UnknownStruct160', from_json=UnknownStruct160.from_json, to_json=UnknownStruct160.to_json
        ),
    })
    unknown_struct161: UnknownStruct161 = dataclasses.field(default_factory=UnknownStruct161, metadata={
        'reflection': FieldReflection[UnknownStruct161](
            UnknownStruct161, id=0x5ba82f66, original_name='UnknownStruct161', from_json=UnknownStruct161.from_json, to_json=UnknownStruct161.to_json
        ),
    })
    unknown_struct26_0x860139ad: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x860139ad, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x6a598a9b: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x6a598a9b, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0xf24649ec: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0xf24649ec, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
        ),
    })
    unknown_struct26_0x4ed7e487: UnknownStruct26 = dataclasses.field(default_factory=UnknownStruct26, metadata={
        'reflection': FieldReflection[UnknownStruct26](
            UnknownStruct26, id=0x4ed7e487, original_name='UnknownStruct26', from_json=UnknownStruct26.from_json, to_json=UnknownStruct26.to_json
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
        if property_count != 20:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x806052cb
        gui_frame = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xefc5a137
        title_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1f5b271d
        continue_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x449f5275
        core_continue_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4cafddd1
        retry_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x361ccf90
        core_retry_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4a5cb6ef
        retry_confirm_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf4dafa61
        best_time_text = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x42ba06cd
        strg_0x42ba06cd = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcff13915
        strg_0xcff13915 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f791468
        strg_0x8f791468 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5e56e087
        strg_0x5e56e087 = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe38b44af
        strg_0xe38b44af = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4a2bede4
        right_reaching_location = struct.unpack(">Q", data.read(8))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xacf22673
        unknown_struct160 = UnknownStruct160.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x5ba82f66
        unknown_struct161 = UnknownStruct161.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x860139ad
        unknown_struct26_0x860139ad = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6a598a9b
        unknown_struct26_0x6a598a9b = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf24649ec
        unknown_struct26_0xf24649ec = UnknownStruct26.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4ed7e487
        unknown_struct26_0x4ed7e487 = UnknownStruct26.from_stream(data, property_size)
    
        return cls(gui_frame, title_text, continue_text, core_continue_text, retry_text, core_retry_text, retry_confirm_text, best_time_text, strg_0x42ba06cd, strg_0xcff13915, strg_0x8f791468, strg_0x5e56e087, strg_0xe38b44af, right_reaching_location, unknown_struct160, unknown_struct161, unknown_struct26_0x860139ad, unknown_struct26_0x6a598a9b, unknown_struct26_0xf24649ec, unknown_struct26_0x4ed7e487)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x14')  # 20 properties

        data.write(b'\x80`R\xcb')  # 0x806052cb
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.gui_frame))

        data.write(b'\xef\xc5\xa17')  # 0xefc5a137
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.title_text))

        data.write(b"\x1f['\x1d")  # 0x1f5b271d
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.continue_text))

        data.write(b'D\x9fRu')  # 0x449f5275
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.core_continue_text))

        data.write(b'L\xaf\xdd\xd1')  # 0x4cafddd1
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.retry_text))

        data.write(b'6\x1c\xcf\x90')  # 0x361ccf90
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.core_retry_text))

        data.write(b'J\\\xb6\xef')  # 0x4a5cb6ef
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.retry_confirm_text))

        data.write(b'\xf4\xda\xfaa')  # 0xf4dafa61
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.best_time_text))

        data.write(b'B\xba\x06\xcd')  # 0x42ba06cd
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x42ba06cd))

        data.write(b'\xcf\xf19\x15')  # 0xcff13915
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xcff13915))

        data.write(b'\x8fy\x14h')  # 0x8f791468
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x8f791468))

        data.write(b'^V\xe0\x87')  # 0x5e56e087
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0x5e56e087))

        data.write(b'\xe3\x8bD\xaf')  # 0xe38b44af
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.strg_0xe38b44af))

        data.write(b'J+\xed\xe4')  # 0x4a2bede4
        data.write(b'\x00\x08')  # size
        data.write(struct.pack(">Q", self.right_reaching_location))

        data.write(b'\xac\xf2&s')  # 0xacf22673
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct160.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'[\xa8/f')  # 0x5ba82f66
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct161.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x86\x019\xad')  # 0x860139ad
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x860139ad.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'jY\x8a\x9b')  # 0x6a598a9b
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x6a598a9b.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xf2FI\xec')  # 0xf24649ec
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0xf24649ec.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'N\xd7\xe4\x87')  # 0x4ed7e487
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct26_0x4ed7e487.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct162Json", data)
        return cls(
            gui_frame=json_data['gui_frame'],
            title_text=json_data['title_text'],
            continue_text=json_data['continue_text'],
            core_continue_text=json_data['core_continue_text'],
            retry_text=json_data['retry_text'],
            core_retry_text=json_data['core_retry_text'],
            retry_confirm_text=json_data['retry_confirm_text'],
            best_time_text=json_data['best_time_text'],
            strg_0x42ba06cd=json_data['strg_0x42ba06cd'],
            strg_0xcff13915=json_data['strg_0xcff13915'],
            strg_0x8f791468=json_data['strg_0x8f791468'],
            strg_0x5e56e087=json_data['strg_0x5e56e087'],
            strg_0xe38b44af=json_data['strg_0xe38b44af'],
            right_reaching_location=json_data['right_reaching_location'],
            unknown_struct160=UnknownStruct160.from_json(json_data['unknown_struct160']),
            unknown_struct161=UnknownStruct161.from_json(json_data['unknown_struct161']),
            unknown_struct26_0x860139ad=UnknownStruct26.from_json(json_data['unknown_struct26_0x860139ad']),
            unknown_struct26_0x6a598a9b=UnknownStruct26.from_json(json_data['unknown_struct26_0x6a598a9b']),
            unknown_struct26_0xf24649ec=UnknownStruct26.from_json(json_data['unknown_struct26_0xf24649ec']),
            unknown_struct26_0x4ed7e487=UnknownStruct26.from_json(json_data['unknown_struct26_0x4ed7e487']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'gui_frame': self.gui_frame,
            'title_text': self.title_text,
            'continue_text': self.continue_text,
            'core_continue_text': self.core_continue_text,
            'retry_text': self.retry_text,
            'core_retry_text': self.core_retry_text,
            'retry_confirm_text': self.retry_confirm_text,
            'best_time_text': self.best_time_text,
            'strg_0x42ba06cd': self.strg_0x42ba06cd,
            'strg_0xcff13915': self.strg_0xcff13915,
            'strg_0x8f791468': self.strg_0x8f791468,
            'strg_0x5e56e087': self.strg_0x5e56e087,
            'strg_0xe38b44af': self.strg_0xe38b44af,
            'right_reaching_location': self.right_reaching_location,
            'unknown_struct160': self.unknown_struct160.to_json(),
            'unknown_struct161': self.unknown_struct161.to_json(),
            'unknown_struct26_0x860139ad': self.unknown_struct26_0x860139ad.to_json(),
            'unknown_struct26_0x6a598a9b': self.unknown_struct26_0x6a598a9b.to_json(),
            'unknown_struct26_0xf24649ec': self.unknown_struct26_0xf24649ec.to_json(),
            'unknown_struct26_0x4ed7e487': self.unknown_struct26_0x4ed7e487.to_json(),
        }


def _decode_gui_frame(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_title_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_continue_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_core_continue_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_retry_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_core_retry_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_retry_confirm_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_best_time_text(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x42ba06cd(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xcff13915(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x8f791468(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0x5e56e087(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_strg_0xe38b44af(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


def _decode_right_reaching_location(data: typing.BinaryIO, property_size: int):
    return struct.unpack(">Q", data.read(8))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x806052cb: ('gui_frame', _decode_gui_frame),
    0xefc5a137: ('title_text', _decode_title_text),
    0x1f5b271d: ('continue_text', _decode_continue_text),
    0x449f5275: ('core_continue_text', _decode_core_continue_text),
    0x4cafddd1: ('retry_text', _decode_retry_text),
    0x361ccf90: ('core_retry_text', _decode_core_retry_text),
    0x4a5cb6ef: ('retry_confirm_text', _decode_retry_confirm_text),
    0xf4dafa61: ('best_time_text', _decode_best_time_text),
    0x42ba06cd: ('strg_0x42ba06cd', _decode_strg_0x42ba06cd),
    0xcff13915: ('strg_0xcff13915', _decode_strg_0xcff13915),
    0x8f791468: ('strg_0x8f791468', _decode_strg_0x8f791468),
    0x5e56e087: ('strg_0x5e56e087', _decode_strg_0x5e56e087),
    0xe38b44af: ('strg_0xe38b44af', _decode_strg_0xe38b44af),
    0x4a2bede4: ('right_reaching_location', _decode_right_reaching_location),
    0xacf22673: ('unknown_struct160', UnknownStruct160.from_stream),
    0x5ba82f66: ('unknown_struct161', UnknownStruct161.from_stream),
    0x860139ad: ('unknown_struct26_0x860139ad', UnknownStruct26.from_stream),
    0x6a598a9b: ('unknown_struct26_0x6a598a9b', UnknownStruct26.from_stream),
    0xf24649ec: ('unknown_struct26_0xf24649ec', UnknownStruct26.from_stream),
    0x4ed7e487: ('unknown_struct26_0x4ed7e487', UnknownStruct26.from_stream),
}
