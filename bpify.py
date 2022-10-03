from flask import Flask, jsonify, request

from listings_api import blueprint
from markets import MARKETS

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.route("/markets", methods=["GET"])
def markets():
    print(MARKETS.__PER_CODE__)
    return jsonify([market.to_dict() for market in MARKETS.get_all()])
