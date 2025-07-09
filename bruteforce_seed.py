import itertools
from mnemonic import Mnemonic
from check_balance import check_btc_balance
import bip32utils

mnemo = Mnemonic("english")

def is_valid_mnemonic(words):
    return mnemo.check(words)

def mnemonic_to_seed(mnemonic_phrase):
    return mnemo.to_seed(mnemonic_phrase, passphrase="")

def derive_address_from_seed(seed):
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN)\
                                         .ChildKey(0 + bip32utils.BIP32_HARDEN)\
                                         .ChildKey(0 + bip32utils.BIP32_HARDEN)\
                                         .ChildKey(0)\
                                         .ChildKey(0)
    return bip32_child_key.Address()

def main():
    # Replace with your 12 scrambled words
    unordered_words = [
        "voice", "yellow", "satoshi", "grace", "magic", "grace",
        "invite", "rocket", "umbrella", "job", "quiz", "eager"
    ]

    print(f"[🔍] Testing permutations of {len(unordered_words)} words...")

    count = 0
    for perm in itertools.permutations(unordered_words):
        count += 1
        mnemonic = " ".join(perm)
        if not is_valid_mnemonic(mnemonic):
            continue

        print(f"\n[✅] Valid Mnemonic Found: {mnemonic}")
        seed = mnemonic_to_seed(mnemonic)
        address = derive_address_from_seed(seed)

        print(f"[📬] Derived address: {address}")
        balance = check_btc_balance(address)

        if balance and balance["balance"] > 0:
            print(f"[💰] Balance Found! {balance['balance']} sats")
            break
        else:
            print(f"[0️⃣] No balance on {address}")

    print(f"[🧮] Total permutations tested: {count}")

if __name__ == "__main__":
    main()
