# nand2tetris Test Report: Inc16

- Generated: 2026-02-14T05:38:59.624Z
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
|        in        |       out        |
| 0000000000000000 | 0000000000000001 |
| 1111111111111111 | 0000000000000000 |
| 0000000000000101 | 0000000000000110 |
| 1111111111111011 | 1111111111111100 |
```

## Expected

```text
|        in        |       out        |
| 0000000000000000 | 0000000000000001 |
| 1111111111111111 | 0000000000000000 |
| 0000000000000101 | 0000000000000110 |
| 1111111111111011 | 1111111111111100 |
```
