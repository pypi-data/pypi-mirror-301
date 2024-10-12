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
from retro_data_structures.properties.dkc_returns.core.Spline import Spline

if typing.TYPE_CHECKING:
    class UnknownStruct65Json(typing_extensions.TypedDict):
        unknown: json_util.JsonObject
        effect_mode: int
    

@dataclasses.dataclass()
class UnknownStruct65(BaseProperty):
    unknown: Spline = dataclasses.field(default_factory=Spline, metadata={
        'reflection': FieldReflection[Spline](
            Spline, id=0xdcbfa4e6, original_name='Unknown', from_json=Spline.from_json, to_json=Spline.to_json
        ),
    })
    effect_mode: enums.EffectMode = dataclasses.field(default=enums.EffectMode.Unknown1, metadata={
        'reflection': FieldReflection[enums.EffectMode](
            enums.EffectMode, id=0x1610eb13, original_name='EffectMode', from_json=enums.EffectMode.from_json, to_json=enums.EffectMode.to_json
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
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xdcbfa4e6
        unknown = Spline.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1610eb13
        effect_mode = enums.EffectMode.from_stream(data)
    
        return cls(unknown, effect_mode)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x02')  # 2 properties

        data.write(b'\xdc\xbf\xa4\xe6')  # 0xdcbfa4e6
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x16\x10\xeb\x13')  # 0x1610eb13
        data.write(b'\x00\x04')  # size
        self.effect_mode.to_stream(data)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct65Json", data)
        return cls(
            unknown=Spline.from_json(json_data['unknown']),
            effect_mode=enums.EffectMode.from_json(json_data['effect_mode']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown.to_json(),
            'effect_mode': self.effect_mode.to_json(),
        }


def _decode_effect_mode(data: typing.BinaryIO, property_size: int):
    return enums.EffectMode.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xdcbfa4e6: ('unknown', Spline.from_stream),
    0x1610eb13: ('effect_mode', _decode_effect_mode),
}
