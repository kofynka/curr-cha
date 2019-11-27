from flask import render_template, url_for, flash, redirect, request, jsonify
from currency_changer import app
from currency_changer.curr_cha_api import get_rates
from curr_cha import change_rates, currencies, zero_format


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    return render_template('home.html', title='Home', currencies=currencies)


@app.route("/change/<amount>/<currency>", methods=['GET', 'POST'])
def change(amount, currency):
    output = change_rates(amount=amount, input_currency=currency)
    full_output = {'input':{'amount':amount, 'currency':currency},'output':output}
    return jsonify(full_output)
