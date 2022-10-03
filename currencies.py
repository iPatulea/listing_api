import time
from dataclasses import asdict, dataclass

import requests


@dataclass
class Currency:
    code: str
    name: str
    symbol: str

    def to_dict(self):
        return asdict(self)


class CURRENCIES:
    # Codes
    USD = "USD"
    EUR = "EUR"
    JPY = "JPY"
    ILS = "ILS"
    AUD = "AUD"

    # Define all currencies
    __ALL__ = [
        Currency(USD, "United States Dollar", "$"),
        Currency(EUR, "Euro", "€"),
        Currency(JPY, "Japanese Yen", "¥"),
        Currency(ILS, "Israeli shekel", "₪"),
        Currency(AUD, "Australian Dollar", "A$"),
    ]
    # Organize per code for convenience
    __PER_CODE__ = {currency.code: currency for currency in __ALL__}

    # openexchangerates app_id, exchange rates, last timestamp, refresh time (s)
    # openexchangerates refreshes hourly
    __APP_ID = "fb57b24cd16b46c99788647d9218056f"
    EXCHANGE_RATES = None
    EXCHANGE_TIMESTAMP = None
    EXCHANGE_REFRESH = 3600

    @classmethod
    def get_all(cls):
        return cls.__ALL__

    @classmethod
    def get_by_code(cls, code):
        if code not in cls.__PER_CODE__:
            raise Exception(f"Currency with code={code} does not exist")
        return cls.__PER_CODE__[code]

    @classmethod
    def __call_openexchangerates(cls):
        base = cls.USD
        openexchangerates_url = f"https://openexchangerates.org/api/latest.json?app_id={cls.__APP_ID}&base={base}"
        response = requests.get(openexchangerates_url).json()
        cls.EXCHANGE_RATES = response["rates"]
        cls.EXCHANGE_TIMESTAMP = response["timestamp"]

    @classmethod
    def exchange(cls, from_currency, to_currency, *, amount=1):
        if (
            not cls.EXCHANGE_RATES
            or time.time() - cls.EXCHANGE_TIMESTAMP > cls.EXCHANGE_REFRESH
        ):
            cls.__call_openexchangerates()
        from_currency_rate = cls.EXCHANGE_RATES[from_currency]
        to_currency_rate = cls.EXCHANGE_RATES[to_currency]
        return int(amount * (to_currency_rate / from_currency_rate))
