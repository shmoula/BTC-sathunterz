import requests

def check_btc_balance(address):
    """
    Checks BTC address balance using Blockstream.info.
    Returns dict with balance info or None on error.
    """
    url = f"https://blockstream.info/api/address/{address}"
    try:
        response = requests.get(url)
        data = response.json()

        total_received = data.get("chain_stats", {}).get("funded_txo_sum", 0)
        total_sent = data.get("chain_stats", {}).get("spent_txo_sum", 0)
        balance = data.get("chain_stats", {}).get("balance", 0)

        return {
            "received": total_received,
            "sent": total_sent,
            "balance": balance
        }
    except Exception as e:
        print(f"[!] Error checking balance: {e}")
        return None
