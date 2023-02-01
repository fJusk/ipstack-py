from typing import Iterable, Mapping, List

from requests.sessions import Session

from ipstackpy.core.base import BaseClient
from ipstackpy.core.exceptions import APIError

from ipstackpy.schema import StandardResponse


class IpStackClient(BaseClient):

    def __init__(
        self, 
        access_key: str, 
        session: Session = None, 
        base_url: str = None
    ) -> None:
        if session is None:
            session = Session()
        
        super().__init__(session, access_key, base_url)

    def __generate_endpoint(self, query: Iterable[str] | str) -> str:
        if isinstance(query, str):
            return f'/{query}'
        elif isinstance(query, list):
            return f"/{','.join(query)}"
        raise ValueError('Argument "query" must be instance of Iterable or str')

    def lookup(
        self, 
        ip_address: str,
        params: Mapping | dict = None,
        **kwargs
    ) -> StandardResponse:
        endpoint = self.__generate_endpoint(ip_address)
        data = self.get(endpoint, params=params, **kwargs)
        return StandardResponse(**data)

    def bulk_lookup(
        self,
        ip_addresses: List[str],
        params: Mapping | dict,
        **kwargs
    ) -> Iterable[StandardResponse]:
        endpoint = self.__generate_endpoint(ip_addresses)
        iterable_data = self.get(endpoint, params, **kwargs)
        return [StandardResponse(**data) for data in iterable_data]
