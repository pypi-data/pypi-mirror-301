import asyncio
import websockets
import json
from .base_client import BaseClient
from .models import OrderbookConfig, TradesConfig, OrderConfig, APIConfig
from typing import Dict, List, AsyncIterator


class BjarkanSORClient(BaseClient):
    def __init__(self, base_url: str = 'https://api.bjarkan.io'):
        super().__init__(base_url)
        self.ws_base_url = f"ws://{base_url.split('://')[1]}"

    def set_orderbook_config(self, config: OrderbookConfig) -> Dict:
        return self._make_request('POST', 'orderbook_config/set', json=config.dict())

    def get_orderbook_config(self) -> OrderbookConfig:
        data = self._make_request('GET', 'orderbook_config/get')
        return OrderbookConfig(**data)

    def set_trades_config(self, config: TradesConfig) -> Dict:
        return self._make_request('POST', 'trades_config/set', json=config.dict())

    def get_trades_config(self) -> TradesConfig:
        data = self._make_request('GET', 'trades_config/get')
        return TradesConfig(**data)

    def set_api_keys(self, api_configs: List[APIConfig]) -> Dict:
        return self._make_request('POST', 'api_keys/set', json=[config.dict() for config in api_configs])

    def get_api_keys(self) -> List[APIConfig]:
        data = self._make_request('GET', 'api_keys/get')
        return [APIConfig(**config) for config in data]

    def get_latest_orderbook(self) -> Dict:
        return self._make_request('GET', 'get_latest_orderbook')

    def execute_order(self, order: OrderConfig) -> Dict:
        return self._make_request('POST', 'execute_order', json=order.dict())

    def get_balances(self) -> Dict:
        return self._make_request('GET', 'get_balances')

    async def stream_orderbook(self) -> AsyncIterator[Dict]:
        uri = f"{self.ws_base_url}/stream_orderbook?token={self.token}"
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    yield json.loads(message)
                except websockets.exceptions.ConnectionClosed:
                    break

    async def stream_trades(self) -> AsyncIterator[Dict]:
        uri = f"{self.ws_base_url}/stream_trades?token={self.token}"
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    yield json.loads(message)
                except websockets.exceptions.ConnectionClosed:
                    break
