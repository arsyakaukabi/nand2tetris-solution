# Project 01 Solution Notes

Dokumen ini merangkum implementasi `training/project_01` dan mirror ke `web-ide/projects/src/project_01`.

## Gate Composition

- `Not`: `Nand(in, in)`
- `And`: `Not(Nand(a,b))`
- `Or`: De Morgan (`Not(And(Not(a), Not(b)))`)
- `Xor`: `(a & !b) | (!a & b)`
- `Mux`: `(a & !sel) | (b & sel)`
- `DMux`: `a = in & !sel`, `b = in & sel`

## Wide/Way Gates

- `Not16`, `And16`, `Or16`, `Mux16`: bitwise per index `0..15`
- `Or8Way`: tree reduction dari 8 input
- `Mux4Way16`: 3x `Mux16` (dua level)
- `Mux8Way16`: 2x `Mux4Way16` + 1x `Mux16`
- `DMux4Way`: 3x `DMux` (split by `sel[1]`, lalu `sel[0]`)
- `DMux8Way`: 1x `DMux` + 2x `DMux4Way`

## Cara Verifikasi

Di Hardware Simulator (desktop/online), load masing-masing `.tst` dan pastikan match ke `.cmp`.

Contoh:

1. Load `training/project_01/And.tst`
2. Run script
3. Pastikan output sama dengan `training/project_01/And.cmp`

Ulangi untuk semua chip selain `Nand`.
