#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


ARITHMETIC_COMMANDS = {
    "add",
    "sub",
    "neg",
    "eq",
    "gt",
    "lt",
    "and",
    "or",
    "not",
}

SEGMENT_BASE = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}


class CodeWriter:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.label_index = 0
        self.file_name = "Sys"

    def set_file_name(self, file_name: str) -> None:
        self.file_name = file_name

    def emit(self, *assembly: str) -> None:
        self.lines.extend(assembly)

    def write_arithmetic(self, command: str) -> None:
        if command == "add":
            self.emit("@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M")
        elif command == "sub":
            self.emit("@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D")
        elif command == "and":
            self.emit("@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M")
        elif command == "or":
            self.emit("@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M")
        elif command == "neg":
            self.emit("@SP", "A=M-1", "M=-M")
        elif command == "not":
            self.emit("@SP", "A=M-1", "M=!M")
        elif command in {"eq", "gt", "lt"}:
            true_label = f"{self.file_name}$TRUE{self.label_index}"
            end_label = f"{self.file_name}$END{self.label_index}"
            self.label_index += 1
            jump = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}[command]
            self.emit(
                "@SP",
                "AM=M-1",
                "D=M",
                "A=A-1",
                "D=M-D",
                f"@{true_label}",
                f"D;{jump}",
                "@SP",
                "A=M-1",
                "M=0",
                f"@{end_label}",
                "0;JMP",
                f"({true_label})",
                "@SP",
                "A=M-1",
                "M=-1",
                f"({end_label})",
            )
        else:
            raise ValueError(f"Unsupported arithmetic command: {command}")

    def push_d_to_stack(self) -> None:
        self.emit("@SP", "A=M", "M=D", "@SP", "M=M+1")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        if command == "push":
            self.write_push(segment, index)
        elif command == "pop":
            self.write_pop(segment, index)
        else:
            raise ValueError(f"Unsupported command type: {command}")

    def write_push(self, segment: str, index: int) -> None:
        if segment == "constant":
            self.emit(f"@{index}", "D=A")
            self.push_d_to_stack()
        elif segment in SEGMENT_BASE:
            base = SEGMENT_BASE[segment]
            self.emit(f"@{base}", "D=M", f"@{index}", "A=D+A", "D=M")
            self.push_d_to_stack()
        elif segment == "temp":
            self.emit("@5", "D=A", f"@{index}", "A=D+A", "D=M")
            self.push_d_to_stack()
        elif segment == "pointer":
            pointer_symbol = "THIS" if index == 0 else "THAT"
            self.emit(f"@{pointer_symbol}", "D=M")
            self.push_d_to_stack()
        elif segment == "static":
            self.emit(f"@{self.file_name}.{index}", "D=M")
            self.push_d_to_stack()
        else:
            raise ValueError(f"Unsupported push segment: {segment}")

    def write_pop(self, segment: str, index: int) -> None:
        if segment in SEGMENT_BASE:
            base = SEGMENT_BASE[segment]
            self.emit(
                f"@{base}",
                "D=M",
                f"@{index}",
                "D=D+A",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
            )
        elif segment == "temp":
            self.emit(
                "@5",
                "D=A",
                f"@{index}",
                "D=D+A",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D",
            )
        elif segment == "pointer":
            pointer_symbol = "THIS" if index == 0 else "THAT"
            self.emit("@SP", "AM=M-1", "D=M", f"@{pointer_symbol}", "M=D")
        elif segment == "static":
            self.emit("@SP", "AM=M-1", "D=M", f"@{self.file_name}.{index}", "M=D")
        else:
            raise ValueError(f"Unsupported pop segment: {segment}")

    def output(self) -> str:
        return "\n".join(self.lines) + "\n"


def parse_vm_file(path: Path) -> list[tuple[str, list[str]]]:
    commands: list[tuple[str, list[str]]] = []
    for raw_line in path.read_text().splitlines():
        line = raw_line.split("//", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        commands.append((parts[0], parts[1:]))
    return commands


def translate_files(vm_files: list[Path], output_path: Path) -> None:
    writer = CodeWriter()

    for vm_file in vm_files:
        writer.set_file_name(vm_file.stem)
        for op, args in parse_vm_file(vm_file):
            if op in ARITHMETIC_COMMANDS:
                writer.write_arithmetic(op)
            elif op in {"push", "pop"}:
                writer.write_push_pop(op, args[0], int(args[1]))
            else:
                raise ValueError(f"Unsupported VM command: {op}")

    output_path.write_text(writer.output())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Project 7 VM Translator (Part I: stack arithmetic + memory access).",
    )
    parser.add_argument("input_path", help="Path to .vm file or folder containing .vm files")
    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    if input_path.is_file() and input_path.suffix == ".vm":
        vm_files = [input_path]
        output_path = input_path.with_suffix(".asm")
    elif input_path.is_dir():
        vm_files = sorted(input_path.glob("*.vm"))
        if not vm_files:
            raise SystemExit(f"No .vm file found in folder: {input_path}")
        output_path = input_path / f"{input_path.name}.asm"
    else:
        raise SystemExit(f"Unsupported path: {input_path}")

    translate_files(vm_files, output_path)
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
