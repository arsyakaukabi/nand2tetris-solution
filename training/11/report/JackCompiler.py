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
        i = 0
        n = len(text)

        while i < n:
            ch = text[i]
            nxt = text[i + 1] if i + 1 < n else ""

            if ch in {" ", "\t", "\r", "\n"}:
                i += 1
                continue

            if ch == "/" and nxt == "/":
                i += 2
                while i < n and text[i] != "\n":
                    i += 1
                continue

            if ch == "/" and nxt == "*":
                i += 2
                while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1
                i += 2
                continue

            if ch == '"':
                i += 1
                start = i
                while i < n and text[i] != '"':
                    i += 1
                tokens.append(Token("stringConstant", text[start:i]))
                i += 1
                continue

            if ch in SYMBOLS:
                tokens.append(Token("symbol", ch))
                i += 1
                continue

            if ch.isdigit():
                start = i
                while i < n and text[i].isdigit():
                    i += 1
                tokens.append(Token("integerConstant", text[start:i]))
                continue

            if ch.isalpha() or ch == "_":
                start = i
                while i < n and (text[i].isalnum() or text[i] == "_"):
                    i += 1
                value = text[start:i]
                tokens.append(Token("keyword" if value in KEYWORDS else "identifier", value))
                continue

            raise ValueError(f"Unexpected character: {ch}")

        return tokens


class SymbolTable:
    def __init__(self) -> None:
        self.class_scope: dict[str, tuple[str, str, int]] = {}
        self.subroutine_scope: dict[str, tuple[str, str, int]] = {}
        self.counts = {"static": 0, "field": 0, "arg": 0, "var": 0}

    def start_subroutine(self) -> None:
        self.subroutine_scope.clear()
        self.counts["arg"] = 0
        self.counts["var"] = 0

    def define(self, name: str, var_type: str, kind: str) -> None:
        index = self.counts[kind]
        self.counts[kind] += 1
        entry = (var_type, kind, index)
        if kind in {"static", "field"}:
            self.class_scope[name] = entry
        else:
            self.subroutine_scope[name] = entry

    def var_count(self, kind: str) -> int:
        return self.counts[kind]

    def kind_of(self, name: str) -> str | None:
        entry = self.subroutine_scope.get(name) or self.class_scope.get(name)
        return None if entry is None else entry[1]

    def type_of(self, name: str) -> str | None:
        entry = self.subroutine_scope.get(name) or self.class_scope.get(name)
        return None if entry is None else entry[0]

    def index_of(self, name: str) -> int | None:
        entry = self.subroutine_scope.get(name) or self.class_scope.get(name)
        return None if entry is None else entry[2]


class VMWriter:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write_push(self, segment: str, index: int) -> None:
        self.lines.append(f"push {segment} {index}")

    def write_pop(self, segment: str, index: int) -> None:
        self.lines.append(f"pop {segment} {index}")

    def write_arithmetic(self, command: str) -> None:
        self.lines.append(command)

    def write_label(self, label: str) -> None:
        self.lines.append(f"label {label}")

    def write_goto(self, label: str) -> None:
        self.lines.append(f"goto {label}")

    def write_if(self, label: str) -> None:
        self.lines.append(f"if-goto {label}")

    def write_call(self, name: str, n_args: int) -> None:
        self.lines.append(f"call {name} {n_args}")

    def write_function(self, name: str, n_locals: int) -> None:
        self.lines.append(f"function {name} {n_locals}")

    def write_return(self) -> None:
        self.lines.append("return")

    def output(self) -> str:
        return "\n".join(self.lines) + "\n"


