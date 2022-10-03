from dataclasses import asdict, dataclass

from currencies import CURRENCIES, Currency


@dataclass
class Market:
    code: str
    name: str
    currency: Currency

    def to_dict(self):
        return asdict(self)


class MARKETS:
    # Codes
    SAN_FRANCISCO = "san-francisco"
    LISBON = "lisbon"
    PARIS = "paris"
    TOKYO = "tokyo"
    JERUSALEM = "jerusalem"
    BRISBANE = "brisbane"

    # Define all markets
    __ALL__ = [
        Market(SAN_FRANCISCO, "San Francisco", CURRENCIES.USD),
        Market(LISBON, "Lisbon", CURRENCIES.EUR),
        Market(PARIS, "Paris", CURRENCIES.EUR),
        Market(TOKYO, "Tokyo", CURRENCIES.JPY),
        Market(JERUSALEM, "Jerusalem", CURRENCIES.ILS),
        Market(BRISBANE, "Brisbane", CURRENCIES.AUD),
    ]
    # Organize per code for convenience
    __PER_CODE__ = {market.code: market for market in __ALL__}

    # Multiple base price dict (market, weekday): multiple
    MULTIPLE_BASE_PRICE = {
        ("", ""): 1,
        ("", 4): 1.25,
        (PARIS, 5): 1.5,
        (PARIS, 6): 1.5,
        (LISBON, 5): 1.5,
        (LISBON, 6): 1.5,
        (SAN_FRANCISCO, 2): 0.7,
    }

    # How many days the API is returning
    CALENDAR_DAYS = 365

    @classmethod
    def get_all(cls):
        return cls.__ALL__

    @classmethod
    def get_by_code(cls, code):
        if code not in cls.__PER_CODE__:
            raise Exception(f"Market with code={code} does not exist")
        return cls.__PER_CODE__[code]

    # Return base price multiple for each pair of market and weekday
    @classmethod
    def get_current_price_multiple(cls, market, weekday):
        if (market, weekday) in cls.MULTIPLE_BASE_PRICE:
            return cls.MULTIPLE_BASE_PRICE[(market, weekday)]
        if ("", weekday) in cls.MULTIPLE_BASE_PRICE:
            return cls.MULTIPLE_BASE_PRICE[("", weekday)]
        return cls.MULTIPLE_BASE_PRICE[("", "")]
