import httpx


def get_usd_rubble_rate() -> float:
    data = httpx.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return data['Valute']['USD']['Value']
