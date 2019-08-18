from flask import jsonify
from schema import Schema

from cazart import Cazart

app = Cazart(__name__)


@app.route("/", schema=Schema({"name": str}))
def root(res):
    print(res)
    return jsonify(success=True)


def main():
    app.flask.run()


if __name__ == "__main__":
    main()
