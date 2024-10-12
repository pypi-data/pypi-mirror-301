"""Contains nip directives."""

import nip.elements
from .constructor import Constructor
from .parser import Parser, ParserError
from .stream import Stream


def insert_directive(right_value, stream: Stream):
    if isinstance(right_value, nip.elements.Value):
        constructor = Constructor()
        path = constructor.construct(right_value)
        assert isinstance(path, str), "Load directive expects path as an argument."
        parser = Parser()
        config = parser.parse(path)  # Document
        return config._value

    elif isinstance(right_value, nip.elements.Args):
        assert len(right_value._value[0]) == 1, "only single positional argument will be treated as config path."
        constructor = Constructor()
        path = constructor.construct(right_value._value[0][0])
        assert isinstance(path, str), "Load directive expects path as first argument."
        parser = Parser()
        parser.link_replacements = right_value._value[1]
        config = parser.parse(path)  # Document
        return config._value

    else:
        raise ParserError(
            stream,
            "string or combination of arg and **kwargs are expected as value of !!insert directive",
        )


_directives = {"insert": insert_directive}


def call_directive(name, right_value, stream: Stream):
    if name not in _directives:
        raise ParserError(stream, f"Unknown parser directive '{name}'.")
    return _directives[name](right_value, stream)
