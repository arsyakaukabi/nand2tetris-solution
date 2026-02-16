# Project 3 — Memory (Nand to Tetris)

## Ringkasan
**Main memory (RAM)** adalah urutan *register* yang dapat di-*address* (addressable sequence of registers), masing-masing menyimpan nilai **n-bit**. Pada project ini kamu akan membangun unit RAM secara bertahap.

Ada 2 problem inti yang harus diselesaikan dengan gate logic:
1. **Menyimpan bit secara persisten dari waktu ke waktu** (*stateful storage*).
2. **Melakukan addressing**: memilih register memori mana yang menjadi target operasi baca/tulis.

---

## Objective
Bangun chip berikut:

- **DFF (given)**
- **Bit**
- **Register**
- **RAM8**
- **RAM64**
- **RAM512**
- **RAM4K**
- **RAM16K**
- **PC**

> **DFF** dianggap *primitive* (diberikan), jadi **tidak perlu kamu implementasikan**.

---

## Deliverables (Yang harus kamu kerjakan)
Untuk setiap chip `Xxx` di daftar (kecuali DFF):
- Lengkapi file **`Xxx.hdl`** (stub) pada bagian `PARTS`.
- Jalankan test yang disediakan dan pastikan hasilnya sesuai *expected output*.

### File yang disediakan untuk setiap chip
- `Xxx.hdl` — *stub file* (rangka HDL, `PARTS` belum lengkap)
- `Xxx.tst` — test script untuk hardware simulator
- `Xxx.cmp` — expected output untuk test tersebut

---

## Acceptance Criteria (Contract)
Implementasi kamu dianggap benar jika:
- `Xxx.hdl` (yang sudah kamu modifikasi),
- ketika diuji dengan `Xxx.tst`,
- menghasilkan output yang **persis sama** dengan `Xxx.cmp`.

Jika tidak sama, simulator akan melaporkan error / mismatch.

---

## Tools & Setup

### Opsi A — Online IDE (direkomendasikan)
Jika kamu memakai **Nand2Tetris Online IDE**:
- Semua file `Xxx.hdl`, `Xxx.tst`, `Xxx.cmp` tersedia di browser.
- Untuk develop & test, pilih project/chip dari dropdown simulator.
- Perubahan HDL tersimpan otomatis.
- Untuk mengambil hasil ke lokal, klik **Download** → semua `Xxx.hdl` project akan diunduh sebagai satu ZIP.

### Opsi B — Desktop Hardware Simulator
Jika kamu memakai **software suite**:
- Hardware simulator ada di: `nand2tetris/tools/`
- File project ada di:
  - `nand2tetris/projects/3/a`
  - `nand2tetris/projects/3/b`

> **Penting (desktop):** folder `a` dan `b` dibutuhkan untuk alasan teknis (auto-grading). **Jangan memindahkan file antar subfolder** dan **jangan mengubah struktur folder**.

---

## Cara Kerja (Instruksi Praktis)
Ulangi siklus berikut untuk setiap chip:

1. **Baca spesifikasi di komentar stub `Xxx.hdl`**
   - Perhatikan `IN`, `OUT`, ukuran bus, dan definisi perilaku.
2. **Turunkan desain secara bertahap**
   - Storage: Bit → Register → RAM (hierarki).
   - Addressing: select line → decode → mux/dmux (sesuai spesifikasi chip).
3. **Implementasikan di `PARTS`**
   - Rakit dari chip yang diizinkan (lihat “Implementation Rules”).
4. **Jalankan test**
   - Online: run `Xxx.tst` dari dropdown Test.
   - Desktop: load `Xxx.tst` dari folder project.
5. **Debug sampai lolos**
   - Fokus pada: wiring load, clocking (DFF), dan addressing (bit selection).

### Urutan pengerjaan yang disarankan (praktis)
- `Bit` → `Register` → `RAM8` → `RAM64` → `RAM512` → `RAM4K` → `RAM16K` → `PC`

---

## Implementation Rules (Yang boleh dipakai sebagai chip-parts)
Semua **Implementation Tips dari Project 1** berlaku juga untuk Project 3.

Modifikasi khusus Project 3:
- Saat mengimplementasikan chip Project 3, kamu boleh memakai sebagai *chip-parts*:
  - chip-chip di **Project 1**, **Project 2**, dan **Project 3** (sesuai daftar yang tersedia di suite).

> **Penting (desktop):** pertahankan struktur `projects/3/a` dan `projects/3/b` apa adanya.

---

## References (rujukan yang disebutkan di dokumen)
- **HDL Guide**
- **Chips Set API**
- **Tutorials** (desktop simulator):
  - Clock Demo
  - Register Demo
  - RAM Demo
  - Program Counter Demo

> Catatan: tutorial online simulator akan tersedia kemudian; prinsip dari tutorial desktop tetap bisa dipakai untuk online (bedanya: online tidak perlu load file manual).

---

## Submission Guideline (khusus Project 3)
Jika instruksi course-mu meminta submit ZIP, maka struktur ZIP **WAJIB** seperti ini:

```text
project3.zip
└── a
    ├── Bit.hdl
    ├── PC.hdl
    ├── RAM64.hdl
    ├── RAM8.hdl
    └── Register.hdl
└── b
    ├── RAM16K.hdl
    ├── RAM4K.hdl
    └── RAM512.hdl
```

> Folder `a` dan `b` diperlukan untuk alasan teknis auto-grading. **Jika struktur tidak sesuai, bisa kena penalti grading.** (Guideline ini khusus Project 3.)

---

## Checklist Cepat
- [ ] `Bit.hdl` lolos `Bit.tst`
- [ ] `Register.hdl` lolos `Register.tst`
- [ ] `RAM8.hdl` lolos `RAM8.tst`
- [ ] `RAM64.hdl` lolos `RAM64.tst`
- [ ] `RAM512.hdl` lolos `RAM512.tst`
- [ ] `RAM4K.hdl` lolos `RAM4K.tst`
- [ ] `RAM16K.hdl` lolos `RAM16K.tst`
- [ ] `PC.hdl` lolos `PC.tst`
- [ ] (Desktop) Struktur folder `projects/3/a` & `projects/3/b` tetap utuh
- [ ] (Submission) ZIP mengikuti struktur `project3.zip` dengan folder `a` dan `b`

---

*Copyright notice (as in original materials): nand2tetris.org — Noam Nisan & Shimon Schocken.*
