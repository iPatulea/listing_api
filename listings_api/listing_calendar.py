import json
import logging
import os

from flask import jsonify, request

from currencies import CURRENCIES
from markets import MARKETS
from utils import Utils

from . import blueprint


@blueprint.route("/listings/<int:id>/calendar", methods=["GET"])
def get_calendar(id):
    # check if file exists
    if not os.path.exists("data.json"):
        return Utils.return_404()
    with open("data.json", "r") as f:
        data = f.read()
        records = json.loads(data)

    record = next((x for x in records if x["id"] == id), None)
    if not record:
        return Utils.return_404()

    # check if currency is given as parameter, check if code is valid, convert base price to the given currency
    if request.args.get("currency", type=str):
        try:
            currency_filter = CURRENCIES.get_by_code(
                request.args.get("currency", type=str).upper()
            ).code
            record["base_price"] = CURRENCIES.exchange(
                record["currency"], currency_filter, amount=record["base_price"]
            )
            record["currency"] = currency_filter
        except Exception as e:
            logging.error(e)
            codes = CURRENCIES.__PER_CODE__
            return (
                jsonify({"currency": [f"Choose from the following: {*codes,}"]}),
                400,
            )

    # go through days, get current price for each day/listing, create the calendar and return it
    date = datetime.today()
    calendar = []
    for i in range(MARKETS.CALENDAR_DAYS):
        current_price = int(
            MARKETS.get_current_price_multiple(record["market"], date.weekday())
            * record["base_price"]
        )
        current_day = {
            "date": date.strftime("%Y-%m-%d"),
            "price": current_price,
            "currency": record["currency"],
        }
        calendar.append(current_day)
        date += timedelta(days=1)
    return jsonify(calendar)
