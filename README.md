cazart
======

*Flask + schema = cazart!*

**cazart** is a small helper for writing schematized JSON endpoints with Flask. It rolls
[schema](https://github.com/keleshev/schema) into Flask's `route` decorator, allowing
for one-shot route and schema specification.

## Installation

**cazart** requires Python 3.5 or newer.

```bash
pip3 install cazart
```

## Usage

To use **cazart**, just swap your `Flask` instance out for a `Cazart` one:

```python
from cazart import Cazart

app = Cazart(__name__)
```

You can access all of Flask's baseline functionality (including non-validated routes)
via `app.flask`.

Then, use `app.route` to specify a combination route and schema:

```python
from cazart import Cazart
from schema import Schema, Or

app = Cazart(__name__)


@app.route("/cazart", schema=Schema({"name": Or("alice", "bob", "mary")}))
def cazart(res):
    print(f"my verified payload is {res}!")
    return ("ok", 200)
```

See the [examples](./examples) for full usage examples, including custom error handling
and dispatching to different schemas on a route based on HTTP method.
