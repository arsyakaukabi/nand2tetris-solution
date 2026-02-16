# nand2tetris Test Report: DMux4Way

- Generated: 2026-02-14T03:35:08.387Z
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
|in | sel  | a | b | c | d |
| 0 |  00  | 0 | 0 | 0 | 0 |
| 0 |  01  | 0 | 0 | 0 | 0 |
| 0 |  10  | 0 | 0 | 0 | 0 |
| 0 |  11  | 0 | 0 | 0 | 0 |
| 1 |  00  | 1 | 0 | 0 | 0 |
| 1 |  01  | 0 | 1 | 0 | 0 |
| 1 |  10  | 0 | 0 | 1 | 0 |
| 1 |  11  | 0 | 0 | 0 | 1 |
```

## Expected

```text
|in | sel  | a | b | c | d |
| 0 |  00  | 0 | 0 | 0 | 0 |
| 0 |  01  | 0 | 0 | 0 | 0 |
| 0 |  10  | 0 | 0 | 0 | 0 |
| 0 |  11  | 0 | 0 | 0 | 0 |
| 1 |  00  | 1 | 0 | 0 | 0 |
| 1 |  01  | 0 | 1 | 0 | 0 |
| 1 |  10  | 0 | 0 | 1 | 0 |
| 1 |  11  | 0 | 0 | 0 | 1 |
```
