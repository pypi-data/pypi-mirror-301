# -*- coding: utf-8 -*-
import re
import typing

import typesystem

from arkindex.schema.openapi import OPEN_API, OpenAPI

ENCODING_CHOICES = ["json", "yaml", None]

# The regexs give us a best-guess for the encoding if none is specified.
# They check to see if the document looks like it is probably a YAML object or
# probably a JSON object. It'll typically be best to specify the encoding
# explicitly, but this should do for convenience.
INFER_YAML = re.compile(r"^([ \t]*#.*\n|---[ \t]*\n)*\s*[A-Za-z0-9_-]+[ \t]*:")
INFER_JSON = re.compile(r'^\s*{\s*"[A-Za-z0-9_-]+"\s*:')


def validate(schema: typing.Union[dict, str, bytes], encoding: str = None):
    if not isinstance(schema, (dict, str, bytes)):
        raise ValueError("schema must be either str, bytes, or dict.")
    if encoding not in ENCODING_CHOICES:
        raise ValueError(f"encoding must be one of {ENCODING_CHOICES!r}")

    if isinstance(schema, bytes):
        schema = schema.decode("utf8", "ignore")

    if isinstance(schema, str):
        if encoding is None:
            if INFER_YAML.match(schema):
                encoding = "yaml"
            elif INFER_JSON.match(schema):
                encoding = "json"
            else:
                text = "Could not determine if content is JSON or YAML."
                code = "unknown_encoding"
                position = typesystem.Position(line_no=1, column_no=1, char_index=0)
                raise typesystem.ParseError(text=text, code=code, position=position)

        tokenize = {"yaml": typesystem.tokenize_yaml, "json": typesystem.tokenize_json}[
            encoding
        ]
        token = tokenize(schema)
        value = token.value
    else:
        token = None
        value = schema

    if token is not None:
        value = typesystem.validate_with_positions(token=token, validator=OpenAPI)
    else:
        value = OPEN_API.validate(value)

    return OpenAPI().load(value)
