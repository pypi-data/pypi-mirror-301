from minemind import DEBUG_PROTOCOL
from minemind.client import Client
from minemind.dispatcher import EventDispatcher
from minemind.protocols.base import InteractionModule
from minemind.protocols.enums import ConnectionState
from minemind.protocols.utils import get_logger
from minemind.protocols.v765.inbound.configuration import (
    FeatureFlagResponse,
    FinishConfigurationResponse,
    PluginMessageResponse,
    RegistryDataResponse,
    UpdateTagsResponse,
)
from minemind.protocols.v765.outbound.configuration import FinishConfigurationRequest


class Configuration(InteractionModule):
    logger = get_logger('Configuration')

    def __init__(self, client: Client):
        self.client = client

    @EventDispatcher.subscribe(PluginMessageResponse)
    async def _plugin_message(self, data: PluginMessageResponse):
        self.logger.log(DEBUG_PROTOCOL, 'Received plugin message')

    @EventDispatcher.subscribe(FeatureFlagResponse)
    async def _feature_flag(self, data: FeatureFlagResponse):
        self.logger.log(DEBUG_PROTOCOL, 'Received feature flag')

    @EventDispatcher.subscribe(RegistryDataResponse)
    async def _registry_data(self, data: RegistryDataResponse):
        self.logger.log(DEBUG_PROTOCOL, 'Received registry data')
        # TODO: Important to save this data for later use
        # dimension_name = data[minecraft:dimension_type][*][name]
        # min_y = data[minecraft:dimension_type][*][name][min_y]
        # height = data[minecraft:dimension_type][*][name][height]
        # print(f'Registry data {len(data.registry_codec)=} bytes')

    @EventDispatcher.subscribe(UpdateTagsResponse)
    async def _update_tags(self, data: UpdateTagsResponse):
        self.logger.log(DEBUG_PROTOCOL, 'Received tags update')

    @EventDispatcher.subscribe(FinishConfigurationResponse)
    async def _finish_configuration(self, data: FinishConfigurationResponse):
        await self.client.send_packet(FinishConfigurationRequest())
        self.client.state = ConnectionState.PLAY
        self.logger.log(DEBUG_PROTOCOL, 'Configuration finished. Switching to PLAY state')
