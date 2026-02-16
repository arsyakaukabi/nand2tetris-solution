#!/usr/bin/env python3

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


KEYWORDS = {
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
}

SYMBOLS = set("{}()[].,;+-*/&|<>=~")
OPS = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
UNARY_OPS = {"-", "~"}
KEYWORD_CONSTANTS = {"true", "false", "null", "this"}


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


@dataclass
class Token:
    kind: str
    value: str


class JackTokenizer:
    def __init__(self, source: str) -> None:
        self.source = source

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        text = self.source
        index = 0
        length = len(text)

        while index < length:
            ch = text[index]
            nxt = text[index + 1] if index + 1 < length else ""

            if ch in {" ", "\t", "\r", "\n"}:
                index += 1
                continue

            if ch == "/" and nxt == "/":
                index += 2
                while index < length and text[index] != "\n":
                    index += 1
                continue

            if ch == "/" and nxt == "*":
                index += 2
                while index + 1 < length and not (
                    text[index] == "*" and text[index + 1] == "/"
                ):
                    index += 1
                index += 2
                continue

            if ch == '"':
                index += 1
                start = index
                while index < length and text[index] != '"':
                    index += 1
                tokens.append(Token("stringConstant", text[start:index]))
                index += 1
                continue

            if ch in SYMBOLS:
                tokens.append(Token("symbol", ch))
                index += 1
                continue

            if ch.isdigit():
                start = index
                while index < length and text[index].isdigit():
                    index += 1
                tokens.append(Token("integerConstant", text[start:index]))
                continue

            if ch.isalpha() or ch == "_":
                start = index
                while index < length and (text[index].isalnum() or text[index] == "_"):
                    index += 1
                value = text[start:index]
                kind = "keyword" if value in KEYWORDS else "identifier"
                tokens.append(Token(kind, value))
                continue

            raise ValueError(f"Unexpected character: {ch}")

        return tokens


