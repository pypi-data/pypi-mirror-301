import asyncio
import uuid
from contextlib import asynccontextmanager
from datetime import datetime

import pytz

from minemind import DEBUG_GAME_EVENTS, DEBUG_PROTOCOL
from minemind.client import Client
from minemind.dispatcher import EventDispatcher
from minemind.mc_types import UUID, Boolean, Double, Float, Long, Short, String, VarInt
from minemind.protocols.base import InteractionModule
from minemind.protocols.enums import ConnectionState, HandshakingNextState
from minemind.protocols.utils import get_logger
from minemind.protocols.v765.configuration import Configuration
from minemind.protocols.v765.entity import Entities, MCMath, Player, Vector3
from minemind.protocols.v765.game import Game
from minemind.protocols.v765.handshake import handshake
from minemind.protocols.v765.inbound.login import CompressResponse, LoginSuccessResponse
from minemind.protocols.v765.inbound.play import (
    CombatDeathResponse,
    DamageEventResponse,
    KeepAliveResponse,
    LoginResponse,
    PositionResponse,
    UpdateHealthResponse,
)
from minemind.protocols.v765.outbound.login import LoginAcknowledgedRequest, LoginStartRequest
from minemind.protocols.v765.outbound.play import (
    ArmAnimationRequest,
    ChatMessageRequest,
    ClientCommandRequest,
    HeldItemSlotRequest,
    InteractRequest,
    KeepAliveRequest,
    PositionLookRequest,
    PositionRequest,
    TeleportConfirmRequest,
)
from minemind.protocols.v765.physics import Physics
from minemind.protocols.v765.world import World


class OfflinePlayerNamespace:
    bytes = b'OfflinePlayer:'


