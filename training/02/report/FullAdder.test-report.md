# nand2tetris Test Report: FullAdder

- Generated: 2026-02-14T05:38:59.129Z
- Directory: `/Users/arsyakaukabi/Desktop/nand2tetris/training/02/project_02`
- Status: **PASS**

## Pipeline

| Step | Status |
| --- | --- |
| Parse HDL | PASS |
| Parse TST | PASS |
| Build Chip | PASS |
| Build Test | PASS |
| Compare with CMP | PASS |

## Output

```text
| a | b | c |sum|carry|
| 0 | 0 | 0 | 0 |  0  |
| 0 | 0 | 1 | 1 |  0  |
| 0 | 1 | 0 | 1 |  0  |
| 0 | 1 | 1 | 0 |  1  |
| 1 | 0 | 0 | 1 |  0  |
| 1 | 0 | 1 | 0 |  1  |
| 1 | 1 | 0 | 0 |  1  |
| 1 | 1 | 1 | 1 |  1  |
```

## Expected

```text
| a | b | c |sum|carry|
| 0 | 0 | 0 | 0 |  0  |
| 0 | 0 | 1 | 1 |  0  |
| 0 | 1 | 0 | 1 |  0  |
| 0 | 1 | 1 | 0 |  1  |
| 1 | 0 | 0 | 1 |  0  |
| 1 | 0 | 1 | 0 |  1  |
| 1 | 1 | 0 | 0 |  1  |
| 1 | 1 | 1 | 1 |  1  |
```
