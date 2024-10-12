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
from retro_data_structures.properties.dkc_returns.archetypes.PickupRelayStruct import PickupRelayStruct

if typing.TYPE_CHECKING:
    class ProbabilityRelayJson(typing_extensions.TypedDict):
        editor_properties: json_util.JsonObject
        prob1_p: json_util.JsonObject
        prob2_p: json_util.JsonObject
        prob_time_attack: json_util.JsonObject
        prob_mirror_mode: json_util.JsonObject
    

@dataclasses.dataclass()
class ProbabilityRelay(BaseObjectType):
    editor_properties: EditorProperties = dataclasses.field(default_factory=EditorProperties, metadata={
        'reflection': FieldReflection[EditorProperties](
            EditorProperties, id=0x255a4580, original_name='EditorProperties', from_json=EditorProperties.from_json, to_json=EditorProperties.to_json
        ),
    })
    prob1_p: PickupRelayStruct = dataclasses.field(default_factory=PickupRelayStruct, metadata={
        'reflection': FieldReflection[PickupRelayStruct](
            PickupRelayStruct, id=0x18e3b4e9, original_name='Prob1P', from_json=PickupRelayStruct.from_json, to_json=PickupRelayStruct.to_json
        ),
    })
    prob2_p: PickupRelayStruct = dataclasses.field(default_factory=PickupRelayStruct, metadata={
        'reflection': FieldReflection[PickupRelayStruct](
            PickupRelayStruct, id=0x219b19a9, original_name='Prob2P', from_json=PickupRelayStruct.from_json, to_json=PickupRelayStruct.to_json
        ),
    })
    prob_time_attack: PickupRelayStruct = dataclasses.field(default_factory=PickupRelayStruct, metadata={
        'reflection': FieldReflection[PickupRelayStruct](
            PickupRelayStruct, id=0x121cb465, original_name='ProbTimeAttack', from_json=PickupRelayStruct.from_json, to_json=PickupRelayStruct.to_json
        ),
    })
    prob_mirror_mode: PickupRelayStruct = dataclasses.field(default_factory=PickupRelayStruct, metadata={
        'reflection': FieldReflection[PickupRelayStruct](
            PickupRelayStruct, id=0xffb7a5be, original_name='ProbMirrorMode', from_json=PickupRelayStruct.from_json, to_json=PickupRelayStruct.to_json
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
        return 'PRLA'

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
        assert property_id == 0x18e3b4e9
        prob1_p = PickupRelayStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x219b19a9
        prob2_p = PickupRelayStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x121cb465
        prob_time_attack = PickupRelayStruct.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xffb7a5be
        prob_mirror_mode = PickupRelayStruct.from_stream(data, property_size)
    
        return cls(editor_properties, prob1_p, prob2_p, prob_time_attack, prob_mirror_mode)

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

        data.write(b'\x18\xe3\xb4\xe9')  # 0x18e3b4e9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prob1_p.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'!\x9b\x19\xa9')  # 0x219b19a9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prob2_p.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x12\x1c\xb4e')  # 0x121cb465
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prob_time_attack.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xff\xb7\xa5\xbe')  # 0xffb7a5be
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.prob_mirror_mode.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        struct_end_offset = data.tell()
        data.seek(root_size_offset)
        data.write(struct.pack(">H", struct_end_offset - root_size_offset - 2))
        data.seek(struct_end_offset)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("ProbabilityRelayJson", data)
        return cls(
            editor_properties=EditorProperties.from_json(json_data['editor_properties']),
            prob1_p=PickupRelayStruct.from_json(json_data['prob1_p']),
            prob2_p=PickupRelayStruct.from_json(json_data['prob2_p']),
            prob_time_attack=PickupRelayStruct.from_json(json_data['prob_time_attack']),
            prob_mirror_mode=PickupRelayStruct.from_json(json_data['prob_mirror_mode']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'editor_properties': self.editor_properties.to_json(),
            'prob1_p': self.prob1_p.to_json(),
            'prob2_p': self.prob2_p.to_json(),
            'prob_time_attack': self.prob_time_attack.to_json(),
            'prob_mirror_mode': self.prob_mirror_mode.to_json(),
        }


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x255a4580: ('editor_properties', EditorProperties.from_stream),
    0x18e3b4e9: ('prob1_p', PickupRelayStruct.from_stream),
    0x219b19a9: ('prob2_p', PickupRelayStruct.from_stream),
    0x121cb465: ('prob_time_attack', PickupRelayStruct.from_stream),
    0xffb7a5be: ('prob_mirror_mode', PickupRelayStruct.from_stream),
}
