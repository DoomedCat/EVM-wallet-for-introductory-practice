from fake_useragent import UserAgent
from web3 import Web3
import json
from decimal import Decimal

from eth_account.signers.local import LocalAccount
from web3.middleware import geth_poa_middleware

from blockchain.models import Network, DefaultABI


class Client:
    network: Network
    account: LocalAccount | None
    w3: Web3

    def __init__(
            self,
            network: Network,
            private_key: str | None = None,
    ) -> None:
        self.network = network
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': UserAgent().chrome
        }

        self.w3 = Web3(
            provider=Web3.HTTPProvider(
                endpoint_uri=self.network.rpc,
                request_kwargs={'headers': self.headers}
            ),
            middlewares=[]
        )

        self.account = self.w3.eth.account.from_key(private_key=private_key)

    def get_balance(self, token_name: str) -> Decimal:
        token = self.network.tokens[token_name]
        if token.contract_address == "NATIVE_COIN":
            return self.w3.from_wei(number=self.w3.eth.get_balance(self.account.address), unit="ether")
        else:
            contract = self.w3.eth.contract(address=Web3.to_checksum_address(token.contract_address), abi=DefaultABI.Token)
            return Decimal(contract.functions.balanceOf(
                self.account.address).call()) / Decimal(10 ** token.decimals)

    def get_gas(self, token: str, recipient: str, amount: str) -> Decimal:
        token = self.network.tokens[token]
        if token.contract_address == "NATIVE_COIN":
            txn = {
                'chainId': self.network.chain_id,
                'from': self.account.address,
                'to': self.w3.to_checksum_address(recipient),
                'value': int(self.w3.to_wei(number=Decimal(amount), unit='ether')),
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gasPrice': self.w3.eth.gas_price,
            }
            return self.w3.from_wei(number=self.w3.eth.estimate_gas(txn), unit='ether')*Decimal("1.2")
        else:
            contract = self.w3.eth.contract(address=Web3.to_checksum_address(token.contract_address), abi=DefaultABI.Token)
            tx_data = contract.encodeABI(
                "transfer",
                args=(
                    self.w3.to_checksum_address(recipient),
                    int(self.w3.to_wei(number=Decimal(amount), unit='ether'))
                )
            )
            txn = {
                'chainId': self.network.chain_id,
                'from': self.account.address,
                'to': self.w3.to_checksum_address(recipient),
                'value': int(self.w3.to_wei(number=Decimal(amount), unit='ether')),
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gasPrice': self.w3.eth.gas_price,
                'data': tx_data
            }
            return self.w3.from_wei(number=self.w3.eth.estimate_gas(txn), unit='ether')*Decimal("1.2")

    def send_transaction(self, token: str, recipient: str, amount: str) -> tuple[bool, str]:
        token = self.network.tokens[token]
        if token.contract_address == "NATIVE_COIN":
            txn = {
                'chainId': self.network.chain_id,
                'from': self.account.address,
                'to': self.w3.to_checksum_address(recipient),
                'value': int(self.w3.to_wei(number=Decimal(amount), unit='ether')),
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gasPrice': self.w3.eth.gas_price,
            }
            txn["gas"] = int(self.w3.eth.estimate_gas(txn)*1.2)
            sign = self.account.sign_transaction(txn)
            tx_hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
            try:
                data = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=200)
                if "status" in data and data['status'] == 1:
                    return True, "0x"+tx_hash.hex()
                else:
                    return False, ""
            except Exception as ex:
                print(ex)
                return False, ""
        else:
            contract = self.w3.eth.contract(address=Web3.to_checksum_address(token.contract_address), abi=DefaultABI.Token)
            tx_data = contract.encodeABI(
                "transfer",
                args=(
                    self.w3.to_checksum_address(recipient),
                    int(self.w3.to_wei(number=Decimal(amount), unit='ether'))
                )
            )
            txn = {
                'chainId': self.network.chain_id,
                'from': self.account.address,
                'to': self.w3.to_checksum_address(recipient),
                'value': int(self.w3.to_wei(number=Decimal(amount), unit='ether')),
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gasPrice': self.w3.eth.gas_price,
                'data': tx_data
            }
            txn["gas"] = int(self.w3.eth.estimate_gas(txn) * 1.2)
            sign = self.account.sign_transaction(txn)
            tx_hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
            try:
                data = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=200)
                if "status" in data and data['status'] == 1:
                    return True, "0x"+tx_hash.hex()
                else:
                    return False, ""
            except:
                return False, ""


