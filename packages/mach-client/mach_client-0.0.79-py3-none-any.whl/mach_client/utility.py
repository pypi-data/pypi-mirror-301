from eth_typing import ChecksumAddress
from web3 import AsyncWeb3
from web3.contract import AsyncContract
from web3.middleware import ExtraDataToPOAMiddleware

from . import config
from .constants import ChainId
from .data_types import Chain, Token
from .client import client


async def make_w3(chain: Chain) -> AsyncWeb3:
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(chain.rpc_url))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    assert await w3.is_connected()

    return w3


def make_token_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=AsyncWeb3.to_checksum_address(token.contract_address),
        abi=config.erc20_abi,
    )


def make_order_book_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=client.deployments[token.chain.id]["contracts"]["order_book"],
        abi=config.order_book_abi,
    )
