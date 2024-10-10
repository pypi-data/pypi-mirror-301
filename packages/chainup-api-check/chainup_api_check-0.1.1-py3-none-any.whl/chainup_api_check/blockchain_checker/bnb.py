import time
from chainup_api_check.model.blockchain_status import BlockchainStatus
from chainup_api_check.util.send_jsonrpc import send_get_request


class Checker:
    def __init__(self, domain, protocol, network, token):
        self.domain = domain
        self.protocol = protocol
        self.network = network
        self.token = token

        self.provider_url = self._build_provider_url()

    def _build_provider_url(self):

        return f"https://{self.domain}/{self.protocol}/{self.network}/{self.token}/status"

    def curl_command(self):
        url = self._build_provider_url()
        data = """-H 'Content-Type: application/json' '"""
        return f"curl -i {url} {data}"

    def get_current_block_height(self):
        """
        获取当前块高
        """
        return send_get_request(url=self._build_provider_url())

    def get_status(self):
        """
        获取当前块高、是否同步最新以及请求延迟
        """
        start_time = time.time()
        result, code = self.get_current_block_height()
        end_time = time.time()
        is_healthy = False
        height = 0
        if result is not None:
            data = result["result"]["sync_info"]
            is_healthy = data["catching_up"] == False
            height = data["latest_block_height"]

        command = self.curl_command()
        request_delay = end_time - start_time

        status = BlockchainStatus(protocol=self.protocol, network=self.network, is_healthy=is_healthy,
                                  height=height, code=code, request_delay=request_delay, command=command)

        return status
