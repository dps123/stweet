"""DefaultTwitterWebClientProvider class."""
from tor_python_easy.tor_control_port_client import TorControlPortClient

from .twitter_auth_web_client_interceptor import TwitterAuthWebClientInterceptor
from ..auth import SimpleAuthTokenProvider
from ..auth.fail_strategy.tor_ip_change_auth_fail_strategy import TorIpChangeAuthFailStrategy
from ..auth.fail_strategy.crawlinski_port_change_auth_fail_strategy import CrawlinskiPortChangeAuthFailStrategy
from ..http_request import WebClient, RequestsWebClient, RequestsWebClientProxyConfig


class DefaultTwitterWebClientProvider:

    @staticmethod
    def get_web_client() -> WebClient:
        """Method returns default WebClient."""
        return RequestsWebClient(interceptors=[TwitterAuthWebClientInterceptor()])

    @staticmethod
    def get_web_client_preconfigured_for_tor_proxy(
            socks_proxy_url: str,
            control_host: str,
            control_port: int,
            control_password: str
    ) -> WebClient:
        tor_control_client = TorControlPortClient(control_host, control_port, control_password)
        fail_strategy = TorIpChangeAuthFailStrategy(tor_control_client)
        auth_token_provider = SimpleAuthTokenProvider(fail_strategy)
        return RequestsWebClient(
            proxy=RequestsWebClientProxyConfig(socks_proxy_url, socks_proxy_url),
            interceptors=[TwitterAuthWebClientInterceptor(auth_token_provider=auth_token_provider)]
        )

    @staticmethod
    def get_web_client_preconfigured_socks_proxy(
            socks_proxy_url: str,
            socks_min_port:  int,
            socks_max_port:  int
    ) -> WebClient:
        fail_strategy = CrawlinskiPortChangeAuthFailStrategy(socks_proxy_url, socks_min_port, socks_max_port)
        auth_token_provider = SimpleAuthTokenProvider(fail_strategy)
        web_client = RequestsWebClient(
            interceptors=[TwitterAuthWebClientInterceptor(auth_token_provider=auth_token_provider)]
        )
        fail_strategy.set_web_client(web_client)
        return web_client
