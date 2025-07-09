import itertools
import bip32utils
from mnemonic import Mnemonic
from check_balance import check_btc_balance
from multiprocessing import Pool, cpu_count, Value
import argparse
import time

mnemo = Mnemonic("english")

# Define the template: 12 elements, empty strings mean unknowns
# Example: word 0 is "voice", word 3 is "rocket", word 6 is "magic"
seed_template = [
    "voice", "", "", "rocket", "", "", "magic", "", "", "", "", ""
]

# All possible words (original unordered set)
unordered_words = [
    "voice", "yellow", "satoshi", "grace", "magic", "grace",
    "invite", "rocket", "umbrella", "job", "quiz", "eager"
]

assert len(seed_template) == 12, "Seed template must have exactly 12 positions"

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

def init_globals(counter):
    global progress_counter
    progress_counter = counter

def try_permutation(perm):
    global progress_counter
    with progress_counter.get_lock():
        progress_counter.value += 1
        current = progress_counter.value

    if current % 1000 == 0:
        print(f"[⏳] Tried {current:,} permutations...")

    mnemonic = " ".join(perm)
    if not is_valid_mnemonic(mnemonic):
        return None

    seed = mnemonic_to_seed(mnemonic)
    address = derive_address_from_seed(seed)
    balance = check_btc_balance(address)

    if balance and balance["balance"] > 0:
        return {
            "mnemonic": mnemonic,
            "address": address,
            "balance": balance["balance"]
        }
    return None

def filled_mnemonics(perms, template, unknown_slots):
    for perm in perms:
        temp = template[:]
        for idx, word in zip(unknown_slots, perm):
            temp[idx] = word
        yield temp

def main():
    parser = argparse.ArgumentParser(description="Brute-force BIP-39 seed phrase permutations.")
    parser.add_argument("--limit", type=int, help="Maximum number of permutations to try")
    args = parser.parse_args()

    # Determine known and unknown positions
    known_positions = {i: w for i, w in enumerate(seed_template) if w}
    unknown_slots = [i for i in range(12) if i not in known_positions]
    unknown_words = unordered_words[:]
    for w in known_positions.values():
        if w in unknown_words:
            unknown_words.remove(w)

    print(f"[📌] Known words at positions: {known_positions}")
    print(f"[🔄] Permuting {len(unknown_words)} words across {len(unknown_slots)} positions")

    perms = itertools.permutations(unknown_words)
    if args.limit:
        perms = itertools.islice(perms, args.limit)
        print(f"[⚡] Limiting to {args.limit:,} permutations")

    cpu_cores = cpu_count()
    print(f"[⚙️] Using {cpu_cores} CPU cores")

    counter = Value('i', 0)

    with Pool(processes=cpu_cores, initializer=init_globals, initargs=(counter,)) as pool:
        for result in pool.imap_unordered(try_permutation, filled_mnemonics(perms, seed_template, unknown_slots), chunksize=100):
            if result:
                print("\n[💥] MATCH FOUND!")
                print(f"[Mnemonic] {result['mnemonic']}")
                print(f"[Address] {result['address']}")
                print(f"[Balance] {result['balance']} sats")
                pool.terminate()
                break

    print("\n✅ Done.")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\n⏱ Finished in {time.time() - start:.2f} seconds")
