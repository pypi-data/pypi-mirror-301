import re
from typing import Any
from urllib.parse import quote, unquote

key_stringify_regexp = re.compile(r"([=:@$/])")
value_stringify_regexp = re.compile(r"([&;/])")
key_parse_regexp = re.compile(r"[=:@$]")
value_parse_regexp = re.compile(r"[&;]")


__all__ = ["stringify", "parse"]


def encode_string(value, regexp) -> str:
    escaped = re.sub(regexp, lambda match: "/" + match.group(0), value)
    return quote(escaped, safe="~@#$&()*!+=:;,?/\'")


def trim(res):
    return res.rstrip(";") if isinstance(res, str) else res


def stringify(value) -> str:
    def _stringify(value) -> str:
        if value is None:
            return ":null"
        if isinstance(value, bool):
            return ":" + str(value).lower()
        if isinstance(value, (int, float)):
            return ":" + str(value)

        res = []

        if isinstance(value, list):
            for item in value:
                res.append(_stringify(item))
            return "@" + "&".join(res) + ";"

        if isinstance(value, dict):
            for k, v in value.items():
                val = _stringify(v)
                res.append(encode_string(k, key_stringify_regexp) + val)
            return "$" + "&".join(res) + ";"

        return "=" + encode_string(str(value), value_stringify_regexp)

    return trim(_stringify(value))


def parse(input_str) -> Any:
    pos = 0
    input_str = unquote(input_str)

    def _read_token(regexp):
        nonlocal pos
        token = ""
        while pos < len(input_str):
            if input_str[pos] == "/":
                pos += 1
                if pos == len(input_str):
                    token += ";"
                    break
            elif regexp.match(input_str[pos]):
                break
            token += input_str[pos]
            pos += 1
        return token

    def _parse_token() -> Any:
        nonlocal pos
        token_type = input_str[pos]
        pos += 1

        if token_type == "=":
            return _read_token(value_parse_regexp)

        if token_type == ":":
            value = _read_token(value_parse_regexp)
            if value == "true":
                return True
            elif value == "false":
                return False
            elif value == "null":
                return None
            return float(value)

        res = []

        if token_type == "@":
            if pos < len(input_str) and input_str[pos] != ";":
                while True:
                    res.append(_parse_token())
                    if pos >= len(input_str) or input_str[pos] == ";":
                        break
                    pos += 1
            pos += 1
            return res

        if token_type == "$":
            res = {}
            if pos < len(input_str) and input_str[pos] != ";":
                while True:
                    name = _read_token(key_parse_regexp)
                    res[name] = _parse_token()
                    if pos >= len(input_str) or input_str[pos] == ";":
                        break
                    pos += 1
            pos += 1
            return res

        raise ValueError("Unexpected char " + token_type)

    return _parse_token()
