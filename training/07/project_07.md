# Project 7 — Virtual Machine I: Stack Arithmetic (Nand to Tetris)

## Ringkasan
Compiler modern sering menghasilkan **VM code** untuk sebuah *virtual machine* (mirip Java bytecode untuk JVM). VM code ini kemudian diterjemahkan lagi menjadi **machine language** host computer oleh program bernama **VM Translator** (sering disebut *compiler backend*).

Di Project 7 kamu membangun **versi dasar VM Translator**: program yang membaca file `.vm`, mem-parse VM command satu per satu, lalu meng-*emit* rangkaian instruksi **Hack assembly** (`.asm`) yang merealisasikan semantik setiap command VM.

> Di Project 8, translator ini akan kamu lanjutkan untuk mendukung *program control*, fungsi, serta bootstrap.

---

## Objective
Bangun **basic VM translator** yang mengimplementasikan:
1) **Arithmetic-logical commands** (stack arithmetic), dan  
2) **push/pop commands** (memory access) untuk segmen yang disyaratkan.

Asumsi: source VM **error-free** (tidak perlu error handling/reporting).

---

## Contract
Tulis VM-to-Hack translator yang:
- konform dengan **VM Specification, Part I** (book §7.2) dan **Standard VM-on-Hack Mapping, Part I** (book §7.3.1),
- menggunakan translator-mu untuk menerjemahkan file-file test `.vm` yang disediakan menjadi `.asm`,
- dan ketika `.asm` hasil translasi dieksekusi pada **CPU Emulator** memakai test scripts (`.tst`) dan compare files (`.cmp`) yang disediakan, hasilnya harus **match**.

**Important (Project 7):** kamu **tidak perlu** menambahkan bootstrap/startup code maupun inisialisasi segment pointers. Semua inisialisasi stack dan memory mapping sudah dilakukan oleh **test scripts**. Jadi output `.asm` dari translator kamu harus berisi **translasi command VM input saja**, dan **tidak lebih**.

---

## Usage (I/O)
### Input
- `fileName.vm` (nama file dapat mengandung path)

### Output
- `fileName.asm` (disimpan di folder yang sama dengan input)

### Cara invoke (contoh)
```bash
VMTranslator fileName.vm
```

---

## Scope Perintah VM yang WAJIB Didukung

### Stage I — Stack arithmetic + `push constant x`
Implement:
- `push constant x` (x = integer non-negatif)
- 9 arithmetic / logical commands:
  - `add`, `sub`, `neg`
  - `eq`, `gt`, `lt`
  - `and`, `or`, `not`

Stage ini penting untuk unit test arithmetic: kamu bisa mendorong konstanta ke stack, lalu operasi.

### Stage II — Memory access (`push` / `pop` untuk semua segmen)
Perluas translator agar mendukung `push segment i` dan `pop segment i` untuk **8 segmen** VM. Disarankan dibangun per sub-stage:

1) `constant` (sudah dari Stage I)  
2) `local`, `argument`, `this`, `that`  
3) `pointer`, `temp` (termasuk kemampuan mengubah base `this`/`that`)  
4) `static`

**Rule penting untuk `static`:**
- Simbol static harus di-*namespace* dengan nama file VM agar tidak bentrok lintas file, umumnya berupa `FileName.i`.

---

## Tools yang Dipakai (untuk testing)
- **CPU Emulator** (wajib): menjalankan output `.asm` dan menjalankan `.tst` scripts.
- **VM Emulator** (sangat direkomendasikan): menjalankan `.vm` langsung untuk memahami perilaku program dan dampaknya ke stack/segments sebelum menulis generator `.asm`.

---

## Test Programs (unit-test incremental)
Project menyediakan 5 VM programs untuk menguji stage-by-stage. Kerjakan dalam urutan ini:

1) **SimpleAdd**
   - Menguji: `push constant i` dan `add`.
2) **StackTest**
   - Menguji: semua arithmetic-logical commands.
3) **BasicTest**
   - Menguji: `push/pop` + arithmetic pada segmen `constant`, `local`, `argument`, `this`, `that`, `temp`.
4) **PointerTest**
   - Menguji: segmen `pointer`, `this`, `that`.
5) **StaticTest**
   - Menguji: segmen `static`.

### Paket file per program
Untuk setiap program `Xxx`, biasanya disediakan 4 file:
- `Xxx.vm` — program VM
- `XxxVME.tst` — script untuk menjalankan di **VM Emulator**
- `Xxx.tst` — script untuk menjalankan `.asm` di **CPU Emulator**
- `Xxx.cmp` — expected output

---

## Workflow Testing (langkah wajib per program)
Untuk setiap test program `Xxx.vm`, lakukan:

1) **Pahami expected behavior**
   - Jalankan `Xxx.vm` di VM Emulator menggunakan `XxxVME.tst`.
2) **Translate**
   - Jalankan translator kamu pada `Xxx.vm` → hasilnya `Xxx.asm`.
3) **Inspect output**
   - Cek `Xxx.asm` untuk error sintaks / pola yang jelas salah.
4) **Formal test**
   - Jalankan `Xxx.asm` di CPU Emulator menggunakan `Xxx.tst`, lalu pastikan output match `Xxx.cmp`.
5) Debug dan ulangi sampai lulus.

**Catatan penting:** test programs dirancang untuk memverifikasi fitur incremental. Implementasikan translator **sesuai urutan stage**; kalau kamu loncat stage, test bisa gagal secara membingungkan.

---

## Proposed Implementation (struktur program yang umum)
Bentuk implementasi yang lazim (nama class/module bebas):

### 1) Parser
- Baca file `.vm`
- Buang whitespace dan komentar
- Baca satu command VM per langkah, serta pecah menjadi:
  - command type (arithmetic / push / pop)
  - arg1 (jika ada)
  - arg2 (jika ada)

### 2) CodeWriter
- Emit Hack assembly untuk tiap command, misalnya lewat API:
  - `writeArithmetic(command)`
  - `writePushPop(commandType, segment, index)`

### 3) Unique label generator
- `eq`, `gt`, `lt` butuh branching di assembly → buat label unik (mis. counter global) agar tidak collision.

---

## Tips
### Initialization (bootstrap) — *jangan dikerjakan di Project 7*
Untuk menjalankan VM program di host, final VM translator (Project 8) akan menambahkan bootstrap code dan inisialisasi segmen. Tetapi untuk Project 7, semua itu sudah diurus test scripts. Jadi output translator kamu harus “pure translation” dari isi file input.

### Save a backup
Setelah lulus Project 7, simpan versi translator yang “clean”. Di Project 8 kamu akan menambah fitur; backup ini berguna kalau terjadi regresi.

---

## Deliverables
- Kode program **VMTranslator** yang bisa dijalankan sesuai usage.
- Translator kamu harus meluluskan test scripts untuk kelima program:
  - `SimpleAdd`, `StackTest`, `BasicTest`, `PointerTest`, `StaticTest`.

---

## Reference Links (untuk dibuka manual)
```text
Project 07 page: https://www.nand2tetris.org/project07
Book references: Chapter 7 (Project 7). Chapter 8 diabaikan untuk project ini.
```
