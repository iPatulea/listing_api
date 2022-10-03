import json
import os

from flask import jsonify, request
from marshmallow import ValidationError

from schemas import ListingSchema
from utils import Utils

from . import blueprint


@blueprint.route("/listings/<int:id>", methods=["GET"])
def _get_(id):
    # check if file exists
    if not os.path.exists("data.json"):
        return Utils.return_404()
    # read data from file
    with open("data.json", "r") as f:
        data = f.read()
        records = json.loads(data)

    # return listing or 404
    result = next((x for x in records if x["id"] == id), None)
    if result:
        return result
    return Utils.return_404()


@blueprint.route("/listings/<int:id>", methods=["PUT"])
def _put_(id):
    # check if file exists
    if not os.path.exists("data.json"):
        return Utils.return_404()
    # check if input is a valid JSON
    try:
        request_data = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        return jsonify({"error": "Invalid input"}), 400

    # check if input validates schema
    schema = ListingSchema(required=False)
    try:
        __input__ = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_records = []
    found = None
    with open("data.json", "r") as f:
        data = f.read()
        records = json.loads(data)

    # after the listing is found and updated, check if currency matches the market if not convert
    for record in records:
        if record["id"] == id:
            for key in __input__.keys():
                record[key] = __input__[key]
            Utils.check_record_currency(record)
            found = record
        new_records.append(record)

    # if found, write the updated listings and return, otherwise 404
    if found:
        with open("data.json", "w") as f:
            f.write(json.dumps(new_records, indent=2))
        return found
    else:
        return Utils.return_404()


@blueprint.route("/listings/<int:id>", methods=["DELETE"])
def _delete_(id):
    # check if file exists
    if not os.path.exists("data.json"):
        return Utils.return_404()
    # read the data, if the <int:id> is not found return 404, otherwise update the listings
    with open("data.json", "r") as f:
        data = f.read()
        records = json.loads(data)

    new_records = list(filter(lambda x: x["id"] != id, records))
    if len(records) == len(new_records):
        return Utils.return_404()

    with open("data.json", "w") as f:
        f.write(json.dumps(new_records, indent=2))
    return {"success": "data deleted"}
