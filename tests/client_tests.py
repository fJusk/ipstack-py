import json
import requests
import responses

from unittest.case import TestCase
from responses import matchers

from ipstackpy.core import BaseClient

from .mock import MockGenerator, DEFAULT_BODY


class BaseClientTest(TestCase):

    token = '8743r8dew:4398:fed3efwewf9843j3f9jru49r'

    def setUp(self) -> None:
        self.session = requests.Session()
        self.generator = MockGenerator()
        self.client = BaseClient(session=self.session, access_key=self.token)

    def test_init(self) -> None:
        base_url = 'https://example.com'
        
        client = BaseClient(
            session=self.session, 
            access_key=self.token,
            base_url=base_url
        )
        
        self.assertIs(client.session, self.session)
        self.assertEqual(client.access_key, self.token)
        self.assertEqual(client.base_url, base_url)
        
        with self.assertRaises(AssertionError):
            client = BaseClient(session='test :)', access_key=self.token)

    @responses.activate
    def test_request(self) -> None:
        """ Test request with good response. """
        method = 'GET'
        url = 'https://test.com/response'
        params = {'access_key': self.token}
        matches = [matchers.query_param_matcher(params)]
        mock_response = self.generator.get_response(url=url, matches=matches)
        responses.add(mock_response)

        response = self.client.request(method, url)

        self.assertDictEqual(response, json.loads(DEFAULT_BODY))

    @responses.activate
    def test_retry_request(self) -> None:
        """ Test retry request with good response. """
        status_codes = [500, 200]
        method = 'GET'
        url = 'https://test.com/response'
        params = {'access_key': self.token}
        matches = [matchers.query_param_matcher(params)]

        for status_code in status_codes:
            mock_response = self.generator.get_response(
                status=status_code,
                url=url,
                matches=matches
            )
            responses.add(mock_response)

        response = self.client.request(method, url)

        self.assertDictEqual(response, json.loads(DEFAULT_BODY))

    @responses.activate
    def test_fail_request(self) -> None:
        """ Test retry request with server-side error in response. """
        status = 500
        method = 'GET'
        url = 'https://test.com/response'
        params = {'access_key': self.token}
        matches = [matchers.query_param_matcher(params)]
        mock_response = self.generator.get_response(status=status, url=url, matches=matches)
        responses.add(mock_response)
        
        with self.assertRaises(requests.exceptions.HTTPError):
            response = self.client.request(method, url) 

    @responses.activate
    def test_get_request(self) -> None:
        """ Test get request with good response. """
        method = 'GET'
        endpoint = '/test'
        url = self.client.base_url + endpoint
        params = {'access_key': self.token}
        matches = [matchers.query_param_matcher(params)]
        mock_response = self.generator.get_response(url=url, matches=matches)
        responses.add(mock_response)
        
        response = self.client.get(endpoint)
        
        self.assertDictEqual(response, json.loads(DEFAULT_BODY))

    def tearDown(self) -> None:
        self.session.close()
