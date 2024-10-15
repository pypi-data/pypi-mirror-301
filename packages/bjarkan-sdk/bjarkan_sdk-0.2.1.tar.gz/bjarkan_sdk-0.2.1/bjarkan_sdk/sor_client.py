from .base_client import BaseClient
from typing import Dict, List


class BjarkanSORClient(BaseClient):
    def __init__(self, base_url: str = 'https://api.bjarkan.io'):
        super().__init__(base_url)

    def set_orderbook_config(self, config: Dict) -> Dict:
        return self._make_request('POST', 'orderbook_config/set', json=config)

    def get_orderbook_config(self) -> Dict:
        return self._make_request('GET', 'orderbook_config/get')

    def set_trades_config(self, config: Dict) -> Dict:
        return self._make_request('POST', 'trades_config/set', json=config)

    def get_trades_config(self) -> Dict:
        return self._make_request('GET', 'trades_config/get')

    def set_api_keys(self, api_configs: List[Dict]) -> Dict:
        return self._make_request('POST', 'api_keys/set', json=api_configs)

    def get_api_keys(self) -> Dict:
        return self._make_request('GET', 'api_keys/get')

    def get_latest_orderbook(self) -> Dict:
        return self._make_request('GET', 'get_latest_orderbook')

    def execute_order(self, order: Dict) -> Dict:
        return self._make_request('POST', 'execute_order', json=order)

    def get_balances(self) -> Dict:
        return self._make_request('GET', 'get_balances')
