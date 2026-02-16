# nand2tetris Test Report: DMux

- Generated: 2026-02-14T03:33:47.072Z
- Directory: `/Users/arsyakaukabi/Desktop/nand2tetris/training/project_01`
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
|in |sel| a | b |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
```

## Expected

```text
|in |sel| a | b |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
```