class CompilationEngine:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.i = 0
        self.class_name = ""
        self.symbols = SymbolTable()
        self.vm = VMWriter()
        self.label_counter = 0

    def compile(self) -> str:
        self.compile_class()
        if self.i != len(self.tokens):
            raise ValueError("Unexpected trailing tokens")
        return self.vm.output()

    def current(self) -> Token:
        return self.tokens[self.i]

    def peek(self, offset: int = 1) -> Token | None:
        idx = self.i + offset
        if idx >= len(self.tokens):
            return None
        return self.tokens[idx]

    def eat(self, value: str | None = None, kind: str | None = None) -> Token:
        token = self.current()
        if value is not None and token.value != value:
            raise ValueError(f"Expected '{value}', got '{token.value}'")
        if kind is not None and token.kind != kind:
            raise ValueError(f"Expected {kind}, got {token.kind}")
        self.i += 1
        return token

    def new_label(self, prefix: str) -> str:
        label = f"{self.class_name}_{prefix}_{self.label_counter}"
        self.label_counter += 1
        return label

    def segment_of_kind(self, kind: str) -> str:
        return {
            "static": "static",
            "field": "this",
            "arg": "argument",
            "var": "local",
        }[kind]

    def push_var(self, name: str) -> None:
        kind = self.symbols.kind_of(name)
        if kind is None:
            raise ValueError(f"Unknown variable: {name}")
        index = self.symbols.index_of(name)
        assert index is not None
        self.vm.write_push(self.segment_of_kind(kind), index)

    def pop_var(self, name: str) -> None:
        kind = self.symbols.kind_of(name)
        if kind is None:
            raise ValueError(f"Unknown variable: {name}")
        index = self.symbols.index_of(name)
        assert index is not None
        self.vm.write_pop(self.segment_of_kind(kind), index)

    def compile_class(self) -> None:
        self.eat("class")
        self.class_name = self.eat(kind="identifier").value
        self.eat("{")
        while self.current().value in {"static", "field"}:
            self.compile_class_var_dec()
        while self.current().value in {"constructor", "function", "method"}:
            self.compile_subroutine()
        self.eat("}")

    def compile_type(self) -> str:
        token = self.current()
        if token.value in {"int", "char", "boolean"} or token.kind == "identifier":
            return self.eat().value
        raise ValueError(f"Invalid type: {token.value}")

    def compile_class_var_dec(self) -> None:
        kind = self.eat().value  # static|field
        var_type = self.compile_type()
        name = self.eat(kind="identifier").value
        self.symbols.define(name, var_type, kind)
        while self.current().value == ",":
            self.eat(",")
            name = self.eat(kind="identifier").value
            self.symbols.define(name, var_type, kind)
        self.eat(";")

    def compile_subroutine(self) -> None:
        subroutine_type = self.eat().value  # constructor|function|method
        self.symbols.start_subroutine()
        self.eat()  # return type
        subroutine_name = self.eat(kind="identifier").value

        if subroutine_type == "method":
            self.symbols.define("this", self.class_name, "arg")

        self.eat("(")
        self.compile_parameter_list()
        self.eat(")")
        self.eat("{")

        while self.current().value == "var":
            self.compile_var_dec()

        n_locals = self.symbols.var_count("var")
        full_name = f"{self.class_name}.{subroutine_name}"
        self.vm.write_function(full_name, n_locals)

        if subroutine_type == "constructor":
            n_fields = self.symbols.var_count("field")
            self.vm.write_push("constant", n_fields)
            self.vm.write_call("Memory.alloc", 1)
            self.vm.write_pop("pointer", 0)
        elif subroutine_type == "method":
            self.vm.write_push("argument", 0)
            self.vm.write_pop("pointer", 0)

        self.compile_statements()
        self.eat("}")

    def compile_parameter_list(self) -> None:
        if self.current().value == ")":
            return
        var_type = self.compile_type()
        name = self.eat(kind="identifier").value
        self.symbols.define(name, var_type, "arg")
        while self.current().value == ",":
            self.eat(",")
            var_type = self.compile_type()
            name = self.eat(kind="identifier").value
            self.symbols.define(name, var_type, "arg")

    def compile_var_dec(self) -> None:
        self.eat("var")
        var_type = self.compile_type()
        name = self.eat(kind="identifier").value
        self.symbols.define(name, var_type, "var")
        while self.current().value == ",":
            self.eat(",")
            name = self.eat(kind="identifier").value
            self.symbols.define(name, var_type, "var")
        self.eat(";")

    def compile_statements(self) -> None:
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

    def compile_let(self) -> None:
        self.eat("let")
        name = self.eat(kind="identifier").value
        is_array = self.current().value == "["

        if is_array:
            self.eat("[")
            self.compile_expression()
            self.eat("]")
            self.push_var(name)
            self.vm.write_arithmetic("add")

        self.eat("=")
        self.compile_expression()
        self.eat(";")

        if is_array:
            self.vm.write_pop("temp", 0)
            self.vm.write_pop("pointer", 1)
            self.vm.write_push("temp", 0)
            self.vm.write_pop("that", 0)
        else:
            self.pop_var(name)

    def compile_if(self) -> None:
        self.eat("if")
        self.eat("(")
        self.compile_expression()
        self.eat(")")

        true_label = self.new_label("IF_TRUE")
        false_label = self.new_label("IF_FALSE")
        end_label = self.new_label("IF_END")

        self.vm.write_if(true_label)
        self.vm.write_goto(false_label)
        self.vm.write_label(true_label)

        self.eat("{")
        self.compile_statements()
        self.eat("}")

        if self.current().value == "else":
            self.vm.write_goto(end_label)
            self.vm.write_label(false_label)
            self.eat("else")
            self.eat("{")
            self.compile_statements()
            self.eat("}")
            self.vm.write_label(end_label)
        else:
            self.vm.write_label(false_label)

    def compile_while(self) -> None:
        self.eat("while")
        start_label = self.new_label("WHILE_EXP")
        end_label = self.new_label("WHILE_END")
        self.vm.write_label(start_label)
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.vm.write_arithmetic("not")
        self.vm.write_if(end_label)
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.vm.write_goto(start_label)
        self.vm.write_label(end_label)

    def compile_do(self) -> None:
        self.eat("do")
        self.compile_subroutine_call()
        self.eat(";")
        self.vm.write_pop("temp", 0)

    def compile_return(self) -> None:
        self.eat("return")
        if self.current().value != ";":
            self.compile_expression()
        else:
            self.vm.write_push("constant", 0)
        self.eat(";")
        self.vm.write_return()

    def compile_expression(self) -> None:
        self.compile_term()
        while self.current().value in OPS:
            op = self.eat().value
            self.compile_term()
            self.write_op(op)

    def write_op(self, op: str) -> None:
        mapping = {
            "+": "add",
            "-": "sub",
            "&": "and",
            "|": "or",
            "<": "lt",
            ">": "gt",
            "=": "eq",
        }
        if op in mapping:
            self.vm.write_arithmetic(mapping[op])
        elif op == "*":
            self.vm.write_call("Math.multiply", 2)
        elif op == "/":
            self.vm.write_call("Math.divide", 2)
        else:
            raise ValueError(f"Unsupported operator: {op}")

    def compile_term(self) -> None:
        token = self.current()

        if token.kind == "integerConstant":
            self.vm.write_push("constant", int(self.eat().value))
            return

        if token.kind == "stringConstant":
            value = self.eat().value
            self.vm.write_push("constant", len(value))
            self.vm.write_call("String.new", 1)
            for ch in value:
                self.vm.write_push("constant", ord(ch))
                self.vm.write_call("String.appendChar", 2)
            return

        if token.kind == "keyword" and token.value in {"true", "false", "null", "this"}:
            value = self.eat().value
            if value == "true":
                self.vm.write_push("constant", 0)
                self.vm.write_arithmetic("not")
            elif value in {"false", "null"}:
                self.vm.write_push("constant", 0)
            else:
                self.vm.write_push("pointer", 0)
            return

        if token.value in UNARY_OPS:
            op = self.eat().value
            self.compile_term()
            self.vm.write_arithmetic("neg" if op == "-" else "not")
            return

        if token.value == "(":
            self.eat("(")
            self.compile_expression()
            self.eat(")")
            return

        if token.kind == "identifier":
            nxt = self.peek()
            if nxt and nxt.value == "[":
                name = self.eat(kind="identifier").value
                self.eat("[")
                self.compile_expression()
                self.eat("]")
                self.push_var(name)
                self.vm.write_arithmetic("add")
                self.vm.write_pop("pointer", 1)
                self.vm.write_push("that", 0)
                return
            if nxt and nxt.value in {"(", "."}:
                self.compile_subroutine_call()
                return
            name = self.eat(kind="identifier").value
            self.push_var(name)
            return

        raise ValueError(f"Unexpected term: {token.kind} {token.value}")

    def compile_expression_list(self) -> int:
        count = 0
        if self.current().value == ")":
            return 0
        self.compile_expression()
        count += 1
        while self.current().value == ",":
            self.eat(",")
            self.compile_expression()
            count += 1
        return count

    def compile_subroutine_call(self) -> None:
        first = self.eat(kind="identifier").value
        n_args = 0
        if self.current().value == ".":
            self.eat(".")
            second = self.eat(kind="identifier").value
            kind = self.symbols.kind_of(first)
            if kind is not None:
                # method on object variable
                self.push_var(first)
                type_name = self.symbols.type_of(first)
                assert type_name is not None
                full_name = f"{type_name}.{second}"
                n_args = 1
            else:
                # class function/constructor
                full_name = f"{first}.{second}"
        else:
            # method in current class
            self.vm.write_push("pointer", 0)
            full_name = f"{self.class_name}.{first}"
            n_args = 1

        self.eat("(")
        n_args += self.compile_expression_list()
        self.eat(")")
        self.vm.write_call(full_name, n_args)


def collect_jack_files(path: Path) -> list[Path]:
    if path.is_file() and path.suffix == ".jack":
        return [path]
    if path.is_dir():
        return sorted(path.glob("*.jack"))
    raise SystemExit(f"Unsupported input: {path}")


def compile_file(path: Path) -> None:
    source = path.read_text()
    tokens = JackTokenizer(source).tokenize()
    vm_code = CompilationEngine(tokens).compile()
    path.with_suffix(".vm").write_text(vm_code)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Project 11 JackCompiler: compiles Jack source to VM code.",
    )
    parser.add_argument("source", help="Path to .jack file or folder of .jack files")
    args = parser.parse_args()

    input_path = Path(args.source).resolve()
    files = collect_jack_files(input_path)
    if not files:
        raise SystemExit(f"No .jack files found in: {input_path}")

    for file in files:
        compile_file(file)
        print(f"wrote {file.with_suffix('.vm')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
