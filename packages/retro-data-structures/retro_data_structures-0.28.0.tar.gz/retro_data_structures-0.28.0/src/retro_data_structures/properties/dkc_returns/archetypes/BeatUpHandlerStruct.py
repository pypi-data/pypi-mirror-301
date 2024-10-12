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
    class BeatUpHandlerStructJson(typing_extensions.TypedDict):
        item: int
        num_awarded: int
        chance: float
    

_FAST_FORMAT = None
_FAST_IDS = (0xb3e3e1e3, 0x8fa67c9e, 0x7a7b330e)


@dataclasses.dataclass()
class BeatUpHandlerStruct(BaseProperty):
    item: enums.PlayerItem = dataclasses.field(default=enums.PlayerItem.Banana, metadata={
        'reflection': FieldReflection[enums.PlayerItem](
            enums.PlayerItem, id=0xb3e3e1e3, original_name='Item', from_json=enums.PlayerItem.from_json, to_json=enums.PlayerItem.to_json
        ),
    })
    num_awarded: int = dataclasses.field(default=1, metadata={
        'reflection': FieldReflection[int](
            int, id=0x8fa67c9e, original_name='NumAwarded'
        ),
    })
    chance: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x7a7b330e, original_name='Chance'
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
            _FAST_FORMAT = struct.Struct('>LHLLHlLHf')
    
        dec = _FAST_FORMAT.unpack(data.read(30))
        assert (dec[0], dec[3], dec[6]) == _FAST_IDS
        return cls(
            enums.PlayerItem(dec[2]),
            dec[5],
            dec[8],
        )

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x03')  # 3 properties

        data.write(b'\xb3\xe3\xe1\xe3')  # 0xb3e3e1e3
        data.write(b'\x00\x04')  # size
        self.item.to_stream(data)

        data.write(b'\x8f\xa6|\x9e')  # 0x8fa67c9e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.num_awarded))

        data.write(b'z{3\x0e')  # 0x7a7b330e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.chance))

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("BeatUpHandlerStructJson", data)
        return cls(
            item=enums.PlayerItem.from_json(json_data['item']),
            num_awarded=json_data['num_awarded'],
            chance=json_data['chance'],
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'item': self.item.to_json(),
            'num_awarded': self.num_awarded,
            'chance': self.chance,
        }


def _decode_item(data: typing.BinaryIO, property_size: int):
    return enums.PlayerItem.from_stream(data)


def _decode_num_awarded(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_chance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xb3e3e1e3: ('item', _decode_item),
    0x8fa67c9e: ('num_awarded', _decode_num_awarded),
    0x7a7b330e: ('chance', _decode_chance),
}
