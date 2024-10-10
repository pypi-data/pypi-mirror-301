from rich.table import Table
from rich.style import Style


class BlockchainStatus:
    def __init__(self, protocol, network, height, is_healthy, request_delay, code, command):
        self.protocol = protocol
        self.network = network
        self.height = height
        self.is_healthy = is_healthy
        self.request_delay = request_delay
        self.code = code
        self.command = command

    def add_table(self, table: Table,row_number):

        style = Style(color="green") if self.is_healthy else Style(color="red")
        table.add_row(
            row_number,
            self.protocol,
            self.network,
            str(self.is_healthy),
            str(self.code),
            str(self.height),
            f"{self.request_delay:.4f}",
            self.command,
            style=style,
            end_section=True
        )