class Bot(InteractionModule):
    logger = get_logger('Bot')

    def __init__(self, username: str = 'Bot', host: str = 'localhost', port: int = 25565, protocol_version: int = 765):
        self.client = Client(host, port, protocol_version)
        self.configuration = Configuration(self.client)

        self.username: str = username

        # TODO: Argument 1 to "uuid3" has incompatible type "type[OfflinePlayerNamespace]"; expected "UUID"  [arg-type]
        self.uuid: uuid.UUID = uuid.uuid3(OfflinePlayerNamespace, username)  # type: ignore[arg-type]
        self.entity_id: int | None = None

        self.dispatcher = EventDispatcher(self.client)

        self.world = World(self.client)
        self.entities = Entities(self.client)
        self.physics = Physics(self.client, self)
        self.game = Game(self.client)

    async def run_forever(self):
        async with self:
            try:
                while True:
                    await asyncio.sleep(1)
            except (KeyboardInterrupt, asyncio.CancelledError):
                self.logger.log(DEBUG_GAME_EVENTS, 'Bot stopped')

    async def __aenter__(self):
        await self.client.connect()
        self._dispatcher_task = asyncio.create_task(self.dispatcher.run_forever())
        await self.login()
        async with self.spawned():
            return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.disconnect()
        await self._dispatcher_task

    @property
    def entity(self) -> Player | None:
        if self.entity_id is None:
            return None
        return self.entities.get_by_id(self.entity_id)  # type: ignore[return-value]

    async def login(self) -> None:
        # TODO: currently only supports offline mode
        await handshake(self.client, HandshakingNextState.LOGIN)

        request = LoginStartRequest(String(self.username), UUID(self.uuid))
        await self.client.send_packet(request)

    async def login_acknowledged(self):
        await self.client.send_packet(LoginAcknowledgedRequest())
        self.client.state = ConnectionState.CONFIGURATION

    @EventDispatcher.subscribe(LoginSuccessResponse)
    async def _login_successful(self, data: LoginSuccessResponse):
        self.logger.log(DEBUG_GAME_EVENTS, f'User {data.username} logged in successfully!')
        await self.login_acknowledged()

    @EventDispatcher.subscribe(CompressResponse)
    async def _set_threshold(self, data: CompressResponse):
        self.logger.log(DEBUG_PROTOCOL, f'Compression activated. Threshold set to {data.threshold.int}')
        self.client.threshold = data.threshold.int

    async def respawn(self):
        await self.client.send_packet(ClientCommandRequest(VarInt(0x00)))  # Perform respawn
        self.logger.log(DEBUG_GAME_EVENTS, 'Respawning...')

    async def _set_player_position(self, x: Double, y: Double, z: Double, on_ground: bool = True):
        await self.client.send_packet(
            PositionRequest(
                x=x,
                y=y,
                z=z,
                on_ground=Boolean(on_ground),
            ),
        )
        self.logger.log(DEBUG_GAME_EVENTS, f'Moved to {x=} {y=} {z=}')

    async def set_position_and_look(self, position: Vector3, yaw: float, pitch: float, on_ground: bool = True):
        # probably it's better to save last_seen_position
        await self.client.send_packet(
            PositionLookRequest(
                x=Double(position.x),
                y=Double(position.y),
                z=Double(position.z),
                yaw=Float(yaw),
                pitch=Float(pitch),
                on_ground=Boolean(on_ground),
            ),
        )
        self.logger.log(DEBUG_GAME_EVENTS, f'Moved to {position=} {yaw=} {pitch=} {on_ground=}')

    @EventDispatcher.subscribe(PositionResponse)
    async def _synchronize_player_position(self, data: PositionResponse):
        if self.entity_id is None:
            self.logger.log(DEBUG_PROTOCOL, 'Entity id is not set. Skipping position synchronization.')
            return
        if self.username is None:
            self.logger.log(DEBUG_PROTOCOL, 'Username is not set. Skipping position synchronization.')
            return
        if self.uuid is None:
            self.logger.log(DEBUG_PROTOCOL, 'UUID is not set. Skipping position synchronization.')
            return
        entity = self.entities.get_by_id(self.entity_id)
        if entity is not None:
            velocity = entity.velocity
            position = entity.position
            yaw = entity.yaw
        else:
            velocity = Vector3(0, 0, 0)
            position = Vector3(0, 0, 0)
            yaw = 0

        # Velocity is only set to 0 if the flag is not set, otherwise keep current velocity
        new_velocity = Vector3(
            x=velocity.x if data.flags.int & data.Flag.X else 0,
            y=velocity.y if data.flags.int & data.Flag.Y else 0,
            z=velocity.z if data.flags.int & data.Flag.Z else 0,
        )

        # If flag is set, then the corresponding value is relative, else it is absolute
        new_position = Vector3(
            x=position.x + data.x.float if data.flags.int & data.Flag.X else data.x.float,
            y=position.y + data.y.float if data.flags.int & data.Flag.Y else data.y.float,
            z=position.z + data.z.float if data.flags.int & data.Flag.Z else data.z.float,
        )

        new_yaw = (MCMath.to_notchian_yaw(yaw) if data.flags.int & data.Flag.YAW else 0) + data.yaw.float
        new_pitch = (MCMath.to_notchian_pitch(yaw) if data.flags.int & data.Flag.PITCH else 0) + data.pitch.float

        if entity is None:
            self.entities.create_bot(
                player_uuid=self.uuid,
                entity_id=self.entity_id,
                username=self.username,
                velocity=new_velocity,
                position=new_position,
                yaw=MCMath.to_notchian_yaw_byte(new_yaw),
                pitch=MCMath.to_notchian_pitch_byte(new_pitch),
                on_ground=False,
            )
        else:
            entity.velocity = new_velocity
            entity.position = new_position
            entity.on_ground = False

            # TODO: Not sure why we use from_notchian_yaw/pitch instead of from_notchian_yaw/pitch_byte
            entity.yaw = MCMath.from_notchian_yaw(new_yaw)
            entity.pitch = MCMath.from_notchian_pitch(new_pitch)

            self.logger.log(
                DEBUG_PROTOCOL,
                f'Position synchronized. {new_position=} {new_yaw=} {new_pitch=}',
            )

        await self.client.send_packet(TeleportConfirmRequest(data.teleport_id))
        self.logger.log(
            DEBUG_PROTOCOL,
            f'Teleportation confirmed. {data.teleport_id=}',
        )

        await self.set_position_and_look(new_position, new_yaw, new_pitch, on_ground=False)

        # TODO: Respawn happens twice, on_death and here
        await self.respawn()

    @EventDispatcher.subscribe(KeepAliveResponse)
    async def _keep_alive(self, data: KeepAliveResponse):
        self.logger.log(DEBUG_PROTOCOL, f'Keep alive received: {data.keep_alive_id=}')
        await self.client.send_packet(KeepAliveRequest(data.keep_alive_id))

    @EventDispatcher.subscribe(LoginResponse)
    async def _start_playing(self, data: LoginResponse):
        self.entity_id = data.entity_id.int
        self.logger.log(DEBUG_PROTOCOL, f'Bot entity id: {self.entity_id=}')

    @EventDispatcher.subscribe(CombatDeathResponse)
    async def _death(self, data: CombatDeathResponse):
        if data.player_id.int == self.entity_id:
            self.logger.log(DEBUG_GAME_EVENTS, f'Bot died. Cause: {data.message}')
            await self.respawn()
        else:
            self.logger.log(
                DEBUG_GAME_EVENTS,
                f'Entity {self.entities.get_by_id(data.player_id.int)} died. Cause: {data.message}',
            )

    @EventDispatcher.subscribe(DamageEventResponse)
    async def _on_damage(self, data: DamageEventResponse):
        if data.entity_id.int == self.entity_id:
            self.logger.log(
                DEBUG_GAME_EVENTS,
                f'Bot received damage from {self.entities.get_by_id(data.source_cause_id.int)}',
            )
            if data.source_cause_id.int != -1:
                await self.attack(data.source_direct_id)
        else:
            self.logger.log(
                DEBUG_GAME_EVENTS,
                f'Entity {self.entities.get_by_id(data.entity_id.int)} received damage from {data.source_type_id}',
            )

    @EventDispatcher.subscribe(UpdateHealthResponse)
    async def _update_health(self, data: UpdateHealthResponse):
        if self.entity is None:
            self.logger.log(DEBUG_PROTOCOL, 'Entity is not set. Skipping health update.')
            return
        self.entity.health = data.health.float
        self.entity.food = data.food.int
        self.entity.saturation = data.food_saturation.float
        self.logger.log(
            DEBUG_GAME_EVENTS,
            f'Health: {self.entity.health}/20.0 Food: {self.entity.food}/20 Saturation: {self.entity.saturation}/5.0',
        )

    async def set_active_slot(self, slot: int):
        request = HeldItemSlotRequest(
            slot_id=Short(slot),
        )
        await self.client.send_packet(request)
        self.logger.log(DEBUG_GAME_EVENTS, f'Set active slot to {slot}')

    async def attack(self, entity_id: VarInt):
        request = InteractRequest(
            entity_id=entity_id,
            interact_type=InteractRequest.InteractType.ATTACK,
            sneaking=Boolean(False),
        )
        await self.client.send_packet(request)
        await self.client.send_packet(ArmAnimationRequest(ArmAnimationRequest.Hand.MAIN_HAND))
        self.logger.log(DEBUG_GAME_EVENTS, f'Attacking entity {self.entities.get_by_id(entity_id.int)}')

    async def chat_message(self, message: str):
        await self.client.send_packet(
            ChatMessageRequest(
                message=String(message),
                timestamp=Long(round(datetime.now(tz=pytz.UTC).timestamp())),
                message_count=VarInt(0),
            ),
        )
        self.logger.log(DEBUG_GAME_EVENTS, f'Sent chat message: {message}')

    @asynccontextmanager
    async def spawned(self):
        while not self.entity_id:
            await asyncio.sleep(0.000001)
        yield
