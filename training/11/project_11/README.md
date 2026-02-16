# Project 11 - JackCompiler (Jack -> VM)

Implementasi compiler:

- `training/11/project_11/JackCompiler.py`

## Fitur

- Input:
  - satu file `.jack`, atau
  - satu folder berisi banyak `.jack`
- Output:
  - satu file `.vm` untuk setiap `.jack`
- Mendukung code generation penuh Project 11:
  - class/function/method/constructor
  - `let`, `if`, `while`, `do`, `return`
  - expression + unary operator
  - string constants (`String.new` + `String.appendChar`)
  - array access dan array assignment
  - method call implicit (`do f(...)`) dan explicit (`obj.m(...)`, `Class.f(...)`)

## Cara pakai

### Compile satu folder

```bash
python3 training/11/project_11/JackCompiler.py training/11/project_11/Pong
```

### Compile satu file

```bash
python3 training/11/project_11/JackCompiler.py training/11/project_11/Seven/Main.jack
```

## Program yang sudah di-compile

- `Seven`
- `ConvertToBin`
- `Square`
- `Average`
- `Pong`
- `ComplexArrays`
