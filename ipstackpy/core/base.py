import json
import logging

from requests import Response
from requests.sessions import Session
from requests.exceptions import HTTPError

from typing import Mapping, Any

from .exceptions import MethodNotAllowed, APIError


class BaseClient:

    allow_methods = ['GET']
    base_url = 'http://api.ipstack.com' 

    def __init__(
        self,
        session: Session,
        access_key: str,
        base_url: str = None,
        ) -> None:
        assert isinstance(session, Session), 'Argument session must be instance of request.Session'
        
        self._session = session
        self._access_key = access_key

        if base_url:
            self.base_url = base_url

    @property
    def session(self) -> Session:
        return self._session
    
    @property
    def access_key(self) -> str:
        return self._access_key
    
    def __isallow_method(self, method: str) -> bool:
        """Checks if the request method is allowed."""
        return method.upper() in self.allow_methods
    
    def __issuccess(self, response_data: dict) -> bool:
        """Cheks if the request is sucess"""
        return response_data.get('success', True)
    
    def __retry_request(
        self, 
        method: str, 
        url: str, 
        params: Mapping, 
        **kwargs
    ) -> Response | Any:
        """
        The method implements a retry of the request, but calls "request" method 
        with "force" argument set to True, and only raises exception if status code 
        is not within the range between 200 and 300.
        """
        response = self.request(method, url, force=True, params=params, **kwargs)
        if 200 <= response.status_code < 300:
            return response

        logging.error(f"Failed retry request to server.")
        logging.info(f"[{response.status_code}] | {response.text}")
        raise HTTPError("Unable connect to server.")
    
    def request(
        self,
        method: str, 
        url: str,
        force: bool = False,
        params: Mapping = None,
        **kwargs
    ) -> dict | Response | Any:
        """
        This method implements a request to API that takes "method", "url", and "params" as kwargs. 
        It then checks the response status and retries the request if necessary. Upon successful response,
        it returns the data. If a bad response is received, it raises an error.
        """
        params = params if params else dict()
        if not self.__isallow_method(method) and not force:
            err_text = f'Method: {method} not allowed.\nAllow methods: {",".join(self.allow_methods)}'
            logging.error(err_text)
            raise MethodNotAllowed(err_text)
        
        params['access_key'] = self.access_key
        response = self._session.request(method, url, params=params, **kwargs)

        if force:
            return response
        
        if 500 <= response.status_code < 600:
            logging.warning(f'Bad response from server. Retry request to {url}')
            response = self.__retry_request(method, url, params)
        
        try:
            body = response.json()
            if self.__issuccess(body):
                return body
            
            try:
                error = body['error']
                code = error['code']
                message = error['info']

            except KeyError:
                logging.error('Cant get values from dict')
                code = response.status_code
                message = response.text
        except json.JSONDecodeError:
            logging.error('Cant decode json')
            code = response.status_code
            message = response.text
            
        logging.error(f'Failed request to {url}')
        logging.error(f'Response: [{code}] | {message}')
        raise APIError(f'Response: [{code}] | {message}')

    def get(self, endpoint: str, params: Mapping = None, **kwargs) -> dict:
        """ GET request by endpoint. """
        method = 'GET'
        url = self.base_url + endpoint
        return self.request(method, url, params, **kwargs)
    
    def close(self) -> None:
        self._session.close()
