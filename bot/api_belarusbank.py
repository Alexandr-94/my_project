import requests
import json
#
def get_exchange_rates(currencies: list, direstion: str, city: str) -> str:
    result = ''
    for currency in currencies:
        s = requests.Session()
        r = s.get(f'https://belarusbank.by/api/kursExchange?city={city.title()}')
        r = json.loads(r.text)
        result += f'{currency.upper()}: {r[0][f"{currency.upper()}_{direstion.lower()}"]} \n'
    return result

if __name__ == '__main__':
    print(get_exchange_rates(['usd', 'eur', 'rub'], 'out', 'минск'))


def get_exchange_rates_convers(currencies: list, direstion: str, city: str) -> str:
    result = ''
    for currency in currencies:
        s = requests.Session()
        r = s.get(f'https://belarusbank.by/api/kursExchange?city={city.title()}')
        r = json.loads(r.text)
        result += f'{currency.upper()}: {r[0][f"{currency.upper()}_{direstion.lower()}"]} \n'
    return result

if __name__ == '__main__':
    print(get_exchange_rates_convers(['usd_eur', 'usd_rub', 'rub_eur'], 'out', 'минск'))
    print(get_exchange_rates_convers(['usd_eur', 'usd_rub', 'rub_eur'], 'in', 'минск'))