# Project 12 - Jack OS

Implementasi kelas OS di folder ini:

- `Array.jack`
- `Keyboard.jack`
- `Math.jack`
- `Memory.jack`
- `Output.jack`
- `Screen.jack`
- `String.jack`
- `Sys.jack`

## Cara compile test folder

Contoh:

```bash
nand2tetris compile training/12/project_12/MathTest --dst training/12/project_12/MathTest
```

Lakukan pola yang sama untuk folder test lain (`ArrayTest`, `MemoryTest`, `StringTest`, dll).

## Verifikasi yang sudah dijalankan

Dengan VM test harness:
- `MathTest` pass
- `ArrayTest` pass
- `MemoryTest` pass
- `MemoryDiag` pass secara diagnostik (`RAM[17000]` mencapai `100`, artinya test flow selesai)
