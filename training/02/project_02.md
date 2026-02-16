# Project 2 — Boolean Arithmetic (Nand to Tetris)

## Ringkasan
Pusat komputasi dari CPU adalah **ALU (Arithmetic-Logic Unit)**. Pada Project 2 kamu akan membangun rangkaian chip aritmetika (penjumlahan) secara bertahap hingga mencapai **ALU** untuk komputer Hack.

---

## Objective
Bangun chip berikut:

- **HalfAdder**
- **FullAdder**
- **Add16**
- **Inc16**
- **ALU**

> Catatan: Semua chip ini adalah standar, kecuali **ALU** yang bervariasi antar arsitektur komputer.

---

## Deliverables (Yang harus kamu kerjakan)
Untuk setiap chip `Xxx` di daftar:
- Lengkapi file **`Xxx.hdl`** (stub) pada bagian `PARTS` yang masih kosong.
- Jalankan test yang disediakan (`Xxx.tst`) dan pastikan output sesuai compare file (`Xxx.cmp`).

### File yang disediakan untuk setiap chip
- `Xxx.hdl` — *stub file* (rangka HDL, `PARTS` belum lengkap)
- `Xxx.tst` — test script untuk hardware simulator
- `Xxx.cmp` — expected output untuk test tersebut

---

## Acceptance Criteria (Contract)
Implementasi kamu dianggap benar jika **`Xxx.hdl` yang sudah dimodifikasi**, ketika diuji dengan **`Xxx.tst`**, menghasilkan output yang **persis sama** dengan **`Xxx.cmp`**. Jika tidak sama, simulator akan menampilkan error/mismatch.

---

## Tools & Setup

### Opsi A — Online IDE (direkomendasikan)
Online IDE menyediakan semua `Xxx.hdl`, `Xxx.tst`, `Xxx.cmp` di browser, dengan auto-save. Kamu memilih project/chip dari dropdown simulator, run test, lalu bisa download semua HDL sebagai zip.

### Opsi B — Desktop Hardware Simulator
Jika kamu memakai software suite Nand2Tetris:
- Hardware simulator ada di `nand2tetris/tools/`
- File project ada di `nand2tetris/projects/2/`
- Edit `Xxx.hdl` pakai text editor, lalu test via desktop simulator

---

## Cara Kerja (Instruksi Praktis)
Ulangi siklus berikut untuk setiap chip:

1. **Baca spesifikasi di komentar stub `Xxx.hdl`**
   - Perhatikan `IN`, `OUT`, ukuran bus, dan definisi fungsional.
2. **Turunkan perilaku logika**
   - Untuk adder: pahami carry & sum bit.
   - Untuk ALU: pahami kontrol yang memodifikasi input dan memilih operasi.
3. **Implementasikan di `PARTS`**
   - Rakit dari chip yang diizinkan (lihat “Implementation Rules”).
4. **Jalankan test**
   - Online: pilih script dari dropdown test.
   - Desktop: load `Xxx.tst` dari folder project.
5. **Iterasi sampai lolos**
   - Kalau mismatch, cek wiring, indeks bus, dan alur carry.

---

## Implementation Rules (Yang boleh dipakai sebagai chip-parts)
Semua “Implementation Tips” dari Project 1 tetap berlaku untuk Project 2.

Perbedaan utama:
- Saat mengimplementasikan Project 2, kamu boleh memakai sebagai *chip-part*:
  - **semua chip dari Project 1**, dan
  - **semua chip dari Project 2**

**Desktop note:** Jangan menambahkan file lain ke folder `projects/2`; desktop simulator akan memakai builtin chip implementations bila diperlukan.

---

## Spesifik untuk ALU (wajib ikuti strategi staged)
ALU Hack menghasilkan:
- `out` (16-bit),
- `zr` dan `ng` (masing-masing 1-bit).

Rekomendasi pengerjaan (dua tahap):
1. **ALU basic**: implementasikan perhitungan `out` dulu, **abaikan `zr` dan `ng`**.
2. **ALU final**: implementasikan `out` **dan** hitung `zr` serta `ng`.

File test yang disediakan untuk dua tahap ini:
- `ALU-basic.tst` + `ALU-basic.cmp` (untuk basic)
- `ALU.tst` + `ALU.cmp` (untuk final)

Cara menjalankan:
- Online IDE: pilih test script dari dropdown **Test**.
- Desktop: load test script dari folder `projects/2`.

---

## References (rujukan yang disebutkan di dokumen)
- HDL Guide
- Chips Set API
- Tutorials (hardware simulator)

> Catatan: Tutorial yang tersedia saat ini fokus ke desktop simulator; prinsipnya tetap sama untuk online simulator (bedanya: online tidak perlu load file manual).

---

## Output yang Dikumpulkan
- Set lengkap `Xxx.hdl` untuk semua chip di Project 2 yang **lolos test** sesuai contract.
- Jika pakai online IDE: download zip yang berisi versi terbaru semua `Xxx.hdl`.

---

## Checklist Cepat
- [ ] HalfAdder.hdl lolos HalfAdder.tst
- [ ] FullAdder.hdl lolos FullAdder.tst
- [ ] Add16.hdl lolos Add16.tst
- [ ] Inc16.hdl lolos Inc16.tst
- [ ] ALU basic lolos ALU-basic.tst
- [ ] ALU final lolos ALU.tst
- [ ] Tidak menambah file lain ke `projects/2` (desktop)

---

*Copyright notice (as in original materials): nand2tetris.org — Noam Nisan & Shimon Schocken.*
