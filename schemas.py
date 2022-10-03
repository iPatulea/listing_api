from marshmallow import Schema, ValidationError, fields, utils

from currencies import CURRENCIES
from markets import MARKETS


# Custom field to check if currency code is valid
class CurrencyField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            CURRENCIES.get_by_code(value)
            return utils.ensure_text_type(value)
        except Exception:
            codes = CURRENCIES.__PER_CODE__
            raise ValidationError(f"Choose one of the following: {*codes,}")


# Custom field to check if market code is valid
class MarketField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            MARKETS.get_by_code(value)
            return utils.ensure_text_type(value)
        except Exception:
            codes = MARKETS.__PER_CODE__
            raise ValidationError(f"Choose one of the following: {*codes,}")


# Custom schema to check POST / PUT body input
class ListingSchema(Schema):
    title = fields.String(data_key="title")
    base_price = fields.Integer(data_key="base_price", strict=True)
    currency = CurrencyField(data_key="currency")
    market = MarketField(data_key="market")
    host_name = fields.String(required=False, data_key="host_name")

    def __init__(self, required=True, **kwargs):
        super().__init__(**kwargs)
        self.fields["title"].required = required
        self.fields["base_price"].required = required
        self.fields["currency"].required = required
        self.fields["market"].required = required
