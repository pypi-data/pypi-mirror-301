from typing import cast

from eth_typing import ChecksumAddress
from mach_client import client


def test_order_history() -> None:
    wallet = cast(ChecksumAddress, "0xb20094DFede30AbEe3a8d549BbA828b6fd771106")
    order_history = client.get_orders(wallet)

    assert type(order_history) == list
    assert type(order_history[0]) == dict
    assert (
        len(
            frozenset(
                (
                    "id",
                    "taker_address",
                    "maker_address",
                    "src_asset_address",
                    "dst_asset_address",
                    "src_chain",
                    "dst_chain",
                    "src_amount",
                    "dst_amount",
                    "created_at",
                    "filled_at",
                    "expires_at",
                    "completed",
                    "place_tx",
                    "fill_tx",
                    "eta",
                )
            )
            - frozenset(order_history[0].keys())
        )
        == 0
    )