class Clients:
    private_key: str
    clients_dict: dict[str, Client] = dict()

    @staticmethod
    def private_key_is_correct(private_key: str) -> bool:
        try:
            w3 = Web3(provider=Web3.HTTPProvider(endpoint_uri='https://eth.llamarpc.com'))
            w3.eth.account.from_key(private_key.strip())
        except:
            return False
        return True

    @staticmethod
    def mnemonic_phrase_is_correct(mnemonic_phrase: str) -> bool:
        try:
            web3 = Web3(provider=Web3.HTTPProvider(endpoint_uri='https://eth.llamarpc.com'))
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            web3.eth.account.enable_unaudited_hdwallet_features()
            web3_account: LocalAccount = web3.eth.account.from_mnemonic(mnemonic_phrase.strip())
        except:
            return False
        return True

    def __init__(self, private_key: str | None = None, mnemonic_phrase: str | None = None):
        if not private_key:
            web3 = Web3(provider=Web3.HTTPProvider(endpoint_uri='https://eth.llamarpc.com'))
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            web3.eth.account.enable_unaudited_hdwallet_features()
            web3_account: LocalAccount = web3.eth.account.from_mnemonic(mnemonic_phrase.strip())
            self.private_key = web3.to_checksum_address(web3_account._private_key.hex())
        else:
            self.private_key = private_key.strip()

        with open("blockchain/networks.json", "r") as f:
            networks = json.load(f)
        for network_name, network_data in networks.items():
            self.clients_dict[network_name] = Client(private_key=private_key,
                                                     network=Network(name=network_name, **network_data))

    def add_network(self, network_name: str, rpc: str):
        self.clients_dict[network_name] = Client(private_key=self.private_key,
                                                 network=Network(name=network_name, rpc=rpc))

    def save_in_file(self):
        with open("blockchain/networks.json", "r") as f:
            networks = json.load(f)
        for network_name, client in self.clients_dict.items():
            network = client.network
            network.save_tokens()
            if network_name not in networks.keys():
                networks[network_name] = dict()
            networks[network_name]['rpc'] = network.rpc
            networks[network_name]['chain_id'] = network.chain_id
            networks[network_name]['coin_symbol'] = network.coin_symbol
        with open("blockchain/networks.json", "w") as f:
            json.dump(networks, f)

    def get_networks_names(self) -> list[str]:
        networks = []
        for network_name, _ in self.clients_dict.items():
            networks.append(network_name)
        return networks

    def get_networks_with_tokens_list(self) -> dict[str, list[str]]:
        tokens = dict()
        for network_name, client in self.clients_dict.items():
            tokens_of_network = []
            for token_name, _ in client.network.tokens.items():
                tokens_of_network.append(token_name)
            tokens[network_name] = tokens_of_network
        return tokens

    def get_balance(self, network_name: str, token_name: str) -> Decimal:
        client = self.clients_dict[network_name]
        return client.get_balance(token_name=token_name)


    def get_gas(self, network: str, token: str, recipient: str, amount: str) -> Decimal:
        client = self.clients_dict[network]
        return client.get_gas(token=token, recipient=recipient, amount=amount)

    def send_transaction(self, network: str, token: str, recipient: str, amount: str) -> tuple[bool, str]:
        client = self.clients_dict[network]
        return client.send_transaction(token=token, recipient=recipient, amount=amount)