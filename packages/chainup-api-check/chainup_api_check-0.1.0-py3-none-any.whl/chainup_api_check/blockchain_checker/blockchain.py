from chainup_api_check.blockchain_checker import evm, bitcoin, beacon, polkadot, cosmos, near, bnb, xrp, solana, ton, aptos


class Item:
    def __init__(self, protocol, network, type):
        self.protocol = protocol
        self.network = network
        self.type = type

    def do_check(self, domain, token):
        block_status = None
        if self.type == "evm":
            eth = evm.Checker(domain=domain, token=token,
                              protocol=self.protocol, network=self.network)
            block_status = eth.get_status()
        if self.type == "bitcoin":
            btc = bitcoin.Checker(domain=domain, token=token,
                                  protocol=self.protocol, network=self.network)
            block_status = btc.get_status()
        if self.type == "beacon":
            eth2 = beacon.Checker(domain=domain, token=token,
                                  protocol=self.protocol, network=self.network)
            block_status = eth2.get_status()
        if self.type == "polkadot":
            p = polkadot.Checker(domain=domain, token=token,
                                 protocol=self.protocol, network=self.network)
            block_status = p.get_status()
        if self.type == "cosmos":
            c = cosmos.Checker(domain=domain, token=token,
                               protocol=self.protocol, network=self.network)
            block_status = c.get_status()
        if self.type == "near":
            c = near.Checker(domain=domain, token=token,
                             protocol=self.protocol, network=self.network)
            block_status = c.get_status()
        if self.type == "bnb":
            c = bnb.Checker(domain=domain, token=token,
                            protocol=self.protocol, network=self.network)
            block_status = c.get_status()
        if self.type == "xrp":
            c = xrp.Checker(domain=domain, token=token,
                            protocol=self.protocol, network=self.network)
            block_status = c.get_status()
        if self.type == "solana":
            c = solana.Checker(domain=domain, token=token,
                               protocol=self.protocol, network=self.network)
            block_status = c.get_status()
        if self.type == "ton":
            c = ton.Checker(domain=domain, token=token,
                            protocol=self.protocol, network=self.network)
            block_status = c.get_status()
        if self.type == "aptos":
            c = aptos.Checker(domain=domain, token=token,
                              protocol=self.protocol, network=self.network)
            block_status = c.get_status()
        return block_status
