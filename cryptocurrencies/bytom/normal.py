#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet, DEFAULT_PATH
from swap.providers.bytom.transaction import NormalTransaction
from swap.providers.bytom.assets import BTM as ASSET
from swap.providers.bytom.solver import NormalSolver
from swap.providers.bytom.signature import NormalSignature
from swap.providers.bytom.utils import (
    submit_transaction_raw, amount_unit_converter
)

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Bytom sender wallet mnemonic
SENDER_MNEMONIC: str = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"

print("=" * 10, "Sender Bytom Account")

# Initialize Bytom sender wallet
sender_wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom sender wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive Bytom sender wallet from path
sender_wallet.from_path(path=DEFAULT_PATH)

# Print some Bytom sender wallet info's
print("XPrivate Key:", sender_wallet.xprivate_key())
print("XPublic Key:", sender_wallet.xpublic_key())
print("Private Key:", sender_wallet.private_key())
print("Public Key:", sender_wallet.public_key())
print("Address:", sender_wallet.address())
print("Balance:", sender_wallet.balance(asset=ASSET, unit="BTM"), "BTM")

print("=" * 10, "Unsigned Normal Transaction")

# Initialize normal transaction
unsigned_normal_transaction: NormalTransaction = NormalTransaction(network=NETWORK)
# Build normal transaction
unsigned_normal_transaction.build_transaction(
    address=sender_wallet.address(),
    recipients={
        "bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p": amount_unit_converter(0.1, "BTM2NEU")
    },
    asset=ASSET
)

print("Unsigned Normal Transaction Fee:", unsigned_normal_transaction.fee(unit="NEU"), "NEU")
print("Unsigned Normal Transaction Hash:", unsigned_normal_transaction.hash())
print("Unsigned Normal Transaction Main Raw:", unsigned_normal_transaction.raw())
# print("Unsigned Normal Transaction Json:", json.dumps(unsigned_normal_transaction.json(), indent=4))
print("Unsigned Normal Transaction Unsigned Datas:", json.dumps(unsigned_normal_transaction.unsigned_datas(), indent=4))
print("Unsigned Normal Transaction Signatures:", json.dumps(unsigned_normal_transaction.signatures(), indent=4))
print("Unsigned Normal Transaction Type:", unsigned_normal_transaction.type())

unsigned_normal_transaction_raw = unsigned_normal_transaction.transaction_raw()
print("Unsigned Normal Transaction Raw:", unsigned_normal_transaction_raw)

print("=" * 10, "Signed Normal Transaction")

# Initialize normal solver
normal_solver: NormalSolver = NormalSolver(
    xprivate_key=sender_wallet.xprivate_key()
)

# Sing unsigned normal transaction
signed_normal_transaction: NormalTransaction = unsigned_normal_transaction.sign(normal_solver)

print("Signed Normal Transaction Fee:", signed_normal_transaction.fee(unit="NEU"), "NEU")
print("Signed Normal Transaction Hash:", signed_normal_transaction.hash())
print("Signed Normal Transaction Raw:", signed_normal_transaction.raw())
# print("Signed Normal Transaction Json:", json.dumps(signed_normal_transaction.json(), indent=4))
print("Signed Normal Transaction Unsigned Datas:", json.dumps(signed_normal_transaction.unsigned_datas(), indent=4))
print("Signed Normal Transaction Signatures:", json.dumps(signed_normal_transaction.signatures(), indent=4))
print("Signed Normal Transaction Type:", signed_normal_transaction.type())

signed_normal_transaction_raw: str = signed_normal_transaction.transaction_raw()
print("Signed Normal Transaction Raw:", signed_normal_transaction_raw)

print("=" * 10, "Normal Signature")

# Initialize normal signature
normal_signature: NormalSignature = NormalSignature(network=NETWORK)
# Sign unsigned normal transaction raw
normal_signature.sign(
    transaction_raw=unsigned_normal_transaction_raw,
    solver=normal_solver
)

print("Normal Signature Fee:", normal_signature.fee(unit="NEU"), "NEU")
print("Normal Signature Hash:", normal_signature.hash())
print("Normal Signature Raw:", normal_signature.raw())
print("Normal Signature Json:", json.dumps(normal_signature.json(), indent=4))
print("Normal Signature Unsigned Datas:", json.dumps(normal_signature.unsigned_datas(), indent=4))
print("Normal Signature Signatures:", json.dumps(normal_signature.signatures(), indent=4))
print("Normal Signature Type:", normal_signature.type())

signed_normal_signature_transaction_raw: str = normal_signature.transaction_raw()
print("Normal Signature Transaction Raw:", signed_normal_signature_transaction_raw)

# Check both signed normal transaction raws are equal
assert signed_normal_transaction_raw == signed_normal_signature_transaction_raw

# Submit normal transaction raw
# print("\nSubmitted Normal Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_normal_transaction_raw  # Or signed_normal_signature_transaction_raw
# ), indent=4))
