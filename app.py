from flask import Flask, request, render_template, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for message flashing

# Dictionary mapping currency codes to symbols
currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "RUB":  "₽",
    # Add more currencies as needed
}

def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    return data['rates'][to_currency]

def convert_currency(amount, from_currency, to_currency):
    rate = get_exchange_rate(from_currency, to_currency)
    return amount * rate

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency'].upper()
        to_currency = request.form['to_currency'].upper()

        if from_currency not in currency_symbols or to_currency not in currency_symbols:
            raise ValueError("Currency symbol doesn't match")

        converted_amount = convert_currency(amount, from_currency, to_currency)
        symbol = currency_symbols.get(to_currency, "")
        return render_template('result.html', converted_amount=f"{symbol}{converted_amount}")
    except ValueError as e:
        flash(str(e))
        return render_template('index.html')
    except Exception as e:
        flash("An error occurred during conversion.")
        return render_template('index.html')
