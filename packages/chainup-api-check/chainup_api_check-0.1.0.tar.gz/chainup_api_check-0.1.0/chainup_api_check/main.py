import typer
from rich.console import Console
from rich.table import Table
from chainup_api_check.blockchain_checker import evm, blockchain
from concurrent.futures import ThreadPoolExecutor


import time

app = typer.Typer()
console = Console()

blockchain_list = [
    # evm
    blockchain.Item(protocol="ethereum", network="mainnet", type="evm"),
    blockchain.Item(protocol="ethereum", network="holesky", type="evm"),
    blockchain.Item(protocol="ethereum", network="sepolia", type="evm"),
    blockchain.Item(protocol="ethereum-archive",
                    network="mainnet", type="evm"),
    blockchain.Item(protocol="tron", network="mainnet", type="evm"),
    blockchain.Item(protocol="bsc", network="mainnet", type="evm"),
    blockchain.Item(protocol="polygon", network="mainnet", type="evm"),
    blockchain.Item(protocol="etc", network="mainnet", type="evm"),
    blockchain.Item(protocol="fantom", network="mainnet", type="evm"),
    blockchain.Item(protocol="heco", network="mainnet", type="evm"),
    blockchain.Item(protocol="arbitrum", network="mainnet", type="evm"),
    blockchain.Item(protocol="avax", network="mainnet", type="evm"),
    blockchain.Item(protocol="optimism", network="mainnet", type="evm"),
    blockchain.Item(protocol="base", network="mainnet", type="evm"),
    blockchain.Item(protocol="scroll", network="mainnet", type="evm"),
    blockchain.Item(protocol="filecoin", network="mainnet", type="evm"),
    blockchain.Item(protocol="filecoin",
                    network="calibration", type="evm"),
    # beacon
    blockchain.Item(protocol="ethereum2",
                    network="mainnet", type="beacon"),
    blockchain.Item(protocol="ethereum2-archive",
                    network="mainnet", type="beacon"),
    blockchain.Item(protocol="ethereum2",
                    network="holesky", type="beacon"),
    blockchain.Item(protocol="ethereum2",
                    network="sepolia", type="beacon"),


    # bitcoin
    blockchain.Item(protocol="bitcoin", network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="litecoin",
                    network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="bch", network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="omni", network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="zcash", network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="qtum", network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="dash", network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="c0ban", network="mainnet", type="bitcoin"),
    blockchain.Item(protocol="dogecoin",
                    network="mainnet", type="bitcoin"),

    # polkadot
    blockchain.Item(protocol="polkadot", network="mainnet", type="polkadot"),
    blockchain.Item(protocol="kusama", network="mainnet", type="polkadot"),

    # cosmos
    blockchain.Item(protocol="cosmos", network="mainnet", type="cosmos"),

    blockchain.Item(protocol="near", network="mainnet", type="near"),

    blockchain.Item(protocol="bnb", network="mainnet", type="bnb"),

    blockchain.Item(protocol="xrp", network="mainnet", type="xrp"),

    blockchain.Item(protocol="solana", network="mainnet", type="solana"),

    blockchain.Item(protocol="ton", network="mainnet", type="ton"),

    blockchain.Item(protocol="aptos", network="mainnet", type="aptos"),




]


def print_blockchain_status(domain: str, protocol: str, token: str):
    table_title = f"{domain} Blockchain Status"
    table = Table(title=table_title)
    table.add_column("No.", justify="center", no_wrap=True)  # 行号列
    table.add_column("Protocol", justify="center",
                     no_wrap=True)
    table.add_column("Network", justify="center")
    table.add_column("Is Healthy", justify="center")
    table.add_column("HTTP Code", justify="center")
    table.add_column("Height", justify="center")
    table.add_column("Request Delay (s)", justify="center")
    table.add_column("Curl", justify="left")
    if protocol == "all":
        with ThreadPoolExecutor() as executor:
            # 使用 map 方法并发执行 do_check 方法，并按照输入顺序返回结果
            results = list(executor.map(lambda i: i.do_check(
                domain, token), blockchain_list))

            for row_number, result in enumerate(results, start=1):
                if result:
                    result.add_table(table, str(row_number))
    else:
        find = False
        for checker in blockchain_list:
            if checker.protocol == protocol:
                status = checker.do_check(domain=domain, token=token)
                status.add_table(table=table, row_number="1")
                find = True
        if not find:
            print(f"{protocol} not in list. plase check it")

    return table


@app.command()
def checker(token: str = typer.Argument(),
            domain: str = typer.Option(
                "api.chainup.net", "--domain", "-d", help="cluster domain"),
            protocol: str = typer.Option(
                "all", "--protocol", "-p", help="protocol name. e.g. ethereum"),
            repeat: bool = typer.Option(
                False, "--repeat", "-r", help="repeat print result"),
            interval: int = typer.Option(
                10, "--interval", "-i", help="every n seconds request ")
            ):

    while repeat:
        table = print_blockchain_status(
            domain=domain, protocol=protocol, token=token)

        console.clear()
        console.print(table)
        time.sleep(interval)
    else:
        table = print_blockchain_status(
            domain=domain, protocol=protocol, token=token)

        console.clear()
        console.print(table)


if __name__ == "__main__":
    app()
