# Generated File
from __future__ import annotations

import dataclasses
import struct
import typing
import typing_extensions

from retro_data_structures import json_util
from retro_data_structures.game_check import Game
from retro_data_structures.properties.base_property import BaseObjectType
from retro_data_structures.properties.field_reflection import FieldReflection
from retro_data_structures.properties.dkc_returns.archetypes.EditorProperties import EditorProperties

if typing.TYPE_CHECKING:
    class BonusRoomJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        use_timer: bool
        auto_start: bool
        timer_seconds: float
        warning_seconds: float
    

@dataclasses.dataclass()
class BonusRoom(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    use_timer: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xd569ad4d, original_name='UseTimer'
        ),
    })
    auto_start: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x3217dff8, original_name='AutoStart'
        ),
    })
    timer_seconds: float = dataclasses.field(default=10.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x6c160621, original_name='TimerSeconds'
        ),
    })
    warning_seconds: float = dataclasses.field(default=5.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7b1e2aeb, original_name='WarningSeconds'
        ),
    })

    @classmethod
    def game(cls) -> Game:
        return Game.DKC_RETURNS

    def get_name(self) -> str | None:
        return self.editor_properties.name

    def set_name(self, name: str) -> None:
        self.editor_properties.name = name

    @classmethod
    def object_type(cls) -> str:
        return 'BONU'

    @classmethod
    def from_stream(cls, data: typing.BinaryIO, size: int | None = None, default_override: dict | None = None) -> typing_extensions.Self:
        struct_id, size, property_count = struct.unpack(">LHH", data.read(8))
        assert struct_id == 0xFFFFFFFF
        root_size_start = data.tell() - 2

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

        assert data.tell() - root_size_start == size
        return cls(**present_fields)

    @classmethod
    def _fast_decode(cls, data: typing.BinaryIO, property_count: int) -> typing_extensions.Self | None:
        if property_count != 5:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x255a4580
        editor_properties = EditorProperties.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xd569ad4d
        use_timer = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x3217dff8
        auto_start = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6c160621
        timer_seconds = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7b1e2aeb
        warning_seconds = struct.unpack('>f', data.read(4))[0]
    
        return cls(editor_properties, use_timer, auto_start, timer_seconds, warning_seconds)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\xff\xff\xff\xff')  # struct object id
        root_size_offset = data.tell()
        data.write(b'\x00\x00')  # placeholder for root struct size
        data.write(b'\x00\x05')  # 5 properties

        data.write(b'%ZE\x80')  # 0x255a4580
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.editor_properties.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xd5i\xadM')  # 0xd569ad4d
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_timer))

        data.write(b'2\x17\xdf\xf8')  # 0x3217dff8
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.auto_start))

        data.write(b'l\x16\x06!')  # 0x6c160621
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.timer_seconds))

        data.write(b'{\x1e*\xeb')  # 0x7b1e2aeb
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.warning_seconds))

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BonusRoomJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            use_timer=json_data['use_timer'],
            auto_start=json_data['auto_start'],
            timer_seconds=json_data['timer_seconds'],
            warning_seconds=json_data['warning_seconds'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'use_timer': self.use_timer,
            'auto_start': self.auto_start,
            'timer_seconds': self.timer_seconds,
            'warning_seconds': self.warning_seconds,
        }


def _decode_use_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_auto_start(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_timer_seconds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_warning_seconds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0xd569ad4d: ('use_timer', _decode_use_timer),
    0x3217dff8: ('auto_start', _decode_auto_start),
    0x6c160621: ('timer_seconds', _decode_timer_seconds),
    0x7b1e2aeb: ('warning_seconds', _decode_warning_seconds),
}
