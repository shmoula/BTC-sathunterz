import argparse
from mnemonic import Mnemonic
import bip32utils
from check_balance import check_btc_balance

def generate_mnemonic():
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128)  # 12 words

def mnemonic_to_seed(mnemonic_phrase):
    mnemo = Mnemonic("english")
    return mnemo.to_seed(mnemonic_phrase, passphrase="")

def derive_btc_address(seed):
    # Create BIP32 Root Key
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)

    # Derive BIP44 path: m/44'/0'/0'/0/0
    bip32_child_key = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN)\
                                         .ChildKey(0 + bip32utils.BIP32_HARDEN)\
                                         .ChildKey(0 + bip32utils.BIP32_HARDEN)\
                                         .ChildKey(0)\
                                         .ChildKey(0)

    return {
        "private_key": bip32_child_key.WalletImportFormat(),
        "public_key": bip32_child_key.PublicKey().hex(),
        "address": bip32_child_key.Address()
    }

def main():
    parser = argparse.ArgumentParser(description="Generate Bitcoin BIP-39 seed and address.")
    args = parser.parse_args()

    mnemonic = generate_mnemonic()
    print("\n[Seed Phrase]\n", mnemonic)

    seed = mnemonic_to_seed(mnemonic)
    print("\n[Seed Hex]\n", seed.hex())

    keys = derive_btc_address(seed)
    print("\n[Derived Bitcoin Info]")
    print("Address:", keys["address"])
    print("Public Key:", keys["public_key"])
    print("Private Key (WIF):", keys["private_key"])

    print("\n[Balance Check]")
    balance = check_btc_balance(keys["address"])

    if balance:
        print(f"Balance: {balance['balance']} sats")
        print(f"Total Received: {balance['received']} sats")
        print(f"Total Sent: {balance['sent']} sats")
    else:
        print("Could not check balance.")

if __name__ == "__main__":
    main()
