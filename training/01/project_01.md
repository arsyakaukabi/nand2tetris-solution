# Project 1 — Elementary Logic Gates (Nand to Tetris)

## Ringkasan
Arsitektur komputer tipikal dibangun dari kumpulan *elementary logic gates* seperti **And**, **Or**, **Mux**, dll., termasuk versi bitwise-nya seperti **And16**, **Or16**, **Mux16** (diasumsikan mesin 16-bit). Pada Project 1 ini kamu membangun satu set gate dasar yang nantinya akan menjadi *building blocks* untuk CPU dan RAM di project berikutnya.

---

## Objective
Bangun chip/gate berikut (istilah *chip* dan *gate* dipakai saling bergantian):

- **Nand (given)**
- **Not**
- **And**
- **Or**
- **Xor**
- **Mux**
- **DMux**
- **Not16**
- **And16**
- **Or16**
- **Mux16**
- **Or8Way**
- **Mux4Way16**
- **Mux8Way16**
- **DMux4Way**
- **DMux8Way**

**Catatan:** `Nand` dianggap primitive, jadi tidak perlu diimplementasikan.

---

## Deliverables (Yang harus kamu kerjakan)
Untuk setiap chip `Xxx` di daftar (selain `Nand`), kamu harus **melengkapi file `Xxx.hdl`** yang disediakan (stub), khususnya bagian `PARTS` yang masih kosong.

### File yang disediakan untuk setiap chip
- `Xxx.hdl` — *stub file* (rangka dasar HDL, bagian `PARTS` belum lengkap)
- `Xxx.tst` — *test script* untuk Hardware Simulator
- `Xxx.cmp` — *compare file* berisi output yang benar (expected output)

---

## Acceptance Criteria (Contract)
Implementasimu dianggap benar jika:
- `Xxx.hdl` yang sudah kamu modifikasi,
- diuji menggunakan `Xxx.tst`,
- menghasilkan output yang **persis sama** dengan `Xxx.cmp`.

Jika output berbeda, simulator akan menampilkan error message / mismatch report.

---

## Tools & Setup

### Opsi A — Online IDE (direkomendasikan)
Online IDE Nand2Tetris menyediakan semua `Xxx.hdl`, `Xxx.tst`, `Xxx.cmp` langsung di browser.

Workflow:
1. Pilih project/chip dari dropdown simulator.
2. Edit `Xxx.hdl` (auto-save).
3. Jalankan test script.
4. Jika ingin ambil hasilnya ke lokal: klik tombol **Download** (biasanya satu ZIP berisi seluruh `Xxx.hdl` project).

**Link:**
- Web IDE: https://nand2tetris.github.io/web-ide/
- Project 1 page: https://www.nand2tetris.org/project01

### Opsi B — Desktop Hardware Simulator
Jika kamu menggunakan *software suite* Nand2Tetris:
1. Download & extract ke folder, mis. `nand2tetris/`.
2. Tools ada di: `nand2tetris/tools/` (Hardware Simulator).
3. File project ada di: `nand2tetris/projects/1/` (di beberapa distribusi bisa muncul sebagai `projects/01/`).

Workflow:
1. Edit `Xxx.hdl` pakai text editor apa pun.
2. Buka Hardware Simulator, load chip + load test script (`Xxx.tst`).
3. Run, pastikan match `Xxx.cmp`.

**Link:**
- Software suite: https://www.nand2tetris.org/software

---

## Cara Kerja (Instruksi Praktis per Chip)
Gunakan siklus kerja berikut untuk setiap chip:

1. **Baca spesifikasi di komentar `Xxx.hdl`**
   - Perhatikan `IN`, `OUT`, serta ukuran bus (mis. `[16]`).
2. **Turunkan perilaku logika**
   - Buat truth table / persamaan Boolean / rule Mux-DMux.
3. **Implementasikan di bagian `PARTS`**
   - Rakit dari chip yang diizinkan pada project ini (lihat “Implementation Tips”).
4. **Jalankan test**
   - Online: run `Xxx.tst` langsung.
   - Desktop: load test script lalu run.
5. **Perbaiki hingga lolos**
   - Kalau mismatch: cek wiring, indeks bus, urutan bit, dan koneksi pin.

---

## HDL Documentation (Notasi yang sering disingkat)
Dokumen project kadang menggunakan notasi singkat. Contoh interpretasi:
- “if (in) out = 1, else out = 0” berarti **jika `in = 1` maka `out = 1`, jika tidak maka `out = 0`** (alias *if-then-else* eksplisit pada nilai 0/1).
- “if (a and b) …” berarti **`a = 1` dan `b = 1`**.

(Selalu rujuk komentar interface di stub `Xxx.hdl` untuk definisi yang tepat.)

---

## References (yang dirujuk oleh dokumen project)
- **HDL Guide** (referensi sintaks & aturan HDL)
- **Chips Set API** (definisi chip-chips bawaan dan pin/pemetaan)
- **Tutorials** (hardware simulator, script-based testing, dll.)

Link rujukan praktis (resmi / umum dipakai):
- Demos & tutorials: https://www.nand2tetris.org/demos
- Appendix HDL (referensi HDL klasik): https://www.cs.huji.ac.il/course/2002/nand2tet/docs/appendix_A.pdf

---

## Implementation Tips (dari dokumen project)
0. **Sebelum implement**, eksperimen dulu dengan *builtin implementation* chip terkait.
   - Online: klik toggle *builtin*.
   - Desktop: load builtin chip dari `tools/builtInChips/`.

1. Satu chip bisa diimplementasikan dengan banyak cara. **Makin sederhana makin baik** — gunakan **sesedikit mungkin chip-parts**.
2. Kamu boleh mengimplementasikan chip langsung dari `Nand`, tetapi juga boleh memakai chip project 1 lain sebagai *chip-part* (komposisi).
3. Tidak perlu membuat “helper chips” buatan sendiri. **Gunakan hanya chip yang ada di daftar project ini.**
4. Disarankan implement sesuai urutan yang diberikan.
   - Jika ada chip yang belum selesai, kamu masih boleh memakainya sebagai *chip-part*:
     - Online: evaluator bisa memakai builtin.
     - Desktop: rename/hapus file `Xxx.hdl` yang belum jadi agar simulator memakai builtin.
5. Chip bisa dites interaktif atau via test script.
   - Online: run script langsung.
   - Desktop: load `Xxx.tst` dulu, baru run.

---

## Output yang Dikumpulkan
- Kumpulan file `Xxx.hdl` yang sudah lengkap dan lolos test.
- Jika pakai online IDE: download ZIP hasilnya.
- Jika pakai desktop: pastikan folder project berisi HDL final untuk semua chip yang diminta.

---

## Checklist Cepat
- [ ] Semua `Xxx.hdl` (selain `Nand`) sudah terisi `PARTS`
- [ ] Semua `Xxx.tst` berjalan tanpa error
- [ ] Output match `Xxx.cmp`
- [ ] Tidak ada helper chip di luar daftar
- [ ] Struktur bus/pin sesuai spesifikasi stub

---

*Copyright notice (as in original materials): nand2tetris.org — Noam Nisan & Shimon Schocken.*
