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
from retro_data_structures.properties.dkc_returns.archetypes.LocomotionContextEnum import LocomotionContextEnum
from retro_data_structures.properties.dkc_returns.archetypes.WanderRandomTurnData import WanderRandomTurnData

if typing.TYPE_CHECKING:
    class WanderBehaviorDataJson(typing_extensions.TypedDict):
        move_toward_nearest_player_on_init: bool
        seek_player: bool
        use_seek_activation_range: bool
        seek_activation_range_squared: float
        maintain_distance: bool
        desired_distance: float
        min_time_between_direction_changes: float
        ignore_tar_inhibited_players: bool
        minimum_seek_direction_time: float
        use_seeking_tarred_player_locomotion_context: bool
        use_platform_edge_as_bounds: bool
        seeking_tarred_player_locomotion_context: json_util.JsonObject
        enable_random_turn: bool
        random_turn: json_util.JsonObject
    

@dataclasses.dataclass()
class WanderBehaviorData(BaseProperty):
    move_toward_nearest_player_on_init: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x41832459, original_name='MoveTowardNearestPlayerOnInit'
        ),
    })
    seek_player: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x6cea0eba, original_name='SeekPlayer'
        ),
    })
    use_seek_activation_range: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x14d027b0, original_name='UseSeekActivationRange'
        ),
    })
    seek_activation_range_squared: float = dataclasses.field(default=0.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x9b8bec06, original_name='SeekActivationRangeSquared'
        ),
    })
    maintain_distance: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x009a1330, original_name='MaintainDistance'
        ),
    })
    desired_distance: float = dataclasses.field(default=7.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x60be35a1, original_name='DesiredDistance'
        ),
    })
    min_time_between_direction_changes: float = dataclasses.field(default=1.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0x8f5e7779, original_name='MinTimeBetweenDirectionChanges'
        ),
    })
    ignore_tar_inhibited_players: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x571855a7, original_name='IgnoreTarInhibitedPlayers'
        ),
    })
    minimum_seek_direction_time: float = dataclasses.field(default=3.0, metadata={
        'reflection': FieldReflection[float](
            float, id=0xe9e0beb6, original_name='MinimumSeekDirectionTime'
        ),
    })
    use_seeking_tarred_player_locomotion_context: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9aeb03d9, original_name='UseSeekingTarredPlayerLocomotionContext'
        ),
    })
    use_platform_edge_as_bounds: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x9a1287d4, original_name='UsePlatformEdgeAsBounds'
        ),
    })
    seeking_tarred_player_locomotion_context: LocomotionContextEnum = dataclasses.field(default_factory=LocomotionContextEnum, metadata={
        'reflection': FieldReflection[LocomotionContextEnum](
            LocomotionContextEnum, id=0x1296e316, original_name='SeekingTarredPlayerLocomotionContext', from_json=LocomotionContextEnum.from_json, to_json=LocomotionContextEnum.to_json
        ),
    })
    enable_random_turn: bool = dataclasses.field(default=False, metadata={
        'reflection': FieldReflection[bool](
            bool, id=0x938c651f, original_name='EnableRandomTurn'
        ),
    })
    random_turn: WanderRandomTurnData = dataclasses.field(default_factory=WanderRandomTurnData, metadata={
        'reflection': FieldReflection[WanderRandomTurnData](
            WanderRandomTurnData, id=0x6633877c, original_name='RandomTurn', from_json=WanderRandomTurnData.from_json, to_json=WanderRandomTurnData.to_json
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
        if property_count != 14:
            return None
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x41832459
        move_toward_nearest_player_on_init = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6cea0eba
        seek_player = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x14d027b0
        use_seek_activation_range = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9b8bec06
        seek_activation_range_squared = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x009a1330
        maintain_distance = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x60be35a1
        desired_distance = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x8f5e7779
        min_time_between_direction_changes = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x571855a7
        ignore_tar_inhibited_players = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0xe9e0beb6
        minimum_seek_direction_time = struct.unpack('>f', data.read(4))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9aeb03d9
        use_seeking_tarred_player_locomotion_context = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x9a1287d4
        use_platform_edge_as_bounds = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x1296e316
        seeking_tarred_player_locomotion_context = LocomotionContextEnum.from_stream(data, property_size)
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x938c651f
        enable_random_turn = struct.unpack('>?', data.read(1))[0]
    
        property_id, property_size = struct.unpack(">LH", data.read(6))
        assert property_id == 0x6633877c
        random_turn = WanderRandomTurnData.from_stream(data, property_size)
    
        return cls(move_toward_nearest_player_on_init, seek_player, use_seek_activation_range, seek_activation_range_squared, maintain_distance, desired_distance, min_time_between_direction_changes, ignore_tar_inhibited_players, minimum_seek_direction_time, use_seeking_tarred_player_locomotion_context, use_platform_edge_as_bounds, seeking_tarred_player_locomotion_context, enable_random_turn, random_turn)

    def to_stream(self, data: typing.BinaryIO, default_override: dict | None = None) -> None:
        default_override = default_override or {}
        data.write(b'\x00\x0e')  # 14 properties

        data.write(b'A\x83$Y')  # 0x41832459
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.move_toward_nearest_player_on_init))

        data.write(b'l\xea\x0e\xba')  # 0x6cea0eba
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.seek_player))

        data.write(b"\x14\xd0'\xb0")  # 0x14d027b0
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_seek_activation_range))

        data.write(b'\x9b\x8b\xec\x06')  # 0x9b8bec06
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.seek_activation_range_squared))

        data.write(b'\x00\x9a\x130')  # 0x9a1330
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.maintain_distance))

        data.write(b'`\xbe5\xa1')  # 0x60be35a1
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.desired_distance))

        data.write(b'\x8f^wy')  # 0x8f5e7779
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.min_time_between_direction_changes))

        data.write(b'W\x18U\xa7')  # 0x571855a7
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.ignore_tar_inhibited_players))

        data.write(b'\xe9\xe0\xbe\xb6')  # 0xe9e0beb6
        data.write(b'\x00\x04')  # size
        data.write(struct.pack('>f', self.minimum_seek_direction_time))

        data.write(b'\x9a\xeb\x03\xd9')  # 0x9aeb03d9
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_seeking_tarred_player_locomotion_context))

        data.write(b'\x9a\x12\x87\xd4')  # 0x9a1287d4
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.use_platform_edge_as_bounds))

        data.write(b'\x12\x96\xe3\x16')  # 0x1296e316
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.seeking_tarred_player_locomotion_context.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

        data.write(b'\x93\x8ce\x1f')  # 0x938c651f
        data.write(b'\x00\x01')  # size
        data.write(struct.pack('>?', self.enable_random_turn))

        data.write(b'f3\x87|')  # 0x6633877c
        before = data.tell()
        data.write(b'\x00\x00')  # size placeholder
        self.random_turn.to_stream(data)
        after = data.tell()
        data.seek(before)
        data.write(struct.pack(">H", after - before - 2))
        data.seek(after)

    @classmethod
    def from_json(cls, data: json_util.JsonValue) -> typing_extensions.Self:
        json_data = typing.cast("WanderBehaviorDataJson", data)
        return cls(
            move_toward_nearest_player_on_init=json_data['move_toward_nearest_player_on_init'],
            seek_player=json_data['seek_player'],
            use_seek_activation_range=json_data['use_seek_activation_range'],
            seek_activation_range_squared=json_data['seek_activation_range_squared'],
            maintain_distance=json_data['maintain_distance'],
            desired_distance=json_data['desired_distance'],
            min_time_between_direction_changes=json_data['min_time_between_direction_changes'],
            ignore_tar_inhibited_players=json_data['ignore_tar_inhibited_players'],
            minimum_seek_direction_time=json_data['minimum_seek_direction_time'],
            use_seeking_tarred_player_locomotion_context=json_data['use_seeking_tarred_player_locomotion_context'],
            use_platform_edge_as_bounds=json_data['use_platform_edge_as_bounds'],
            seeking_tarred_player_locomotion_context=LocomotionContextEnum.from_json(json_data['seeking_tarred_player_locomotion_context']),
            enable_random_turn=json_data['enable_random_turn'],
            random_turn=WanderRandomTurnData.from_json(json_data['random_turn']),
        )

    def to_json(self) -> json_util.JsonObject:
        return {
            'move_toward_nearest_player_on_init': self.move_toward_nearest_player_on_init,
            'seek_player': self.seek_player,
            'use_seek_activation_range': self.use_seek_activation_range,
            'seek_activation_range_squared': self.seek_activation_range_squared,
            'maintain_distance': self.maintain_distance,
            'desired_distance': self.desired_distance,
            'min_time_between_direction_changes': self.min_time_between_direction_changes,
            'ignore_tar_inhibited_players': self.ignore_tar_inhibited_players,
            'minimum_seek_direction_time': self.minimum_seek_direction_time,
            'use_seeking_tarred_player_locomotion_context': self.use_seeking_tarred_player_locomotion_context,
            'use_platform_edge_as_bounds': self.use_platform_edge_as_bounds,
            'seeking_tarred_player_locomotion_context': self.seeking_tarred_player_locomotion_context.to_json(),
            'enable_random_turn': self.enable_random_turn,
            'random_turn': self.random_turn.to_json(),
        }


