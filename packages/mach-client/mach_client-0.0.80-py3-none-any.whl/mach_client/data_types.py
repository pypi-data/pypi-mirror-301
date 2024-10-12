from eth_typing import ChecksumAddress
from typing import Any

from .client import client
from .constants import ChainId
from . import config


class Token:
    __slots__ = ("chain", "symbol", "chain_id", "contract_address", "decimals")

    def __init__(self, chain_id: ChainId, symbol: str):
        self.symbol = symbol
        self.chain = Chain(chain_id)
        asset_data = self.chain.data["assets"][self.symbol]
        self.contract_address: ChecksumAddress = asset_data["address"]
        self.decimals: int = asset_data["decimals"]

    @classmethod
    def from_str(cls, identifier: str):
        chain_name, symbol = identifier.split("-")
        chain_id = ChainId.from_name(chain_name)
        return cls(chain_id, symbol)

    @classmethod
    def from_contract_address(cls, chain: ChainId, contract_address: ChecksumAddress):
        symbol = client.symbol_by_contract[(chain, contract_address)]
        return cls(chain, symbol)

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Token)
            and self.chain == other.chain
            and self.symbol == other.symbol
        )

    def __repr__(self) -> str:
        return f"{self.chain}-{self.symbol}"

    def is_stablecoin(self) -> bool:
        upper = self.symbol.upper()

        return any(
            map(lambda symbol: symbol in upper, ("USD", "EUR", "JPY", "GPB", "CHF"))
        ) or upper in ("FRAX", "DAI", "MIM")


class Chain:
    __slots__ = ("id", "data", "lz_cid", "rpc_url")

    def __init__(self, id: ChainId):
        self.id = id
        self.data = client.deployments[self.id]
        self.lz_cid: int = self.data["lz_cid"]  # type: ignore
        self.rpc_url = config.rpc_urls[self.id]

    @property
    def name(self) -> str:
        return str(self.id)

    @classmethod
    def from_name(cls, name: str):
        return cls(ChainId.from_name(name))

    def __eq__(self, other) -> bool:
        return isinstance(other, Chain) and self.id == other.id

    def __repr__(self) -> str:
        return self.name
