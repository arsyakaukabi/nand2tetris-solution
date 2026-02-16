# Project 4 Explanation (Machine Language)

Dokumen ini menjelaskan apa yang dikerjakan pada `training/04/project_04`.

## Gambaran Umum

Project 4 fokus ke pemrograman Hack Assembly:

- `Mult.asm`: menghitung perkalian `R0 * R1` dan menyimpan hasil di `R2`.
- `Fill.asm`: membaca keyboard terus-menerus, lalu mengubah seluruh layar menjadi hitam/putih.

Target utama project ini adalah memahami alur low-level:

1. baca nilai dari RAM,
2. proses dengan instruction Hack,
3. tulis balik hasil ke RAM / memory-mapped I/O.

## Penjelasan `Mult.asm`

File: `training/04/project_04/Mult/Mult.asm`

Algoritma yang dipakai adalah **repetitive addition**:

- Inisialisasi `R2 = 0` (akumulator hasil).
- Simpan counter `i = 0`.
- Loop selama `i < R1`:
  - tambah `R0` ke `R2`,
  - naikkan `i`.
- Setelah selesai, program masuk loop akhir tak berhingga (`END`) supaya state stabil.

Properti penting:

- `R0` dan `R1` tidak diubah oleh program.
- Hasil akhir hanya ditaruh di `R2`.

## Penjelasan `Fill.asm`

File: `training/04/project_04/Fill/Fill.asm`

Program berjalan dalam loop utama tanpa henti:

1. Baca `KBD` (`RAM[24576]`):
   - jika `KBD != 0`, set `color = -1` (hitam),
   - jika `KBD == 0`, set `color = 0` (putih).
2. Set pointer `addr` ke `SCREEN` (`RAM[16384]`).
3. Loop dari `SCREEN` sampai sebelum `KBD`:
   - tulis `color` ke `RAM[addr]`,
   - `addr++`.
4. Kembali ke loop utama untuk cek keyboard lagi.

Dengan ini:

- menekan tombol cukup lama → layar penuh hitam,
- melepas tombol cukup lama → layar penuh putih.

## Verifikasi

Verifikasi formal yang dijalankan:

- `Mult.tst` dibandingkan `Mult.cmp` → **PASS**
- `FillAutomatic.tst` dibandingkan `FillAutomatic.cmp` → **PASS**

Catatan:

- `Fill.tst` bersifat interaktif/manual (butuh keyboard input real-time).
- CLI global `nand2tetris run` pada environment ini belum menangani `.asm/.tst` Project 4 secara langsung, jadi verifikasi dilakukan melalui harness CPU internal simulator.

## Artefak Submission

ZIP submission sudah dibuat di:

- `training/04/report/project4.zip`

Isi:

- `Mult/Mult.asm`
- `Fill/Fill.asm`
