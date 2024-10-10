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
        data = """-H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"getblockchaininfo","params":[],"id":1}'"""
        return f"curl -i {url} {data}"

    def get_current_block_height(self):
        """
        获取当前块高
        """
        result, http_code = send_rpc_request(
            url=self._build_provider_url(), method="getblockchaininfo")
        current, target = None, None
        if result is not None:
            current = result["blocks"]
            target = result["headers"]
        if current == None or target == None:
            return None, False, http_code
        if http_code == 200 and int(target) - int(current) <= 100:
            return current, True, 200
        else:
            return current, False, http_code

    def get_status(self):
        """
        获取当前块高、是否同步最新以及请求延迟
        """
        start_time = time.time()
        block_height, is_healthy, code = self.get_current_block_height()
        end_time = time.time()
        command = self.curl_command()
        request_delay = end_time - start_time
        height = 0
        if block_height is None:
            height = 0
        else:
            height = block_height

        status = BlockchainStatus(protocol=self.protocol, network=self.network, is_healthy=is_healthy,
                                  height=height, code=code, request_delay=request_delay, command=command)

        return status
