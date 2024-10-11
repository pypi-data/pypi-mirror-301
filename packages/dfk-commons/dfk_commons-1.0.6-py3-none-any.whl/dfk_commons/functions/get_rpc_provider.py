from web3 import Web3
from web3.middleware import geth_poa_middleware
import requests

from dfk_commons.classes.RPCProvider import RPCProvider

def try_rpc(rpc, logger):
    try:
        session = requests.Session()
        if "id" in rpc and "password" in rpc:
            session.auth = (rpc["id"], rpc["password"])
        w3 = Web3(Web3.HTTPProvider(rpc["url"], session=session))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        w3.client_version
        w3.eth.get_block("latest")
        return w3
    except Exception as e:
        logger.info(f"RPC {rpc['url']} failed: {e}")
    return False


def get_rpc_provider(chain, disabled_rpc_list, logger):
    if chain == "dfk":
        rpc_list = [
            {
                "url":"https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc",
            },
            {
                "url":"https://avax-pokt.nodies.app/ext/bc/q2aTwKuyzgs8pynF7UXBZCU7DejbZbZ6EUyHr3JQzYgwNPUPi/rpc",
            },
            {
                "url":"https://dfkchain.api.onfinality.io/public",
            },
        ]
        chainId= 53935
    elif chain == "klay":
        rpc_list = [
            {
                "url":"https://public-en-cypress.klaytn.net",
            },
            {
                "url":"https://klaytn-pokt.nodies.app",
            },
            {
                "url":"https://klaytn.api.onfinality.io/public",
            },
        ]
        chainId = 8217

    for rpc in rpc_list:
        if rpc["url"] in disabled_rpc_list:
            continue
        w3 = try_rpc(rpc, logger)
        if w3:
            logger.info(f"Using RPC: {rpc['url']}")
            return RPCProvider(chain, w3, rpc["url"], chainId)
        
    raise Exception("No RPC available")
