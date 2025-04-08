from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)

# Configuration du logging pour le debug
logging.basicConfig(level=logging.INFO)

# URLs des APIs pour récupérer les données des wallets
API_URLS = {
    "btc": "https://api.blockcypher.com/v1/btc/main/addrs/",
    "eth": "https://api.blockcypher.com/v1/eth/main/addrs/",
    "usdt": "https://api.etherscan.io/api?module=account&action=balance&address="  # À compléter avec une API key si besoin
}


# ✅ PAGE D'ACCUEIL
@app.route("/")
def index():
    return render_template("index.html")


# ✅ PAGE SOLDE
@app.route("/solde", methods=["GET", "POST"])
def solde():
    balance = None
    error = None

    if request.method == "POST":
        crypto_type = request.form.get("crypto-type")
        address = request.form.get("wallet-address")

        if not address:
            error = "Adresse de wallet requise."
        elif crypto_type not in API_URLS:
            error = "Type de crypto-monnaie non supporté."
        else:
            try:
                url = f"{API_URLS[crypto_type]}{address}"
                logging.info(f"Fetching balance from URL: {url}")
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                # Pour BTC et ETH, on divise par 1e8 (satoshi/wei)
                balance_raw = data.get("final_balance", 0)
                balance_value = balance_raw / 1e8
                balance = f"{balance_value:.8f} {crypto_type.upper()}"
            except Exception as e:
                logging.error(f"Erreur lors de la récupération du solde: {e}")
                error = "Erreur lors de la récupération du solde."

    return render_template("solde.html", balance=balance, error=error)


# ✅ PAGE TRANSACTIONS
@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    transactions = []
    error = None

    if request.method == "POST":
        address = request.form.get("wallet-address")

        if not address:
            error = "Adresse de wallet requise."
        else:
            try:
                url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full"
                logging.info(f"Fetching transactions from URL: {url}")
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                for tx in data.get("txs", []):
                    output_addresses = tx.get("outputs", [{}])[0].get("addresses", [])
                    tx_type = "Reçu" if address in output_addresses else "Envoyé"
                    amount = sum(output["value"] for output in tx.get("outputs", [])) / 1e8
                    date = tx.get("confirmed", "Inconnu")
                    transactions.append({
                        "type": tx_type,
                        "amount": f"{amount:.8f}",
                        "date": date
                    })
            except Exception as e:
                logging.error(f"Erreur lors de la récupération des transactions: {e}")
                error = "Impossible de récupérer l'historique des transactions."

    return render_template("transactions.html", transactions=transactions, error=error)


# ✅ PAGE SCANNER
@app.route("/scanner")
def scanner():
    return render_template("scanner.html")


# ✅ PAGE FACTURE
@app.route("/factures")
def facture():
    return render_template("factures.html")


# ✅ LANCEMENT DE L'APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
