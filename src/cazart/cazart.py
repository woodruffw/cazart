from functools import wraps

from flask import Flask, request
from schema import SchemaError
from werkzeug.local import Local, LocalManager

_local = Local()
_local_manager = LocalManager()

bad_json = _local("bad_json")
validation_error = _local("validation_error")


def _fail_on_invalid():
    return (_local.validation_error, 400)


def _update_locals(json, message):
    _local.bad_json = json
    _local.validation_error = message


class Cazart:
    """
    A thin wrapper for Flask and schema, providing schema-validated endpoint decorators.
    """

    def __init__(self, import_name, **kwargs):
        self.import_name = import_name
        self.flask = Flask(import_name, **kwargs)
        _local_manager.make_middleware(self.flask)

    def route(self, rule, *, schema, error=_fail_on_invalid, **kwargs):
        """
        Like ``Flask.route()``, but with an additional schema to validate against.
        Adds two keywords, ``schema`` and ``error``, and passes all other arguments
        to Flask.

        :param schema: The schema to validate against, or a dictionary of HTTP methods to schemas
        :type schema: ``schema.Schema`` or dict
        :param error: The function to call on validation failure
        :type error: function
        """
        if isinstance(schema, dict):
            kwargs["methods"] = schema.keys()

        def wrapper(fn):
            @wraps(fn)
            @self.flask.route(rule, **kwargs)
            def decorated():
                nonlocal schema
                res = request.get_json(force=True, silent=True)
                if res is None:
                    _update_locals(res, "missing or malformed JSON")
                    return error()

                if isinstance(schema, dict):
                    schema = schema.get(request.method)

                try:
                    schema.validate(res)
                except SchemaError as e:
                    _update_locals(res, e.code)
                    return error()
                return fn(res)

            return decorated

        return wrapper