def _decode_move_toward_nearest_player_on_init(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_seek_player(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_seek_activation_range(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_seek_activation_range_squared(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_maintain_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_desired_distance(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_min_time_between_direction_changes(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_ignore_tar_inhibited_players(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_minimum_seek_direction_time(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>f', data.read(4))[0]


def _decode_use_seeking_tarred_player_locomotion_context(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_use_platform_edge_as_bounds(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


def _decode_enable_random_turn(data: typing.BinaryIO, property_size: int):
    return struct.unpack('>?', data.read(1))[0]


_property_decoder: typing.Dict[int, typing.Tuple[str, typing.Callable[[typing.BinaryIO, int], typing.Any]]] = {
    0x41832459: ('move_toward_nearest_player_on_init', _decode_move_toward_nearest_player_on_init),
    0x6cea0eba: ('seek_player', _decode_seek_player),
    0x14d027b0: ('use_seek_activation_range', _decode_use_seek_activation_range),
    0x9b8bec06: ('seek_activation_range_squared', _decode_seek_activation_range_squared),
    0x9a1330: ('maintain_distance', _decode_maintain_distance),
    0x60be35a1: ('desired_distance', _decode_desired_distance),
    0x8f5e7779: ('min_time_between_direction_changes', _decode_min_time_between_direction_changes),
    0x571855a7: ('ignore_tar_inhibited_players', _decode_ignore_tar_inhibited_players),
    0xe9e0beb6: ('minimum_seek_direction_time', _decode_minimum_seek_direction_time),
    0x9aeb03d9: ('use_seeking_tarred_player_locomotion_context', _decode_use_seeking_tarred_player_locomotion_context),
    0x9a1287d4: ('use_platform_edge_as_bounds', _decode_use_platform_edge_as_bounds),
    0x1296e316: ('seeking_tarred_player_locomotion_context', LocomotionContextEnum.from_stream),
    0x938c651f: ('enable_random_turn', _decode_enable_random_turn),
    0x6633877c: ('random_turn', WanderRandomTurnData.from_stream),
}
