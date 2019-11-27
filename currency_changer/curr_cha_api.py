import json, redis, requests

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def get_rates(input_currency):
    rates = load_from_redis(r.get('rates'))
    if rates:
        return rates
    else:
        r.setex('rates', '2', load_to_redis(input_currency))
        rates = load_from_redis(r.get('rates'))
        return rates
    return None
    

def load_to_redis(input_currency):
    try:
        response = requests.get('https://api.exchangeratesapi.io/latest?base=' + f'{input_currency}')
    except Exception as e:
        print(e)
    return json.dumps(response.json())


def load_from_redis(rates: str):
    if rates:
        return json.loads(rates)
    return None

# print(get_rates('EUR'))
