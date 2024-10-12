from typing import Any

import pytest

from pyurlon.urlon import parse, stringify


@pytest.mark.parametrize(
    "input_data,expected",
    [
        # booleans and none
        (True, ":true"),
        (False, ":false"),
        (None, ":null"),
        # numbers
        (1234567890, ":1234567890"),
        (1.23456789e-13, ":1.23456789e-13"),
        (-9876.54321, ":-9876.54321"),
        (23456789012e66, ":2.3456789012e+76"),
        (0, ":0"),
        (1, ":1"),
        (0.5, ":0.5"),
        (98.6, ":98.6"),
        (99.44, ":99.44"),
        (1066, ":1066"),
        (1e1, ":10.0"),
        (0.1e1, ":1.0"),
        (1e-1, ":0.1"),
        (1, ":1"),
        (2, ":2"),
        (-42, ":-42"),
        # strings
        ("", "="),
        (";", "=/"),
        ("@", "=@"),
        ("/", "=//"),
        ("|", "=%7C"),
        ("&", "=/&"),
        (" ", "=%20"),
        ('"', "=%22"),
        ("\\", "=%5C"),
        ("\b\f\n\r\t", "=%08%0C%0A%0D%09"),
        ("/ & /", "=//%20/&%20//"),
        ("abcdefghijklmnopqrstuvwyz", "=abcdefghijklmnopqrstuvwyz"),
        ("ABCDEFGHIJKLMNOPQRSTUVWYZ", "=ABCDEFGHIJKLMNOPQRSTUVWYZ"),
        ("0123456789", "=0123456789"),
        ("`1~!@#$%^&*()_+-={':[,]}|;.</>?", "=%601~!@#$%25%5E/&*()_+-=%7B':%5B,%5D%7D%7C/;.%3C//%3E?"),
        ("\u0123\u4567\u89AB\uCDEF\uabcd\uef4A", "=%C4%A3%E4%95%A7%E8%A6%AB%EC%B7%AF%EA%AF%8D%EE%BD%8A"),
        ("// /* <!-- --", "=////%20//*%20%3C!--%20--"),
        ("# -- --> */", "=#%20--%20--%3E%20*//"),
        ("@:0&@:0&@:0&:0", "=@:0/&@:0/&@:0/&:0"),
        (
            '{"object with 1 member":["array with 1 element"]}',
            "=%7B%22object%20with%201%20member%22:%5B%22array%20with%201%20element%22%5D%7D",
        ),
        (
            "/\\\"\uCAFE\uBABE\uAB98\uFCDE\ubcda\uef4A\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?",
            "=//%5C%22%EC%AB%BE%EB%AA%BE%EA%AE%98%EF%B3%9E%EB%B3%9A%EE%BD%8A%08%0C%0A%0D%09%601~!@#$%25%5E/&*()_+-=%5B%5D%7B%7D%7C/;:',.//%3C%3E?",
        ),
        # lists
        ([], "@"),
        ([[0]], "@@:0"),
        ([[[[[0]]]]], "@@@@@:0"),
        ([[[[[0], 0]], 0]], "@@@@@:0;&:0;;&:0"),
        ([0, [0, [0, 0]]], "@:0&@:0&@:0&:0"),
        ([None], "@:null"),
        # dictionaries
        ({}, "$"),
        ({"": ""}, "$="),
        ({"a": {"b": 1}, "c": "x"}, "$a$b:1;&c=x"),
        # complex
        ([{}, {}], "@$;&$"),
        ({"foo": [2, {"bar": [4, {"baz": [6, {"deep enough": 7}]}]}]}, "$foo@:2&$bar@:4&$baz@:6&$deep%20enough:7"),
        (
            {
                "num": 1,
                "alpha": "abc",
                "ignore": "me",
                "change": "to a function",
                "toUpper": True,
                "obj": {"nested_num": 50, "alpha": "abc", "nullable": None},
                "arr": [1, 7, 2],
            },
            "$num:1&alpha=abc&ignore=me&change=to%20a%20function&toUpper:true&obj$nested_num:50&alpha=abc&nullable:null;&arr@:1&:7&:2",
        ),
    ],
)
def test_stringify_and_parse(input_data: Any, expected: str) -> None:
    result = stringify(input_data)
    assert result == expected
    result = parse(result)
    assert result == input_data


def test_parse_unexpected_character() -> None:
    with pytest.raises(
        ValueError,
        match=f"Unexpected char \\^"
    ):
        _ = parse("^")
