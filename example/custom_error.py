from flask import abort, jsonify
from schema import Schema

from cazart import Cazart, validation_error

app = Cazart(__name__)


def fatal():
    print(f"oh no! {validation_error}")
    abort(400)


@app.route("/", schema=Schema({"name": str}), error=fatal)
def root(res):
    print(res)
    return jsonify(success=True)


def main():
    app.flask.run()


if __name__ == "__main__":
    main()
