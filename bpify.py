from flask import Flask, jsonify, request

from listings_api import blueprint
from markets import MARKETS

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.route("/test_flask", methods=["GET", "POST"])
def test_flask():
    """Example to show how to use Flask and extract information from the incoming request. It is not intended to be
    the only way to do things with Flask, rather more a way to help you not spend too much time on Flask.

    Ref: http://flask.palletsprojects.com/en/1.1.x/

    Try to make those requests: curl "http://localhost:5000/test_flask?first=beyond&last=pricing" curl
    "http://localhost:5000/test_flask" -H "Content-Type: application/json" -X POST -d '{"first":"beyond",
    "last":"pricing"}'

    """
    # This contains the method used to access the route, such as GET or POST, etc
    method = request.method

    # Query parameters
    # It is a dict like object
    # Ref: https://flask.palletsprojects.com/en/1.1.x/api/?highlight=args#flask.Request.args
    query_params = request.args
    query_params_serialized = ", ".join(f"{k}: {v}" for k, v in query_params.items())

    # Get the data as JSON directly
    # If the mimetype does not indicate JSON (application/json, see is_json), this returns None.
    # Ref: https://flask.palletsprojects.com/en/1.1.x/api/?highlight=get_json#flask.Request.get_json
    data_json = request.get_json()

    return jsonify(
        {
            "method": method,
            "query_params": query_params_serialized,
            "data_json": data_json,
        }
    )


@app.route("/markets", methods=["GET"])
def markets():
    print(MARKETS.__PER_CODE__)
    return jsonify([market.to_dict() for market in MARKETS.get_all()])
