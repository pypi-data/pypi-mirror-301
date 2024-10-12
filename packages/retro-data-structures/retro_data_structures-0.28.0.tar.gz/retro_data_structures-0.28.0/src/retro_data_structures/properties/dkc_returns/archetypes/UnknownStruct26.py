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
from retro_data_structures.properties.dkc_returns.core.Color import Color

if typing.TYPE_CHECKING:
    class UnknownStruct26Json(typing_extensions.TypedDict):
        text_gradient_start_color: json_util.JsonValue
        text_gradient_end_color: json_util.JsonValue
        text_outline_color: json_util.JsonValue
    

_FAST_FORMAT = None
_FAST_IDS = (0xf9e0d0fb, 0xe0417e89, 0xf2e13506)


@dataclasses.dataclass()
class UnknownStruct26(BaseProperty):
    text_gradient_start_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.9960780143737793, g=0.9764710068702698, b=0.6078429818153381, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xf9e0d0fb, original_name='TextGradientStartColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    text_gradient_end_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.9568629860877991, g=0.7882350087165833, b=0.32548999786376953, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xe0417e89, original_name='TextGradientEndColor', from_json=Color.from_json, to_json=Color.to_json
        ),
    })
    text_outline_color: Color = dataclasses.field(default_factory=lambda: Color(r=0.764706015586853, g=0.04705899953842163, b=0.031373001635074615, a=0.0), metadata={
        'reflection': FieldReflection[Color](
            Color, id=0xf2e13506, original_name='TextOutlineColor', from_json=Color.from_json, to_json=Color.to_json
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
        if property_count != 3:
            return None
    
        global _FAST_FORMAT
        if _FAST_FORMAT is None:
            _FAST_FORMAT = struct.Struct('>LHffffLHffffLHffff')
    
        dec = _FAST_FORMAT.unpack(data.read(66))
        assert (dec[0], dec[6], dec[12]) == _FAST_IDS
        return cls(
            Color(*dec[2:6]),
            Color(*dec[8:12]),
            Color(*dec[14:18]),
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xf9\xe0\xd0\xfb')  # 0xf9e0d0fb
        data.write(b'\x00\x10')  # size
        self.text_gradient_start_color.to_stream(data)

        data.write(b'\xe0A~\x89')  # 0xe0417e89
        data.write(b'\x00\x10')  # size
        self.text_gradient_end_color.to_stream(data)

        data.write(b'\xf2\xe15\x06')  # 0xf2e13506
        data.write(b'\x00\x10')  # size
        self.text_outline_color.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct26Json", data)
        return cls(
            text_gradient_start_color=Color.from_json(json_data['text_gradient_start_color']),
            text_gradient_end_color=Color.from_json(json_data['text_gradient_end_color']),
            text_outline_color=Color.from_json(json_data['text_outline_color']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'text_gradient_start_color': self.text_gradient_start_color.to_json(),
            'text_gradient_end_color': self.text_gradient_end_color.to_json(),
            'text_outline_color': self.text_outline_color.to_json(),
        }


def _decode_text_gradient_start_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_gradient_end_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


def _decode_text_outline_color(data: typing.BinaryIO, property_size: int):
    return Color.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xf9e0d0fb: ('text_gradient_start_color', _decode_text_gradient_start_color),
    0xe0417e89: ('text_gradient_end_color', _decode_text_gradient_end_color),
    0xf2e13506: ('text_outline_color', _decode_text_outline_color),
}
