import time
from chainup_api_check.model.blockchain_status import BlockchainStatus
from chainup_api_check.util.send_jsonrpc import send_rpc_request


class Checker:
    def __init__(self, domain, protocol, network, token):
        self.domain = domain
        self.protocol = protocol
        self.network = network
        self.token = token

        self.provider_url = self._build_provider_url()

    def _build_provider_url(self):
        return f"https://{self.domain}/{self.protocol}/{self.network}/{self.token}"

    def curl_command(self):
        url = self._build_provider_url()
        data = """-H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"block","params":{"finality": "final"},"id":1}' """
        return f"curl -i {url} {data}"

    def get_current_block_height(self):
        """
        获取当前块高
        """
        params = {"finality": "final"}
        return send_rpc_request(url=self._build_provider_url(), method="block", params=params)

    def get_status(self):
        """
        获取当前块高、是否同步最新以及请求延迟
        """
        start_time = time.time()
        result, code = self.get_current_block_height()
        end_time = time.time()
        is_healthy = False
        command = self.curl_command()
        request_delay = end_time - start_time
        height = 0
        if result is None:
            height = 0
        else:
            is_healthy = True
            height = result["header"]["height"]

        status = BlockchainStatus(protocol=self.protocol, network=self.network, is_healthy=is_healthy,
                                  height=height, code=code, request_delay=request_delay, command=command)

        return status
