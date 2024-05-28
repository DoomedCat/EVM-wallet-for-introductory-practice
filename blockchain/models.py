import json
from dataclasses import dataclass

from web3 import Web3
from web3.eth.eth import ChecksumAddress
import requests


@dataclass
class DefaultABI:
    Token = [
        {
            'constant': True,
            'inputs': [],
            'name': 'name',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'symbol',
            'outputs': [{'name': '', 'type': 'string'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'totalSupply',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [],
            'name': 'decimals',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': 'account', 'type': 'address'}],
            'name': 'balanceOf',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': True,
            'inputs': [{'name': 'owner', 'type': 'address'}, {'name': 'spender', 'type': 'address'}],
            'name': 'allowance',
            'outputs': [{'name': 'remaining', 'type': 'uint256'}],
            'payable': False,
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': 'spender', 'type': 'address'}, {'name': 'value', 'type': 'uint256'}],
            'name': 'approve',
            'outputs': [],
            'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        },
        {
            'constant': False,
            'inputs': [{'name': 'to', 'type': 'address'}, {'name': 'value', 'type': 'uint256'}],
            'name': 'transfer',
            'outputs': [], 'payable': False,
            'stateMutability': 'nonpayable',
            'type': 'function'
        }]


class Token:
    name: str
    decimals: int

    def __init__(self, name: str, contract_address: ChecksumAddress, rpc: str, decimals: int | None = None):
        self.name = name
        self.decimals = decimals
        if contract_address != "NATIVE_COIN":
            self.contract_address = Web3.to_checksum_address(contract_address)
        else:
            self.contract_address = contract_address

        if not self.decimals:
            web3 = Web3(provider=Web3.HTTPProvider(endpoint_uri=rpc))
            contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=DefaultABI.Token)
            self.decimals = contract.functions.decimals().call()



class Network:
    tokens: dict[str, Token]

    def __init__(
            self,
            name: str,
            rpc: str,
            chain_id: int | None = None,
            coin_symbol: str | None = None,
    ) -> None:
        self.name: str = name
        self.rpc: str = rpc
        self.chain_id: int | None = chain_id
        self.native_coin_symbol: str | None = coin_symbol

        if not self.chain_id:
            self.chain_id = Web3(Web3.HTTPProvider(self.rpc)).eth.chain_id

        if not self.native_coin_symbol:
            response = requests.get('https://chainid.network/chains.json').json()
            for network in response:
                if network['chainId'] == self.chain_id:
                    self.native_coin_symbol = network['nativeCurrency']['symbol']
                    break

        if self.native_coin_symbol:
            self.coin_symbol = self.native_coin_symbol.upper()

        self.tokens = dict()

        with open("blockchain/tokens.json", "r") as f:
            tokens_file = json.load(f)
        if self.name in tokens_file.keys():
            for token_name, token in tokens_file[self.name].items():
                self.tokens[token_name] = Token(name=token_name, contract_address=token["contract_address"],
                                                decimals=token["decimals"], rpc=self.rpc)
        if self.native_coin_symbol not in self.tokens:
            self.tokens[self.native_coin_symbol] = Token(name=self.native_coin_symbol, contract_address="NATIVE_COIN",
                                                         rpc=self.rpc, decimals=18)

    def save_tokens(self):
        with open("blockchain/tokens.json", "r") as f:
            tokens_file = json.load(f)
        if self.name not in tokens_file.keys():
            tokens_file[self.name] = dict()
        for token_name, token in self.tokens.items():
            if token_name not in tokens_file.keys():
                tokens_file[self.name][token_name] = dict()
            tokens_file[self.name][token_name]["contract_address"] = token.contract_address
            tokens_file[self.name][token_name]["decimals"] = token.decimals

        with open("blockchain/tokens.json", "w") as f:
            json.dump(tokens_file, f)

    def add_token(self, token_name: str, contract_address: str):
        self.tokens[token_name] = Token(name=token_name, contract_address=contract_address, rpc=self.rpc)
