import operator

from currencies import CURRENCIES
from markets import MARKETS


class Utils:
    # Filtering Operators
    OPERATORS = {
        "base_price.e": operator.eq,
        "base_price.gt": operator.gt,
        "base_price.gte": operator.ge,
        "base_price.lt": operator.lt,
        "base_price.lte": operator.le,
    }

    @classmethod
    def return_404(cls):
        return {"error": "data not found"}, 404

    # Verify if the currency of the listing is correct for its market and adjust base price if not
    @classmethod
    def check_record_currency(cls, record):
        market = next((x for x in MARKETS.__ALL__ if x.code == record["market"]), None)
        if record["currency"] != market.currency:
            exchanged_base_price = CURRENCIES.exchange(
                record["currency"], market.currency, amount=record["base_price"]
            )
            record["currency"] = market.currency
            record["base_price"] = exchanged_base_price
