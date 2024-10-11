import os

from .constants import ChainId

# Anything on these chains will be invisible to the client
excluded_chains = frozenset(
    (
        ChainId.ETHEREUM,
        ChainId.MODE,
        ChainId.CELO,
        ChainId.MANTLE,
        ChainId.OPBNB,
        ChainId.SCROLL,
        ChainId.BLAST,
    )
)

rpc_urls = {
    ChainId.ETHEREUM: "https://long-capable-tree.quiknode.pro/4f8abee71b92694624d5f6a5aac43bf273b76db1/",
    ChainId.OP: "https://alien-dry-lake.optimism.quiknode.pro/9e3364e544a78fa0581658f542d58d8c02cd13ba/",
    ChainId.BSC: "https://necessary-thrumming-diamond.bsc.quiknode.pro/f2f3a08170d298c0bd742d77ea0462afcec15dd4/",
    ChainId.POLYGON: "https://holy-restless-vineyard.matic.quiknode.pro/559b966d2ea5ab37e95abee0cf1049a10971e30d/",
    # ChainId.OPBNB: "Only has regular BSC?",
    ChainId.MANTLE: "https://still-compatible-wind.mantle-mainnet.quiknode.pro/277b01e4afb73df889a08ba018dc14e354f5f0da/",
    ChainId.BASE: "https://polished-spring-star.base-mainnet.quiknode.pro/19455fd433fb2639609315f8588c3a58a5a9a10f/",
    # ChainId.MODE: "Not yet available on Quicknode?",
    ChainId.ARBITRUM: "https://prettiest-patient-scion.arbitrum-mainnet.quiknode.pro/2d53fa7ffc71e31afb3113f96c54519fcd6516e2/",
    ChainId.CELO: "https://attentive-alien-water.celo-mainnet.quiknode.pro/9c1b86178a6c7ebc5c772663ac82b51003ef8a81/",
    ChainId.AVALANCHE_C_CHAIN: "https://withered-soft-field.avalanche-mainnet.quiknode.pro/f0478bf89e96d35ee8351213a1120fe4ba292849/ext/bc/C/rpc/",
    ChainId.BLAST: "https://warmhearted-few-scion.blast-mainnet.quiknode.pro/22d44d1f9a1a57adf90c0efd2d644977c3dd5a23/",
    ChainId.SCROLL: "https://sleek-crimson-flower.scroll-mainnet.quiknode.pro/37e22c7823176a82f7cea7b89b5c37786b76a810/",
    # tron: "https://practical-restless-meme.tron-mainnet.quiknode.pro/6088a1547d6e57bd2b9376aebca00366523ae405/jsonrpc",
    # solana: "https://cosmological-soft-dust.solana-mainnet.quiknode.pro/c4fc0753cc3e5219724fcbf042ce9ce0abd84590/",
}

backend_url = os.environ.get(
    "MACH_BACKEND_URL", "https://cache-half-full-production.fly.dev"
)

endpoints = {
    "orders": "/v1/orders",
    "gas": "/v1/orders/gas",
    "quotes": "/v1/quotes",
    "points": "/v1/points",
    "token_balances": "/tokenBalances",
    "get_config": "/get_config",
}
