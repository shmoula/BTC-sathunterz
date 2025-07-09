# Sathunterz Bitcoin Seed Experiments

Welcome to the experimental repository, built for the **SaTHunterz side event at BTC Prague**!

This project was created as a learning exercise to:

✅ Understand BIP-39 Bitcoin seed phrases  
✅ Explore how wallets derive keys and addresses  
✅ Experiment with brute-forcing seed phrase permutations  
✅ Check Bitcoin addresses for balances programmatically

---

## 🚀 What This Project Does

- **btc_seed_cli.py**  
    Generate a random BIP-39 seed phrase and derive:
    - 512-bit seed
    - Master private key
    - First Bitcoin address
    - Check if the address has any sats

- **check_balance.py**  
    Simple function to query Blockstream.info for the balance of a Bitcoin address.

- **balance_cli.py**  
    Standalone CLI tool to check the balance of any Bitcoin address you provide.

- **bruteforce_seed.py**
    Brute-force tool to:
    - Test permutations of an unordered set of seed words
    - Check if derived addresses hold any sats

- **bruteforce_seed_parallel.py**
    The same brute-force tool enhanced with:
    - Use of multiprocessing to speed up
    - Supports pinning known words in known positions
    - Limit the number of permutations for faster testing
    
    
---

## 🛠 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/shmoula/BTC-sathunterz.git
cd BTC-sathunterz
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install mnemonic bip32utils requests
```

---

## ⚙️ How to Use

### Generate a Random Seed Phrase

```bash
python btc_seed_cli.py
```

### Check Balance of a Bitcoin Address

```bash
python balance_cli.py 1YourBitcoinAddressHere
```

### Brute-force Seed Permutations - serial

Run permutations over the given words, one by one:

```bash
python bruteforce_seed.py
```

### Brute-force Seed Permutations - parallel

Run with no limit (⚠️ extremely large permutation space!):

```bash
python bruteforce_seed_parallel.py
```

Or limit to e.g. first 10,000 permutations:

```bash
python bruteforce_seed_parallel.py --limit 10000
```

### Pin Known Words

Edit `bruteforce_seed_parallel.py`:

```python
seed_template = [
    "voice", "", "", "rocket", "", "", "magic", "", "", "", "", ""
]
```

Empty slots will be permuted. Known words stay fixed in their positions.

---

## 🤓 Disclaimer

> This repository was created for educational purposes during the SaTHunterz side event at BTC Prague.  
> **Do not use this software with real funds.**  
> Brute-forcing seed phrases is computationally expensive and practically infeasible for real wallets with strong entropy.
