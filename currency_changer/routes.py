from flask import render_template, url_for, flash, redirect, request, jsonify
from currency_changer import app
from currency_converter import CurrencyConverter

c = CurrencyConverter(fallback_on_missing_rate=True)

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    currencies = get_currencies()
    return render_template('home.html', title='Home', currencies=currencies)


@app.route("/change/<amount>/<currency>", methods=['GET', 'POST'])
def change(amount, currency):
    amount = float(amount)
    try:
        currencies = get_currencies()
        output = {}
        for i in currencies: 
            change_value = c.convert(amount, currency, i)
            if change_value >= 1:
                change_value = f'{change_value:,.2f}'
                output[i] = change_value
            else:
                change_value = f'{change_value:.3f}'
                output[i] = change_value
        return jsonify({'input':{'amount':amount, 'currency':currency}, 'output':output})
    except:
        return jsonify({'error':'wrong input'})


# delete deprecated, invalid and uninteresting currencies
def get_currencies():
    cset = c.currencies 
    clist = sorted(cset)
    deletes = ['CYP', 'EEK', 'LTL', 'LVL', 'MTL', 'ROL', 'SIT',\
            'SKK', 'TRL', 'IDR', 'ISK', 'MYR', 'PHP', 'RON']
    for i in deletes:
        clist.remove(i)
    return clist
    