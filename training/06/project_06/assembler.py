#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


JUMP_TO_BITS = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

COMP_TO_BITS = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}


def build_predefined_symbols() -> dict[str, int]:
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }
    for register_index in range(16):
        symbols[f"R{register_index}"] = register_index
    return symbols


def clean_line(line: str) -> str:
    no_comment = line.split("//", 1)[0]
    return no_comment.strip()


def read_instructions(asm_path: Path) -> list[str]:
    instructions: list[str] = []
    for raw_line in asm_path.read_text().splitlines():
        instruction = clean_line(raw_line)
        if instruction:
            instructions.append(instruction)
    return instructions


def first_pass(symbols: dict[str, int], instructions: list[str]) -> list[str]:
    rom_address = 0
    executable_instructions: list[str] = []

    for instruction in instructions:
        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]
            symbols[label] = rom_address
        else:
            executable_instructions.append(instruction)
            rom_address += 1

    return executable_instructions


def dest_bits(dest_mnemonic: str) -> str:
    if not dest_mnemonic:
        return "000"
    has_a = "1" if "A" in dest_mnemonic else "0"
    has_d = "1" if "D" in dest_mnemonic else "0"
    has_m = "1" if "M" in dest_mnemonic else "0"
    return f"{has_a}{has_d}{has_m}"


def encode_a_instruction(symbols: dict[str, int], symbol: str, next_ram: int) -> tuple[str, int]:
    if symbol.isdigit():
        address_value = int(symbol)
    else:
        if symbol not in symbols:
            symbols[symbol] = next_ram
            next_ram += 1
        address_value = symbols[symbol]
    return f"{address_value:016b}", next_ram


def encode_c_instruction(instruction: str) -> str:
    if "=" in instruction:
        dest_mnemonic, remainder = instruction.split("=", 1)
    else:
        dest_mnemonic, remainder = "", instruction

    if ";" in remainder:
        comp_mnemonic, jump_mnemonic = remainder.split(";", 1)
    else:
        comp_mnemonic, jump_mnemonic = remainder, ""

    comp_bits = COMP_TO_BITS[comp_mnemonic]
    destination_bits = dest_bits(dest_mnemonic)
    jump_bits = JUMP_TO_BITS[jump_mnemonic]
    return f"111{comp_bits}{destination_bits}{jump_bits}"


def assemble(asm_path: Path) -> str:
    symbols = build_predefined_symbols()
    raw_instructions = read_instructions(asm_path)
    executable_instructions = first_pass(symbols, raw_instructions)

    next_ram_address = 16
    machine_lines: list[str] = []

    for instruction in executable_instructions:
        if instruction.startswith("@"):
            machine_code, next_ram_address = encode_a_instruction(
                symbols,
                instruction[1:],
                next_ram_address,
            )
            machine_lines.append(machine_code)
        else:
            machine_lines.append(encode_c_instruction(instruction))

    return "\n".join(machine_lines)


def write_hack_file(asm_path: Path) -> Path:
    hack_path = asm_path.with_suffix(".hack")
    hack_path.write_text(assemble(asm_path))
    return hack_path


def find_asm_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.asm") if path.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hack Assembler (Project 6): translate .asm to .hack",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to an .asm file or a folder to process recursively",
    )
    args = parser.parse_args()

    target_path = Path(args.path).resolve()
    asm_files: list[Path]
    if target_path.is_file() and target_path.suffix.lower() == ".asm":
        asm_files = [target_path]
    elif target_path.is_dir():
        asm_files = find_asm_files(target_path)
    else:
        raise SystemExit(f"Unsupported path: {target_path}")

    if not asm_files:
        raise SystemExit("No .asm files found")

    for asm_file in asm_files:
        hack_file = write_hack_file(asm_file)
        print(f"wrote {hack_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
