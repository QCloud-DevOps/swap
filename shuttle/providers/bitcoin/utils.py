#!/usr/bin/env python3

from btcpy.structs.script import P2pkhScript, P2shScript
from btcpy.structs.transaction import Sequence, MutableTransaction
from btcpy.structs.address import Address
from btcpy.setup import setup
from base64 import b64encode, b64decode

import cryptos
import hashlib
import json
import binascii

from ...utils.exceptions import AddressError, NetworkError


def decode_transaction_raw(tx_raw):
    """
    Decode bitcoin transaction raw.

    :param tx_raw: bitcoin transaction raw.
    :type tx_raw: str
    :returns: dict -- decoded bitcoin transaction.

    >>> from shuttle.providers.bitcoin.utils import decode_transaction_raw
    >>> decode_transaction_raw(transaction_raw)
    {...}
    """

    tx_raw = str(tx_raw + "=" * (-len(tx_raw) % 4))
    try:
        tx_raw = json.loads(b64decode(str(tx_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise ValueError("invalid bitcoin transaction raw")
    if "type" not in tx_raw and not str(tx_raw["type"]).startswith("bitcoin"):
        raise ValueError("invalid bitcoin transaction raw")
    # Setting testnet
    setup(tx_raw["network"], strict=True)
    tx = MutableTransaction.unhexlify(tx_raw["raw"])
    return dict(
        fee=tx_raw["fee"],
        type=tx_raw["type"],
        tx=tx.to_json(),
        network=tx_raw["network"]
    )


# Checking address
def is_address(address, network="testnet"):
    """
    Check bitcoin address.

    :param address: bitcoin address.
    :type address: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns: bool -- bitcoin valid/invalid address.

    >>> from shuttle.providers.bitcoin.utils import is_address
    >>> is_address(bitcoin_address, "testnet")
    True
    """

    if isinstance(address, str):
        if network == "testnet":
            return cryptos.Bitcoin(testnet=True).is_address(address)
        elif network == "mainnet":
            return cryptos.Bitcoin(testnet=False).is_address(address)
        else:
            raise NetworkError("invalid %s network" % network, "only takes testnet or mainnet")
    raise TypeError("address must be string format!")


# Double SHA256 hash
def double_sha256(data):
    """
    Double SHA256 hash.

    :param data: encoded data.
    :type data: bytes
    :returns: bytearray -- hashed double sha256.

    >>> from shuttle.providers.bitcoin.utils import double_sha256
    >>> double_sha256("Hello Meheret!".encode())
    b"..."
    """

    if isinstance(data, bytes):
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()
    raise TypeError("data must be bytes format!")


# Transaction fee calculator
def fee_calculator(transaction_input=1, transaction_output=1):
    """
    Bitcoin fee calculator.

    :param transaction_input: transaction input numbers, defaults to 1.
    :type transaction_input: int
    :param transaction_output: transaction output numbers, defaults to 1.
    :type transaction_output: int
    :returns: int -- bitcoin fee.

    >>> from shuttle.providers.bitcoin.utils import fee_calculator
    >>> fee_calculator(2, 9)
    1836
    """

    # 444 input 102 output
    transaction_input = ((transaction_input - 1) * 444) + 576
    transaction_output = ((transaction_output - 1) * 102)
    return transaction_input + transaction_output


# Setting expiration to script
def expiration_to_script(sequence):
    if isinstance(sequence, int):
        if sequence <= 16:
            return "OP_%d" % sequence
        else:
            return Sequence(sequence).for_script()
    raise TypeError("Sequence must be integer format!")


# Creating script from address
def script_from_address(address, network="testnet"):
    """
    Get script from address.

    :param address: bitcoin address.
    :type address: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns: P2pkhScript, P2shScript -- bitcoin p2pkh or p2sh script instance.

    >>> from shuttle.providers.bitcoin.utils import script_from_address
    >>> script_from_address("mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH", "testnet")
    P2pkhScript('7b7c4431a43b612a72f8229935c469f1f6903658')
    """

    if not is_address(address, network):
        raise AddressError("invalid %s %s address!" % (network, address))
    load_address = Address.from_string(address)
    get_type = load_address.get_type()
    if str(get_type) == "p2pkh":
        return P2pkhScript(load_address)
    elif str(get_type) == "p2sh":
        return P2shScript(load_address)


# Creating script from address
def address_to_hash(address, network="testnet"):
    """
    Get hash from address.

    :param address: bitcoin address.
    :type address: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns: P2pkhScript, P2shScript -- bitcoin p2pkh or p2sh script instance.

    >>> from shuttle.providers.bitcoin.utils import address_to_hash
    >>> address_to_hash("mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH", "testnet")
    "7b7c4431a43b612a72f8229935c469f1f6903658"
    """

    if not is_address(address, network):
        raise AddressError("invalid %s %s address!" % (network, address))
    return Address.from_string(address).hash.hex()