class CompilationEngine:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0
        self.lines: list[str] = []
        self.indent = 0

    def parse(self) -> str:
        self.compile_class()
        if self.i != len(self.tokens):
            raise ValueError("Unexpected trailing tokens after class parsing")
        return "\n".join(self.lines) + "\n"

    def current(self) -> Token:
        return self.tokens[self.i]

    def peek(self, offset: int = 1) -> Token | None:
        idx = self.i + offset
        if idx >= len(self.tokens):
            return None
        return self.tokens[idx]

    def write_open(self, tag: str) -> None:
        self.lines.append(f'{"  " * self.indent}<{tag}>')
        self.indent += 1

    def write_close(self, tag: str) -> None:
        self.indent -= 1
        self.lines.append(f'{"  " * self.indent}</{tag}>')

    def write_token(self, token: Token) -> None:
        self.lines.append(
            f'{"  " * self.indent}<{token.kind}> {xml_escape(token.value)} </{token.kind}>'
        )

    def eat(self, expected_value: str | None = None, expected_kind: str | None = None) -> Token:
        token = self.current()
        if expected_value is not None and token.value != expected_value:
            raise ValueError(f"Expected '{expected_value}', got '{token.value}'")
        if expected_kind is not None and token.kind != expected_kind:
            raise ValueError(f"Expected kind '{expected_kind}', got '{token.kind}'")
        self.write_token(token)
        self.i += 1
        return token

    def compile_class(self) -> None:
        self.write_open("class")
        self.eat("class")
        self.eat(expected_kind="identifier")
        self.eat("{")
        while self.current().value in {"static", "field"}:
            self.compile_class_var_dec()
        while self.current().value in {"constructor", "function", "method"}:
            self.compile_subroutine_dec()
        self.eat("}")
        self.write_close("class")

    def compile_class_var_dec(self) -> None:
        self.write_open("classVarDec")
        self.eat()  # static|field
        self.compile_type()
        self.eat(expected_kind="identifier")
        while self.current().value == ",":
            self.eat(",")
            self.eat(expected_kind="identifier")
        self.eat(";")
        self.write_close("classVarDec")

    def compile_type(self) -> None:
        token = self.current()
        if token.value in {"int", "char", "boolean"} or token.kind == "identifier":
            self.eat()
            return
        raise ValueError(f"Expected type, got {token.value}")

    def compile_subroutine_dec(self) -> None:
        self.write_open("subroutineDec")
        self.eat()  # constructor|function|method
        if self.current().value == "void":
            self.eat("void")
        else:
            self.compile_type()
        self.eat(expected_kind="identifier")
        self.eat("(")
        self.compile_parameter_list()
        self.eat(")")
        self.compile_subroutine_body()
        self.write_close("subroutineDec")

    def compile_parameter_list(self) -> None:
        self.write_open("parameterList")
        if self.current().value != ")":
            self.compile_type()
            self.eat(expected_kind="identifier")
            while self.current().value == ",":
                self.eat(",")
                self.compile_type()
                self.eat(expected_kind="identifier")
        self.write_close("parameterList")

    def compile_subroutine_body(self) -> None:
        self.write_open("subroutineBody")
        self.eat("{")
        while self.current().value == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.eat("}")
        self.write_close("subroutineBody")

    def compile_var_dec(self) -> None:
        self.write_open("varDec")
        self.eat("var")
        self.compile_type()
        self.eat(expected_kind="identifier")
        while self.current().value == ",":
            self.eat(",")
            self.eat(expected_kind="identifier")
        self.eat(";")
        self.write_close("varDec")

    def compile_statements(self) -> None:
        self.write_open("statements")
        while self.current().value in {"let", "if", "while", "do", "return"}:
            value = self.current().value
            if value == "let":
                self.compile_let()
            elif value == "if":
                self.compile_if()
            elif value == "while":
                self.compile_while()
            elif value == "do":
                self.compile_do()
            else:
                self.compile_return()
        self.write_close("statements")

    def compile_let(self) -> None:
        self.write_open("letStatement")
        self.eat("let")
        self.eat(expected_kind="identifier")
        if self.current().value == "[":
            self.eat("[")
            self.compile_expression()
            self.eat("]")
        self.eat("=")
        self.compile_expression()
        self.eat(";")
        self.write_close("letStatement")

    def compile_if(self) -> None:
        self.write_open("ifStatement")
        self.eat("if")
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        if self.current().value == "else":
            self.eat("else")
            self.eat("{")
            self.compile_statements()
            self.eat("}")
        self.write_close("ifStatement")

    def compile_while(self) -> None:
        self.write_open("whileStatement")
        self.eat("while")
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.write_close("whileStatement")

    def compile_do(self) -> None:
        self.write_open("doStatement")
        self.eat("do")
        self.compile_subroutine_call()
        self.eat(";")
        self.write_close("doStatement")

    def compile_return(self) -> None:
        self.write_open("returnStatement")
        self.eat("return")
        if self.current().value != ";":
            self.compile_expression()
        self.eat(";")
        self.write_close("returnStatement")

    def compile_expression(self) -> None:
        self.write_open("expression")
        self.compile_term()
        while self.current().value in OPS:
            self.eat()
            self.compile_term()
        self.write_close("expression")

    def compile_term(self) -> None:
        self.write_open("term")
        token = self.current()

        if token.kind in {"integerConstant", "stringConstant"}:
            self.eat()
        elif token.kind == "keyword" and token.value in KEYWORD_CONSTANTS:
            self.eat()
        elif token.value in UNARY_OPS:
            self.eat()
            self.compile_term()
        elif token.value == "(":
            self.eat("(")
            self.compile_expression()
            self.eat(")")
        elif token.kind == "identifier":
            next_token = self.peek()
            if next_token and next_token.value == "[":
                self.eat(expected_kind="identifier")
                self.eat("[")
                self.compile_expression()
                self.eat("]")
            elif next_token and next_token.value in {"(", "."}:
                self.compile_subroutine_call()
            else:
                self.eat(expected_kind="identifier")
        else:
            raise ValueError(f"Unexpected term token: {token}")

        self.write_close("term")

    def compile_subroutine_call(self) -> None:
        self.eat(expected_kind="identifier")
        if self.current().value == ".":
            self.eat(".")
            self.eat(expected_kind="identifier")
        self.eat("(")
        self.compile_expression_list()
        self.eat(")")

    def compile_expression_list(self) -> None:
        self.write_open("expressionList")
        if self.current().value != ")":
            self.compile_expression()
            while self.current().value == ",":
                self.eat(",")
                self.compile_expression()
        self.write_close("expressionList")


def write_tokens_xml(tokens: list[Token], output: Path) -> None:
    lines = ["<tokens>"]
    for token in tokens:
        lines.append(f"<{token.kind}> {xml_escape(token.value)} </{token.kind}>")
    lines.append("</tokens>")
    output.write_text("\n".join(lines) + "\n")


def analyze_file(path: Path) -> None:
    source = path.read_text()
    tokens = JackTokenizer(source).tokenize()
    write_tokens_xml(tokens, path.with_name(f"{path.stem}T.xml"))
    parsed = CompilationEngine(tokens).parse()
    path.with_suffix(".xml").write_text(parsed)


def collect_jack_files(input_path: Path) -> list[Path]:
    if input_path.is_file() and input_path.suffix == ".jack":
        return [input_path]
    if input_path.is_dir():
        return sorted(input_path.glob("*.jack"))
    raise SystemExit(f"Unsupported source: {input_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Project 10 JackAnalyzer: emits XxxT.xml and Xxx.xml",
    )
    parser.add_argument("source", help="Path to .jack file or folder containing .jack files")
    args = parser.parse_args()

    input_path = Path(args.source).resolve()
    files = collect_jack_files(input_path)
    if not files:
        raise SystemExit(f"No .jack file found in: {input_path}")

    for file in files:
        analyze_file(file)
        print(f"wrote {file.with_name(f'{file.stem}T.xml')}")
        print(f"wrote {file.with_suffix('.xml')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
