# Project 5 — Computer Architecture (Nand to Tetris)

## Ringkasan
Di project sebelumnya kamu sudah membangun **ALU** dan **RAM**. Di Project 5 ini kamu “menjahit semuanya” menjadi **Hack Hardware Platform** lengkap: sebuah komputer general-purpose yang mampu menjalankan program dalam **Hack machine language**.

---

## Objective
Selesaikan konstruksi **Hack CPU** dan **platform hardware Hack**, hingga mencapai chip paling atas **Computer**.

---

## Chips yang harus diimplementasikan
Kamu akan melengkapi (mengisi bagian `PARTS`) untuk 3 chip berikut:
- **Memory.hdl** — menangani seluruh address space RAM (*Entire RAM address space*)
- **CPU.hdl** — Hack CPU
- **Computer.hdl** — chip paling atas (top-most chip) dari platform

---

## Deliverables
- `Memory.hdl` (Project 05)
- `CPU.hdl` (Project 05)
- `Computer.hdl` (Project 05)

> File `.tst` dan `.cmp` sudah disediakan untuk testing; kamu hanya memodifikasi HDL chip yang diminta.

---

## Acceptance Criteria (Contract)
Platform yang kamu bangun harus mampu **mengeksekusi program** dalam **Hack machine language (Chapter 4)**. Buktikan dengan menjalankan 3 program test (Add, Max, Rect) pada chip `Computer`.

---

## Tools & Setup

### Opsi A — Online IDE
Semua chip bisa diimplementasikan dan diuji menggunakan **Hardware Simulator** yang disediakan (di web IDE).

### Opsi B — Desktop Software Suite
Jika kamu memakai Nand2Tetris Software Suite, file project tersimpan di:
- `nand2tetris/projects/05`

Tools yang dipakai:
- **Hardware Simulator** (untuk unit test Memory/CPU, dan integrasi Computer + ROM)

---

## Testing Strategy (wajib: unit-test sebelum integrasi)

### 1) Unit test `Memory` dan `CPU`
Sangat disarankan (dan “penting”) untuk **unit-test** `Memory` dan `CPU` dulu sebelum membangun `Computer`.

- **Memory**
  - Recommended test: `Memory.tst` + `Memory.cmp`
- **CPU**
  - Recommended test: `CPU.tst` + `CPU.cmp`
  - Alternative test (lebih ringan/kurang thorough): `CPU-external.tst` + `CPU-external.cmp` (tidak mengharuskan penggunaan built-in `DRegister`).

### 2) Test integrasi `Computer` (jalankan program `.hack`)
Cara “natural” mengetes `Computer` adalah membuatnya mengeksekusi program Hack machine language. Prinsip test script:
1) load `Computer.hdl` ke Hardware Simulator,  
2) load file program `.hack` ke chip-part ROM di dalam `Computer`,  
3) jalankan clock cukup banyak cycle untuk mengeksekusi instruksi.

**Tiga program uji yang disediakan:**
- **Add.hack** — menambahkan konstanta 2 dan 3, simpan ke `RAM[0]`  
  - Recommended: `ComputerAdd.tst` + `ComputerAdd.cmp`  
  - Alternative: `ComputerAdd-external.tst` + `ComputerAdd-external.cmp` (kurang thorough; hanya butuh built-in `RAM16K`)
- **Max.hack** — `max(RAM[0], RAM[1])` → `RAM[2]`  
  - Recommended: `ComputerMax.tst` + `ComputerMax.cmp`  
  - Alternative: `ComputerMax-external.tst` + `ComputerMax-external.cmp` (kurang thorough; hanya butuh built-in `RAM16K`)
- **Rect.hack** — gambar rectangle width 16 pixel, height `RAM[0]` di top-left screen  
  - Recommended: `ComputerRect.tst` + `ComputerRect.cmp`  
  - Alternative: `ComputerRect-external.tst` + `ComputerRect-external.cmp` (kurang thorough; tidak butuh built-in chips)

> **Debug mindset penting:** program `Rect.hack` yang disediakan *bug-free*. Kalau hasilnya salah, biasanya yang bug adalah `Computer.hdl` atau chip-part bawahannya—jadi kamu harus debug hardware kamu.

**Catatan:** sebelum menjalankan test `.tst` untuk Computer, baca file `.tst` dan pahami instruksi ke simulator. Referensi: **TDL Guide**.

---

## Recommended Build Order (Tips resmi)
Disarankan menyelesaikan konstruksi dalam urutan berikut:

### 1) Memory
`Memory` mencakup 3 chip-part:
- `RAM16K`
- `Screen`
- `Keyboard`

**Catatan:**
- `Screen` dan `Keyboard` tersedia sebagai **built-in chips**, jadi tidak perlu diimplementasikan.
- Walaupun `RAM16K` sudah kamu bangun di Project 3, **direkomendasikan memakai built-in RAM16K** karena memiliki GUI yang memudahkan debugging.

### 2) CPU
CPU bisa dibangun mengikuti rancangan yang diusulkan (Figure 5.9 / Chapter 5), menggunakan:
- `ALU` (Project 2)
- register chips (Project 3)

Namun, untuk memudahkan testing/debugging, direkomendasikan memakai built-in:
- `ARegister`
- `DRegister`  
Keduanya memiliki interface dan fungsionalitas yang sama seperti `Register`, tetapi menyediakan GUI side-effects yang membantu debugging.

> Secara prinsip, CPU kamu boleh memakai chip internal buatan sendiri (tidak disebut di rancangan buku), tapi ini **tidak direkomendasikan** dan biasanya membuat desain kurang efisien. Jika kamu membuat chip baru, dokumentasikan dan unit-test dengan teliti sebelum integrasi.

### 3) Instruction Memory
Gunakan built-in **ROM32K**.

### 4) Computer (top-most chip)
Bangun `Computer` mengikuti rancangan yang diusulkan (Figure 5.10 / Chapter 5).

---

## References / Resources
Dokumen rujukan yang disebutkan di halaman project:
- Chapter 5
- HDL Guide
- TDL Guide (reference)
- Hack Chip Set

---

## Checklist Cepat
- [ ] `Memory.hdl` lolos `Memory.tst`
- [ ] `CPU.hdl` lolos `CPU.tst` (opsional: `CPU-external.tst`)
- [ ] `Computer.hdl` lolos:
  - [ ] `ComputerAdd.tst`
  - [ ] `ComputerMax.tst`
  - [ ] `ComputerRect.tst`
- [ ] Jika hasil `Rect.hack` tidak sesuai → debug `Computer/CPU/Memory` (programnya bug-free)

---

*Based on official nand2tetris Project 05 description.*
