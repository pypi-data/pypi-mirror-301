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
from retro_data_structures.properties.dkc_returns.archetypes.LocomotionContextEnum import LocomotionContextEnum
from retro_data_structures.properties.dkc_returns.archetypes.TrackPlayer import TrackPlayer
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct10 import UnknownStruct10
from retro_data_structures.properties.dkc_returns.archetypes.UnknownStruct9 import UnknownStruct9

if typing.TYPE_CHECKING:
    class AnimGridModifierDataJson(typing_extensions.TypedDict):
        unknown: int
        enabled_by_default: bool
        mirror_when_facing_left: bool
        enable_interval_timer: bool
        minimum_interval_time: float
        maximum_interval_time: float
        override_locomotion_context_during_interval: bool
        unknown_struct3: json_util.JsonObject
        looping: int
        logic_type: int
        unknown_struct9: json_util.JsonObject
        track_player: json_util.JsonObject
        unknown_struct10: json_util.JsonObject
    

@dataclasses.dataclass()
class AnimGridModifierData(BaseProperty):
    unknown: int = dataclasses.field(default=0, metadata={
        'reflection': FieldReflection[int](
            int, id=0xa1266897, original_name='Unknown'
        ),
    })
    enabled_by_default: bool = dataclasses.field(default=True, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x7be67947, original_name='EnabledByDefault'
        ),
    })
    mirror_when_facing_left: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6ef66faa, original_name='MirrorWhenFacingLeft'
        ),
    })
    enable_interval_timer: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x4432ccd6, original_name='EnableIntervalTimer'
        ),
    })
    minimum_interval_time: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xf0cc73c9, original_name='MinimumIntervalTime'
        ),
    })
    maximum_interval_time: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x2b73202e, original_name='MaximumIntervalTime'
        ),
    })
    override_locomotion_context_during_interval: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0xcfc6720e, original_name='OverrideLocomotionContextDuringInterval'
        ),
    })
    unknown_struct3: LocomotionContextEnum = dataclasses.field(default_factory=LocomotionContextEnum, metadata={
        'reflection': FieldReflection[LocomotionContextEnum](
            LocomotionContextEnum, id=0x900fb99c, original_name='UnknownStruct3', from_json=LocomotionContextEnum.from_json, to_json=LocomotionContextEnum.to_json
        ),
    })
    looping: enums.Looping = dataclasses.field(default=enums.Looping.Unknown1, metadata={
        'reflection': FieldReflection[enums.Looping](
            enums.Looping, id=0x6f74f82f, original_name='Looping', from_json=enums.Looping.from_json, to_json=enums.Looping.to_json
        ),
    })
    logic_type: enums.LogicType = dataclasses.field(default=enums.LogicType.Unknown1, metadata={
        'reflection': FieldReflection[enums.LogicType](
            enums.LogicType, id=0x611f9f41, original_name='LogicType', from_json=enums.LogicType.from_json, to_json=enums.LogicType.to_json
        ),
    })
    unknown_struct9: UnknownStruct9 = dataclasses.field(default_factory=UnknownStruct9, metadata={
        'reflection': FieldReflection[UnknownStruct9](
            UnknownStruct9, id=0x42a7922c, original_name='UnknownStruct9', from_json=UnknownStruct9.from_json, to_json=UnknownStruct9.to_json
        ),
    })
    track_player: TrackPlayer = dataclasses.field(default_factory=TrackPlayer, metadata={
        'reflection': FieldReflection[TrackPlayer](
            TrackPlayer, id=0xe67ef99e, original_name='TrackPlayer', from_json=TrackPlayer.from_json, to_json=TrackPlayer.to_json
        ),
    })
    unknown_struct10: UnknownStruct10 = dataclasses.field(default_factory=UnknownStruct10, metadata={
        'reflection': FieldReflection[UnknownStruct10](
            UnknownStruct10, id=0x7873efd9, original_name='UnknownStruct10', from_json=UnknownStruct10.from_json, to_json=UnknownStruct10.to_json
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
        assert property_id == 0xa1266897
        unknown = struct.unpack('>l', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7be67947
        enabled_by_default = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6ef66faa
        mirror_when_facing_left = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x4432ccd6
        enable_interval_timer = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xf0cc73c9
        minimum_interval_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x2b73202e
        maximum_interval_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xcfc6720e
        override_locomotion_context_during_interval = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x900fb99c
        unknown_struct3 = LocomotionContextEnum.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6f74f82f
        looping = enums.Looping.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x611f9f41
        logic_type = enums.LogicType.from_stream(data)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x42a7922c
        unknown_struct9 = UnknownStruct9.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe67ef99e
        track_player = TrackPlayer.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x7873efd9
        unknown_struct10 = UnknownStruct10.from_stream(data, property_size)
    
        return cls(unknown, enabled_by_default, mirror_when_facing_left, enable_interval_timer, minimum_interval_time, maximum_interval_time, override_locomotion_context_during_interval, unknown_struct3, looping, logic_type, unknown_struct9, track_player, unknown_struct10)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\r')  # 13 properties

        data.write(b'\xa1&h\x97')  # 0xa1266897
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>l', self.unknown))

        data.write(b'{\xe6yG')  # 0x7be67947
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enabled_by_default))

        data.write(b'n\xf6o\xaa')  # 0x6ef66faa
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.mirror_when_facing_left))

        data.write(b'D2\xcc\xd6')  # 0x4432ccd6
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_interval_timer))

        data.write(b'\xf0\xccs\xc9')  # 0xf0cc73c9
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_interval_time))

        data.write(b'+s .')  # 0x2b73202e
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.maximum_interval_time))

        data.write(b'\xcf\xc6r\x0e')  # 0xcfc6720e
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.override_locomotion_context_during_interval))

        data.write(b'\x90\x0f\xb9\x9c')  # 0x900fb99c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct3.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'ot\xf8/')  # 0x6f74f82f
        data.write(b'\x00\x04')  # size
        self.looping.to_stream(data)

        data.write(b'a\x1f\x9fA')  # 0x611f9f41
        data.write(b'\x00\x04')  # size
        self.logic_type.to_stream(data)

        data.write(b'B\xa7\x92,')  # 0x42a7922c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct9.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\xe6~\xf9\x9e')  # 0xe67ef99e
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.track_player.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'xs\xef\xd9')  # 0x7873efd9
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.unknown_struct10.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("AnimGridModifierDataJson", data)
        return cls(
            unknown=json_data['unknown'],
            enabled_by_default=json_data['enabled_by_default'],
            mirror_when_facing_left=json_data['mirror_when_facing_left'],
            enable_interval_timer=json_data['enable_interval_timer'],
            minimum_interval_time=json_data['minimum_interval_time'],
            maximum_interval_time=json_data['maximum_interval_time'],
            override_locomotion_context_during_interval=json_data['override_locomotion_context_during_interval'],
            unknown_struct3=LocomotionContextEnum.from_json(json_data['unknown_struct3']),
            looping=enums.Looping.from_json(json_data['looping']),
            logic_type=enums.LogicType.from_json(json_data['logic_type']),
            unknown_struct9=UnknownStruct9.from_json(json_data['unknown_struct9']),
            track_player=TrackPlayer.from_json(json_data['track_player']),
            unknown_struct10=UnknownStruct10.from_json(json_data['unknown_struct10']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'unknown': self.unknown,
            'enabled_by_default': self.enabled_by_default,
            'mirror_when_facing_left': self.mirror_when_facing_left,
            'enable_interval_timer': self.enable_interval_timer,
            'minimum_interval_time': self.minimum_interval_time,
            'maximum_interval_time': self.maximum_interval_time,
            'override_locomotion_context_during_interval': self.override_locomotion_context_during_interval,
            'unknown_struct3': self.unknown_struct3.to_json(),
            'looping': self.looping.to_json(),
            'logic_type': self.logic_type.to_json(),
            'unknown_struct9': self.unknown_struct9.to_json(),
            'track_player': self.track_player.to_json(),
            'unknown_struct10': self.unknown_struct10.to_json(),
        }


def _decode_unknown(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>l', data.read(4))[0]


def _decode_enabled_by_default(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_mirror_when_facing_left(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_interval_timer(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_interval_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maximum_interval_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_override_locomotion_context_during_interval(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_looping(data: typing.BinaryIO, property_size: int):
    return enums.Looping.from_stream(data)


def _decode_logic_type(data: typing.BinaryIO, property_size: int):
    return enums.LogicType.from_stream(data)


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0xa1266897: ('unknown', _decode_unknown),
    0x7be67947: ('enabled_by_default', _decode_enabled_by_default),
    0x6ef66faa: ('mirror_when_facing_left', _decode_mirror_when_facing_left),
    0x4432ccd6: ('enable_interval_timer', _decode_enable_interval_timer),
    0xf0cc73c9: ('minimum_interval_time', _decode_minimum_interval_time),
    0x2b73202e: ('maximum_interval_time', _decode_maximum_interval_time),
    0xcfc6720e: ('override_locomotion_context_during_interval', _decode_override_locomotion_context_during_interval),
    0x900fb99c: ('unknown_struct3', LocomotionContextEnum.from_stream),
    0x6f74f82f: ('looping', _decode_looping),
    0x611f9f41: ('logic_type', _decode_logic_type),
    0x42a7922c: ('unknown_struct9', UnknownStruct9.from_stream),
    0xe67ef99e: ('track_player', TrackPlayer.from_stream),
    0x7873efd9: ('unknown_struct10', UnknownStruct10.from_stream),
}
