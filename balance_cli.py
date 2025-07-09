import argparse
from check_balance import check_btc_balance

def main():
    parser = argparse.ArgumentParser(description="Check balance of a Bitcoin address.")
    parser.add_argument("address", help="Bitcoin address to check")
    args = parser.parse_args()

    print(f"[🔍] Checking balance for address: {args.address}")
    balance = check_btc_balance(args.address)

    if balance:
        print(f"\n[✅] Balance: {balance['balance']} sats")
        print(f"Total Received: {balance['received']} sats")
        print(f"Total Sent: {balance['sent']} sats")
    else:
        print("\n[❌] Failed to retrieve balance.")

if __name__ == "__main__":
    main()
