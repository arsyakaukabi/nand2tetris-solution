# Project 10 - JackAnalyzer (Tokenizer + Syntax Parser)

Implementasi ada di:

- `training/10/project_10/JackAnalyzer.py`

## Fitur

- Input file tunggal `.jack` atau folder berisi banyak `.jack`
- Output token XML: `XxxT.xml`
- Output parsed XML: `Xxx.xml`
- Support grammar Project 10:
  - class / classVarDec / subroutineDec
  - parameterList / subroutineBody / varDec
  - statements (`let`, `if`, `while`, `do`, `return`)
  - expression / term / expressionList
  - array indexing dan subroutine call

## Cara pakai

### Single file

```bash
python3 training/10/project_10/JackAnalyzer.py training/10/project_10/ArrayTest/Main.jack
```

### Folder

```bash
python3 training/10/project_10/JackAnalyzer.py training/10/project_10/Square
```

Analyzer akan menulis file XML di folder yang sama dengan source `.jack`.
