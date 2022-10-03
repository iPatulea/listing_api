import json
import logging
import os

from flask import jsonify, request
from marshmallow import ValidationError

from currencies import CURRENCIES
from markets import MARKETS
from schemas import ListingSchema
from utils import Utils

from . import blueprint


@blueprint.route("/listings", methods=["POST"])
def post_listing():
    # check if input is a valid JSON
    try:
        request_data = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        return jsonify({"error": "Invalid input"}), 400

    # check if input validates schema
    schema = ListingSchema()
    try:
        record = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # create / open file
    mode = "r" if os.path.exists("data.json") else "a+"
    with open("data.json", mode) as f:
        data = f.read()

    # adjust listing if currency doesn't match the market and add to file
    if not data or not len(json.loads(data)):
        record["id"] = 1
        records = [record]
    else:
        records = json.loads(data)
        record["id"] = records[len(records) - 1]["id"] + 1
    Utils.check_record_currency(record)
    records.append(record)
    with open("data.json", "w") as f:
        f.write(json.dumps(records, indent=2))
    return record


@blueprint.route("/listings", methods=["GET"])
def get_listings():
    # check if file exists
    if not os.path.exists("data.json"):
        return jsonify([])

    # check if market filter exists and verify if the code provided is valid
    if request.args.get("market", type=str):
        try:
            market_filters = list(
                filter(
                    lambda x: MARKETS.get_by_code(x),
                    request.args.get("market", default="", type=str).split(","),
                )
            )
        except Exception as e:
            logging.error(e)
            codes = MARKETS.__PER_CODE__
            return (
                jsonify({"market": [f"Choose from the following: {*codes,}"]}),
                400,
            )
    else:
        market_filters = None

    # get all base price filters if there are any
    base_price_operators = list(
        filter(lambda x: x in Utils.OPERATORS.keys(), request.args)
    )

    # check if currency parameter exists, return error if base price exists but currency not and
    # check if currency code is valid
    if base_price_operators and not request.args.get("currency", type=str):
        codes = [currency.code for currency in CURRENCIES.get_all()]
        return (
            jsonify(
                {
                    "currency": [
                        f"Missing required parameter, choose one of the following: {*codes,}"
                    ]
                }
            ),
            400,
        )
    elif request.args.get("currency", type=str):
        try:
            currency_arg = CURRENCIES.get_by_code(
                request.args.get("currency", type=str).upper()
            ).code
        except Exception as e:
            logging.error(e)
            codes = CURRENCIES.__PER_CODE__
            return (
                jsonify({"currency": [f"Choose from the following: {*codes,}"]}),
                400,
            )
    else:
        currency_arg = None

    # open file in read mode
    with open("data.json", "r") as f:
        data = f.read()
        records = json.loads(data)

    # return all records if no parameters
    if not market_filters and not currency_arg:
        return jsonify(records)

    filtered_records = []
    for record in records:
        # filter listings in available markets
        if not market_filters or record["market"] in market_filters:
            # append to result if no other parameters
            if not base_price_operators and not currency_arg:
                filtered_records.append(record)
                continue

            # convert record's currency to the currency received as parameter
            record["base_price"] = CURRENCIES.exchange(
                record["currency"], currency_arg, amount=record["base_price"]
            )
            record["currency"] = currency_arg

            # add to result if no base price filtering has been provided
            if not base_price_operators:
                filtered_records.append(record)
                continue

            # go through all given operators and if the listing matches all of them add to result
            conform_base_price = True
            for base_price_operator in base_price_operators:
                try:
                    arg_value = int(request.args.get(base_price_operator, type=int))
                except TypeError:
                    return (
                        jsonify({base_price_operator: ["Value must be Integer"]}),
                        400,
                    )
                if not Utils.OPERATORS[base_price_operator](
                    record["base_price"], arg_value
                ):
                    conform_base_price = False
                    break
            if conform_base_price:
                filtered_records.append(record)
    return jsonify(filtered_records)
