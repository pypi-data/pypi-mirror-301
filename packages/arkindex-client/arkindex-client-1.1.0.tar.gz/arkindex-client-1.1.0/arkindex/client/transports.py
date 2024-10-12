# -*- coding: utf-8 -*-
import http
from importlib.metadata import version

import requests

from arkindex import exceptions
from arkindex.client import decoders

REQUEST_TIMEOUT = (30, 60)


class BlockAllCookies(http.cookiejar.CookiePolicy):
    """
    A cookie policy that rejects all cookies.
    Used to override the default `requests` behavior.
    """

    return_ok = set_ok = domain_return_ok = path_return_ok = (
        lambda self, *args, **kwargs: False
    )
    netscape = True
    rfc2965 = hide_cookie2 = False


class BaseTransport:
    schemes = None

    def send(self, method, url, query_params=None, content=None, encoding=None):
        raise NotImplementedError()


class HTTPTransport(BaseTransport):
    schemes = ["http", "https"]
    default_decoders = [
        decoders.JSONDecoder(),
        decoders.TextDecoder(),
        decoders.DownloadDecoder(),
    ]

    def __init__(
        self,
        auth=None,
        decoders=None,
        headers=None,
        session=None,
        allow_cookies=True,
        verify=True,
    ):
        if session is None:
            session = requests.Session()
        if auth is not None:
            session.auth = auth
        if not allow_cookies:
            session.cookies.set_policy(BlockAllCookies())

        self.session = session
        self.verify = verify
        self.decoders = list(decoders) if decoders else list(self.default_decoders)

        client_version = version("arkindex-client")
        self.headers = {
            "accept": ", ".join([decoder.media_type for decoder in self.decoders]),
            "user-agent": f"arkindex-client/{client_version}",
        }
        if headers:
            self.headers.update({key.lower(): value for key, value in headers.items()})

    def send(self, method, url, query_params=None, content=None, encoding=None):
        options = self.get_request_options(query_params, content, encoding)
        response = self.session.request(method, url, **options)
        result = self.decode_response_content(response)

        if 400 <= response.status_code <= 599:
            title = "%d %s" % (response.status_code, response.reason)
            raise exceptions.ErrorResponse(
                title=title, status_code=response.status_code, content=result
            )

        return result

    def get_decoder(self, content_type=None):
        """
        Given the value of a 'Content-Type' header, return the appropriate
        decoder for handling the response content.
        """
        if content_type is None:
            return self.decoders[0]

        content_type = content_type.split(";")[0].strip().lower()
        main_type = content_type.split("/")[0] + "/*"
        wildcard_type = "*/*"

        for codec in self.decoders:
            if codec.media_type in (content_type, main_type, wildcard_type):
                return codec

        text = (
            "Unsupported encoding '%s' in response Content-Type header." % content_type
        )
        message = exceptions.ErrorMessage(text=text, code="cannot-decode-response")
        raise exceptions.ClientError(messages=[message])

    def get_request_options(self, query_params=None, content=None, encoding=None):
        """
        Return the 'options' for sending the outgoing request.
        """
        options = {
            "headers": dict(self.headers),
            "params": query_params,
            "timeout": REQUEST_TIMEOUT,
            "verify": self.verify,
        }

        if content is not None:
            assert (
                encoding == "application/json"
            ), "Only JSON request bodies are supported"
            options["json"] = content

        return options

    def decode_response_content(self, response):
        """
        Given an HTTP response, return the decoded data.
        """
        if not response.content:
            return None

        content_type = response.headers.get("content-type")
        decoder = self.get_decoder(content_type)
        return decoder.decode(response)
