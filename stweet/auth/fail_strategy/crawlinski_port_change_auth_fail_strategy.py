import time

from stweet.auth.fail_strategy.auth_fail_strategy import AuthFailStrategy
from ...http_request import RequestsWebClient

class CrawlinskiPortChangeAuthFailStrategy(AuthFailStrategy):
    web_client: RequestsWebClient
    proxy_url: str
    min_port : int
    max_port : int
    cur_port : int

    def __init__(self, proxy_url: str, min_port : int, max_port : int):
        self.proxy_url = proxy_url
        self.min_port = min_port
        self.max_port = max_port
        self.cur_port = min_port

    def set_web_client(self, web_client: RequestsWebClient):
        self.web_client = web_client
        web_client.set_proxy(self.proxy_url, self.cur_port)

    def get_next_port(self):
        self.cur_port += 1
        if self.cur_port > self.max_port:
            self.cur_port = self.min_port

    def run_strategy(self) -> None:
        time.sleep(5)
        self.get_next_port()
        web_client.set_proxy(self.proxy_url, self.cur_port)

