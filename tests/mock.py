import json

from typing import Iterable

from responses import Response, matchers
from pydantic import BaseModel


DEFAULT_METHOD = 'GET'
DEFAULT_STATUS = 200
DEFAULT_BODY = '{"test_key": "test_value"}'
DEFAULT_CONTENT_TYPE = 'application/json'


class MockGenerator:
    
    def __init__(self) -> None:
        pass

    def __get_body(self, model: BaseModel) -> str:
        pass

    def get_response(self, **kwargs) -> Response:
        
        if 'model' in kwargs:
            model = kwargs['model']
            assert isinstance(model, BaseModel)
            
            body = self.__get_body(model)

        elif 'body' in kwargs:
            body = kwargs['body']

        else:
            body = DEFAULT_BODY

        try:
            url = kwargs['url']
        except KeyError:
            raise ValueError('Arg "url" must be include in kwargs')

        status = kwargs.get('status', DEFAULT_STATUS)
        method = kwargs.get('method', DEFAULT_METHOD)
        content_type = kwargs.get('content_type', DEFAULT_CONTENT_TYPE)
        matches: Iterable = kwargs.get('matches', None)

        response = Response(
            method=method,
            status=status,
            url=url,
            body=body,
            content_type=content_type,
            match=matches
        )

        return response