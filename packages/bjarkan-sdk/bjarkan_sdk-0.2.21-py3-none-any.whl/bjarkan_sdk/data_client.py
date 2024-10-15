from .base_client import BaseClient
from typing import Dict, List, Optional, Iterator
from datetime import datetime


class BjarkanDataClient(BaseClient):
    def __init__(self, base_url: str = 'https://data.bjarkan.io'):
        super().__init__(base_url)

    def get_tables(self) -> List[Dict[str, any]]:
        return self._make_request('GET', 'tables')

    def get_history(self,
                    table_name: str,
                    start_time: datetime,
                    end_time: datetime,
                    exchange: Optional[str] = None,
                    symbol: Optional[str] = None,
                    use_exchange_time: Optional[bool] = False,
                    sort_descending: bool = False,
                    bucket_period: Optional[str] = None,
                    limit: Optional[int] = None,
                    offset: Optional[int] = None) -> Dict[str, any]:
        data = {
            "table_name": table_name,
            "start_time": int(start_time.timestamp()),
            "end_time": int(end_time.timestamp()),
            "exchange": exchange,
            "symbol": symbol,
            "use_exchange_time": use_exchange_time,
            "sort_descending": sort_descending,
            "bucket_period": bucket_period,
            "limit": limit,
            "offset": offset
        }
        return self._make_request('POST', 'history', json=data)

    def get_paginated_history(self,
                              table_name: str,
                              start_time: datetime,
                              end_time: datetime,
                              exchange: Optional[str] = None,
                              symbol: Optional[str] = None,
                              use_exchange_time: Optional[bool] = False,
                              sort_descending: bool = False,
                              bucket_period: Optional[str] = None,
                              page_size: int = 1000) -> Iterator[Dict[str, any]]:
        offset = 0
        while True:
            result = self.get_history(
                table_name=table_name,
                start_time=start_time,
                end_time=end_time,
                exchange=exchange,
                symbol=symbol,
                use_exchange_time=use_exchange_time,
                sort_descending=sort_descending,
                bucket_period=bucket_period,
                limit=page_size,
                offset=offset
            )
            yield result
            if len(result['data']) < page_size:
                break
            offset += page_size

    @staticmethod
    def validate_bucket_period(bucket_period: str) -> bool:
        valid_periods = ['100ms', '1s', '30s', '1 minute', '5 minutes', '15 minutes', '30 minutes', '1 hour']
        return bucket_period in valid_periods
