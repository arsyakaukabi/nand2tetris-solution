# nand2tetris Test Report: Not16

- Generated: 2026-02-14T03:33:57.316Z
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
|        in        |       out        |
| 0000000000000000 | 1111111111111111 |
| 1111111111111111 | 0000000000000000 |
| 1010101010101010 | 0101010101010101 |
| 0011110011000011 | 1100001100111100 |
| 0001001000110100 | 1110110111001011 |
```

## Expected

```text
|        in        |       out        |
| 0000000000000000 | 1111111111111111 |
| 1111111111111111 | 0000000000000000 |
| 1010101010101010 | 0101010101010101 |
| 0011110011000011 | 1100001100111100 |
| 0001001000110100 | 1110110111001011 |
```
