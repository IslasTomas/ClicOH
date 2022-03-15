import requests


url_api_dollar = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
MAX_INTENTOS = 10


def get_data_from_request_to_dollar_api():

    for i in range(MAX_INTENTOS):
        response = requests.get(url_api_dollar)
        data = response.json()
        if response.status_code == 200:
            data = response.json()
            return data
    raise Exception


def get_dollar_price(type_dollar='Dolar Blue'):
    data = get_data_from_request_to_dollar_api()

    for dollar_data in data:
        if dollar_data['casa']['nombre'] == type_dollar:
            price = dollar_data['casa']['compra']
            return float(price.replace(',', '.'))

    return False
