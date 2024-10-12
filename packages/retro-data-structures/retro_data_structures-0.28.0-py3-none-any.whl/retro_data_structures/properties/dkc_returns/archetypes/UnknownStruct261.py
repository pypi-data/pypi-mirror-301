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
from retro_data_structures.properties.dkc_returns.archetypes.RobotChickenFlyerStructB import RobotChickenFlyerStructB

if typing.TYPE_CHECKING:
    class UnknownStruct261Json(typing_extensions.TypedDict):
        attack_selector: int
        health: float
        robot_chicken_flyer_struct_b_0x002cfe87: json_util.JsonObject
        robot_chicken_flyer_struct_b_0x76c9c7ba: json_util.JsonObject
        robot_chicken_flyer_struct_b_0xedba2d6e: json_util.JsonObject
        robot_chicken_flyer_struct_b_0x9b03b5c0: json_util.JsonObject
        robot_chicken_flyer_struct_b_0x00705f14: json_util.JsonObject
        robot_chicken_flyer_struct_b_0x76956629: json_util.JsonObject
        robot_chicken_flyer_struct_b_0xede68cfd: json_util.JsonObject
    

@dataclasses.dataclass()
class UnknownStruct261(BaseProperty):
    attack_selector: enums.RobotChickenEnum = dataclasses.field(default=enums.RobotChickenEnum.Unknown1, metadata={
        'reflection': FieldReflection[enums.RobotChickenEnum](
            enums.RobotChickenEnum, id=0x97d30f8b, original_name='AttackSelector', from_json=enums.RobotChickenEnum.from_json, to_json=enums.RobotChickenEnum.to_json
        ),
    })
    health: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf0668919, original_name='Health'
        ),
    })
    robot_chicken_flyer_struct_b_0x002cfe87: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructB](
            RobotChickenFlyerStructB, id=0x002cfe87, original_name='RobotChickenFlyerStructB', from_json=RobotChickenFlyerStructB.from_json, to_json=RobotChickenFlyerStructB.to_json
        ),
    })
    robot_chicken_flyer_struct_b_0x76c9c7ba: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructB](
            RobotChickenFlyerStructB, id=0x76c9c7ba, original_name='RobotChickenFlyerStructB', from_json=RobotChickenFlyerStructB.from_json, to_json=RobotChickenFlyerStructB.to_json
        ),
    })
    robot_chicken_flyer_struct_b_0xedba2d6e: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructB](
            RobotChickenFlyerStructB, id=0xedba2d6e, original_name='RobotChickenFlyerStructB', from_json=RobotChickenFlyerStructB.from_json, to_json=RobotChickenFlyerStructB.to_json
        ),
    })
    robot_chicken_flyer_struct_b_0x9b03b5c0: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructB](
            RobotChickenFlyerStructB, id=0x9b03b5c0, original_name='RobotChickenFlyerStructB', from_json=RobotChickenFlyerStructB.from_json, to_json=RobotChickenFlyerStructB.to_json
        ),
    })
    robot_chicken_flyer_struct_b_0x00705f14: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructB](
            RobotChickenFlyerStructB, id=0x00705f14, original_name='RobotChickenFlyerStructB', from_json=RobotChickenFlyerStructB.from_json, to_json=RobotChickenFlyerStructB.to_json
        ),
    })
    robot_chicken_flyer_struct_b_0x76956629: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructB](
            RobotChickenFlyerStructB, id=0x76956629, original_name='RobotChickenFlyerStructB', from_json=RobotChickenFlyerStructB.from_json, to_json=RobotChickenFlyerStructB.to_json
        ),
    })
    robot_chicken_flyer_struct_b_0xede68cfd: RobotChickenFlyerStructB = dataclasses.field(default_factory=RobotChickenFlyerStructB, metadata={
        'reflection': FieldReflection[RobotChickenFlyerStructB](
            RobotChickenFlyerStructB, id=0xede68cfd, original_name='RobotChickenFlyerStructB', from_json=RobotChickenFlyerStructB.from_json, to_json=RobotChickenFlyerStructB.to_json
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
        if property_count != 9:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x97d30f8b
        attack_selector = enums.RobotChickenEnum.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0668919
        health = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x002cfe87
        robot_chicken_flyer_struct_b_0x002cfe87 = RobotChickenFlyerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76c9c7ba
        robot_chicken_flyer_struct_b_0x76c9c7ba = RobotChickenFlyerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xedba2d6e
        robot_chicken_flyer_struct_b_0xedba2d6e = RobotChickenFlyerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9b03b5c0
        robot_chicken_flyer_struct_b_0x9b03b5c0 = RobotChickenFlyerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x00705f14
        robot_chicken_flyer_struct_b_0x00705f14 = RobotChickenFlyerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x76956629
        robot_chicken_flyer_struct_b_0x76956629 = RobotChickenFlyerStructB.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xede68cfd
        robot_chicken_flyer_struct_b_0xede68cfd = RobotChickenFlyerStructB.from_stream(data, property_size)
    
        return cls(attack_selector, health, robot_chicken_flyer_struct_b_0x002cfe87, robot_chicken_flyer_struct_b_0x76c9c7ba, robot_chicken_flyer_struct_b_0xedba2d6e, robot_chicken_flyer_struct_b_0x9b03b5c0, robot_chicken_flyer_struct_b_0x00705f14, robot_chicken_flyer_struct_b_0x76956629, robot_chicken_flyer_struct_b_0xede68cfd)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\t')  # 9 properties

        data.write(b'\x97\xd3\x0f\x8b')  # 0x97d30f8b
        data.write(b'\x00\x04')  # size
        self.attack_selector.to_stream(data)

        data.write(b'\xf0f\x89\x19')  # 0xf0668919
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.health))

        data.write(b'\x00,\xfe\x87')  # 0x2cfe87
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x002cfe87.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\xc9\xc7\xba')  # 0x76c9c7ba
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x76c9c7ba.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xba-n')  # 0xedba2d6e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0xedba2d6e.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x9b\x03\xb5\xc0')  # 0x9b03b5c0
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x9b03b5c0.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x00p_\x14')  # 0x705f14
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x00705f14.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'v\x95f)')  # 0x76956629
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0x76956629.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xed\xe6\x8c\xfd')  # 0xede68cfd
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.robot_chicken_flyer_struct_b_0xede68cfd.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("UnknownStruct261Json", data)
        return cls(
            attack_selector=enums.RobotChickenEnum.from_json(json_data['attack_selector']),
            health=json_data['health'],
            robot_chicken_flyer_struct_b_0x002cfe87=RobotChickenFlyerStructB.from_json(json_data['robot_chicken_flyer_struct_b_0x002cfe87']),
            robot_chicken_flyer_struct_b_0x76c9c7ba=RobotChickenFlyerStructB.from_json(json_data['robot_chicken_flyer_struct_b_0x76c9c7ba']),
            robot_chicken_flyer_struct_b_0xedba2d6e=RobotChickenFlyerStructB.from_json(json_data['robot_chicken_flyer_struct_b_0xedba2d6e']),
            robot_chicken_flyer_struct_b_0x9b03b5c0=RobotChickenFlyerStructB.from_json(json_data['robot_chicken_flyer_struct_b_0x9b03b5c0']),
            robot_chicken_flyer_struct_b_0x00705f14=RobotChickenFlyerStructB.from_json(json_data['robot_chicken_flyer_struct_b_0x00705f14']),
            robot_chicken_flyer_struct_b_0x76956629=RobotChickenFlyerStructB.from_json(json_data['robot_chicken_flyer_struct_b_0x76956629']),
            robot_chicken_flyer_struct_b_0xede68cfd=RobotChickenFlyerStructB.from_json(json_data['robot_chicken_flyer_struct_b_0xede68cfd']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'attack_selector': self.attack_selector.to_json(),
            'health': self.health,
            'robot_chicken_flyer_struct_b_0x002cfe87': self.robot_chicken_flyer_struct_b_0x002cfe87.to_json(),
            'robot_chicken_flyer_struct_b_0x76c9c7ba': self.robot_chicken_flyer_struct_b_0x76c9c7ba.to_json(),
            'robot_chicken_flyer_struct_b_0xedba2d6e': self.robot_chicken_flyer_struct_b_0xedba2d6e.to_json(),
            'robot_chicken_flyer_struct_b_0x9b03b5c0': self.robot_chicken_flyer_struct_b_0x9b03b5c0.to_json(),
            'robot_chicken_flyer_struct_b_0x00705f14': self.robot_chicken_flyer_struct_b_0x00705f14.to_json(),
            'robot_chicken_flyer_struct_b_0x76956629': self.robot_chicken_flyer_struct_b_0x76956629.to_json(),
            'robot_chicken_flyer_struct_b_0xede68cfd': self.robot_chicken_flyer_struct_b_0xede68cfd.to_json(),
        }


def _decode_attack_selector(data: typing.BinaryIO, property_size: int):
    return enums.RobotChickenEnum.from_stream(data)


def _decode_health(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x97d30f8b: ('attack_selector', _decode_attack_selector),
    0xf0668919: ('health', _decode_health),
    0x2cfe87: ('robot_chicken_flyer_struct_b_0x002cfe87', RobotChickenFlyerStructB.from_stream),
    0x76c9c7ba: ('robot_chicken_flyer_struct_b_0x76c9c7ba', RobotChickenFlyerStructB.from_stream),
    0xedba2d6e: ('robot_chicken_flyer_struct_b_0xedba2d6e', RobotChickenFlyerStructB.from_stream),
    0x9b03b5c0: ('robot_chicken_flyer_struct_b_0x9b03b5c0', RobotChickenFlyerStructB.from_stream),
    0x705f14: ('robot_chicken_flyer_struct_b_0x00705f14', RobotChickenFlyerStructB.from_stream),
    0x76956629: ('robot_chicken_flyer_struct_b_0x76956629', RobotChickenFlyerStructB.from_stream),
    0xede68cfd: ('robot_chicken_flyer_struct_b_0xede68cfd', RobotChickenFlyerStructB.from_stream),
}
