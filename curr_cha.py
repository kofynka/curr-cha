from currency_changer.curr_cha_api import get_rates
import pprint, click, sys, time


# only valid and interesting currencies already picked and sorted
symbols = {'€': ['EUR'], '$': ['AUD', 'CAD', 'MXN', 'NZD', 'SGD', 'USD'],
         'лв': ['BGN'], 'R$': ['BRL'], 'Fr': ['CHF'], '¥': ['CNY', 'JPY'],
         'Kč': ['CZK'], 'kr': ['DKK', 'NOK', 'SEK'], '£': ['GBP'], 'H$': ['HKD'],
         'kn': ['HRK'], 'Ft': ['HUF'], '₪': ['ILS'], '₹': ['INR'], '₩': ['KRW'],
         'zł': ['PLN'], '₽': ['RUB'], '฿': ['THB'], '₺': ['TRY'], 'R': ['ZAR']}

currencies = []
for val in symbols.values():
    if len(val) > 1:
        for item in val:
          currencies.append(item)  
    else:
        currencies.append(val[0])


def change_rates(amount, input_currency):
    rates = get_rates(input_currency)['rates']
    result = {}
    for key, val in rates.items():
        x = float(amount) * float(val)
        result[key] = x
    return result


@click.command()
@click.option('-a', '--amount', type=float, required=True, help='Amount of currency you want to change.')
@click.option('-in', '--input_currency', type=str, required=True, help='From what currency (3 letters or currency symbol)')
@click.option('-out', '--output_currency', type=str, required=False, help='To what currency (3 letters or currency symbol) leave out this param to convert to all currencies')
def change(amount, input_currency, output_currency):
    """
    This is simple CLI app for changing currencies
    """
    output = {}
    input_currency = handle_input(input_currency)
    

    # if there is param with output_currency
    if output_currency:
        output_currency = handle_output(output_currency)

        # because api doesn't return eur to eur rate
        if input_currency == output_currency:
            print('From currency to same currency is not possible')
            sys.exit()

        value = change_rates(amount, input_currency)[output_currency]
        changed_value = zero_format(value)
        output[output_currency] = changed_value
    else:
        print('Set output currency to ALL!')
        output = change_rates(amount, input_currency)

    full_output = {'input':{'amount':amount, 'currency':input_currency},'output':output}
    # print nicely
    pprint.pprint(full_output)
    return full_output
    # click.echo(full_output)


def handle_input(input_currency):
    input_currency = finder(input_currency)
    print('Got input currency!')
    return input_currency


def handle_output(output_currency):
    output_currency = finder(output_currency)
    print('Got output currency!')
    return output_currency


def finder(output_currency):
    x = output_currency 
    # if symbol try to find it
    if len(x) < 3:
        # looking for key with same symbol and if there is puts in list
        x = symbols.get(x)
        if x:
            # if there are more currencies with same symbol
            if len(x) > 1:
                answer = input('There are more currencies with that symbol please specify from following:{0}\n (should be 3 letters)\n'.format(x)).upper()
                if answer in x:
                    x = answer.upper()
                    return x
                else:
                    print("Come on! That wasn't so hard to do. ;)")
                    sys.exit()
            else:
                # if only one element in list return it as string
                return ''.join(x)
        else:
            print("I didn't found your symbol")
            sys.exit()
    # wrong input
    elif len(x) > 3:
        print("Valid input and output is just 3 letters or currency symbol")
        sys.exit()
    # actual input was 3 letters
    else:
        x = x.upper()
        for key, val in symbols.items():
            if x in val:
                return x
        else:
            print("I am sorry but that currency is not in our database. :(")
            sys.exit()


def zero_format(value):
    # if the result is smaller than 1 format 4 digits after decimal point
    if value >= 1:
        value = f'{value:,.2f}'
    else:
        value = f'{value:.4f}'
    return value


if __name__ == "__main__":
    change()
