# Project 8 — Virtual Machine II: Program Control (Nand to Tetris)

## Ringkasan
Di Project 7 kamu sudah membuat VM Translator dasar yang mendukung:
- stack arithmetic / logical commands, dan
- `push` / `pop` (memory access).

Di Project 8 kamu **meng-upgrade** translator tersebut menjadi **full-scale VM Translator** dengan menambahkan:
1) **branching / program flow commands** (`label`, `goto`, `if-goto`),  
2) **function commands** (`function`, `call`, `return`), dan  
3) kemampuan menerjemahkan **program multi-file** (satu folder berisi beberapa `.vm`) menjadi **satu** file `.asm`.

Translator ini nantinya menjadi “compiler backend” untuk pipeline Jack → VM → Hack assembly.

---

## Objective
Extend VM translator Project 7 menjadi translator lengkap yang mampu menangani **single-file** maupun **multi-file VM programs**, dengan asumsi source VM **error-free**.

---

## Contract
Kamu harus menyelesaikan VM-to-Hack translator yang:
- conform dengan **VM Specification** dan **Standard VM Mapping on the Hack Platform**,
- menerjemahkan test programs `.vm` yang disediakan menjadi Hack assembly,
- dan saat dieksekusi di **CPU Emulator** menggunakan test scripts (`.tst`) + compare files (`.cmp`), output harus **match**.

---

## Scope Wajib (fitur yang harus didukung)

### A) Program Flow / Branching Commands
Implement translasi untuk:
- `label X`
- `goto X`
- `if-goto X`

**Catatan penting (label scoping):**
- Di VM spec, label bersifat **function-scoped**. Praktiknya, label biasanya di-*qualify* menjadi:
  - `FunctionName$LabelName`
agar tidak bentrok antar fungsi.

### B) Function Calling Commands
Implement translasi untuk:
- `function f nLocals`
- `call f nArgs`
- `return`

Di sini inti VM implementation adalah “stack frame” dan mekanisme call/return yang menjaga konteks caller dan callee.

### C) Multi-file VM Program Translation
Translator harus bisa menerima input:
- **1 file** `.vm`, atau
- **1 folder** berisi beberapa `.vm`

Dan menghasilkan output:
- jika input file: `FileName.asm` (di folder yang sama)
- jika input folder: `FolderName.asm` (di dalam folder tersebut), berisi hasil translasi **gabungan** semua file `.vm` di folder itu.

---

## Bootstrap Code Rule (aturan penting khusus Project 8)
Bootstrap code = startup code yang:
1) **set `SP = 256`**, lalu
2) **memanggil `Sys.init`**.

**Rule untuk project ini:**
- Jika translator dipanggil untuk menerjemahkan **satu file saja** → **JANGAN** menulis bootstrap code.
- Jika translator dipanggil untuk menerjemahkan **lebih dari satu `.vm` file** (artinya input folder) → **WAJIB** menulis bootstrap code.

> Kenapa begitu? Karena test scripts untuk beberapa test awal akan menginisialisasi stack & segment pointers “secara manual”, sementara test multi-file mengasumsikan kamu menghasilkan bootstrap code sendiri.

---

## Test Programs (urutan pengerjaan yang disarankan)
Dokumen project menyarankan staged development: **branching dulu**, lalu **function commands**, supaya kamu bisa unit-test incremental.

### Stage 1 — Test Branching Commands
1) **BasicLoop**
   - Menguji `label` dan `if-goto`.
   - Program menghitung `1 + 2 + ... + argument[0]` dan push hasil ke stack.

2) **FibonacciSeries**
   - Menguji `label`, `goto`, `if-goto` secara lebih ketat.
   - Program menghitung dan menyimpan deret Fibonacci pertama sebanyak `n` elemen ke memory.

**Catatan:** pada dua test ini, inisialisasi stack dan virtual segments dilakukan oleh test scripts, bukan oleh bootstrap.

### Stage 2 — Test Function Commands + Multi-file Translation
3) **SimpleFunction**
   - Menguji `function` dan `return`.
   - Test script akan menyiapkan SP, segment pointers, mock return address, lalu memanggil fungsi.

4) **NestedCall** (opsional, intermediate)
   - Berguna jika SimpleFunction sudah lulus tapi FibonacciElement gagal.
   - Cek dokumentasi test untuk detailnya.

5) **FibonacciElement** (WAJIB, multi-file)
   - Terdiri dari **dua file**:
     - `Main.vm` berisi fungsi rekursif `Main.fibonacci`
     - `Sys.vm` berisi `Sys.init` yang memanggil `Main.fibonacci` dengan `n=4`, lalu infinite loop
   - Test ini memverifikasi:
     - multi-file translation (input = folder, output = `FibonacciElement.asm`),
     - bootstrap code,
     - `function`, `call`, `return`,
     - dan sebagian besar command VM lainnya.

6) **StaticsTest** (WAJIB, multi-file)
   - Menguji penanganan `static` variables dalam setting multi-file.
   - Terdiri dari **tiga file**:
     - `Class1.vm` dan `Class2.vm` set/get beberapa static variables
     - `Sys.vm` memanggil fungsi-fungsi dari Class1 dan Class2
   - Harus menerjemahkan folder → output `StaticsTest.asm`.

---

## Implementation Guidance (high-level, tapi preskriptif)

### 1) Rekomendasi arsitektur program
Umumnya VM Translator dipisah menjadi:
- **Parser**
  - membaca `.vm`, membuang komentar/whitespace, mengklasifikasikan command, dan memberi argumen (arg1/arg2).
- **CodeWriter**
  - menghasilkan Hack assembly untuk tiap command (tulis ke output stream).
  - plus state: current file name (untuk `static`), current function name (untuk label scoping), dan counter untuk label unik.

### 2) API CodeWriter yang biasanya dibutuhkan (praktis)
Minimal kamu akan butuh method-method seperti:
- `writeArithmetic(cmd)`
- `writePushPop(cmdType, segment, index)`
- `writeLabel(label)`
- `writeGoto(label)`
- `writeIf(label)`
- `writeFunction(functionName, nLocals)`
- `writeCall(functionName, nArgs)`
- `writeReturn()`
- `writeInit()` (bootstrap)

> Kamu bisa men-gate pemanggilan `writeInit()` via constructor flag (single-file vs folder), sesuai aturan bootstrap.

### 3) Strategi “paper-first” untuk function call
Bagian function commands adalah yang paling menantang. Cara paling aman:
- gambar peta RAM stack,
- trace langkah demi langkah untuk `call` dan `return`,
- pastikan pointer `SP/LCL/ARG/THIS/THAT` bergerak benar,
- baru generalisasi menjadi template assembly yang digenerate.

### 4) Poin penting implementasi (semantik yang wajib benar)
- **`if-goto`**: pop nilai dari stack; jika nilai != 0, lompat ke label.
- **Label unik**:
  - label internal untuk branching (`eq/gt/lt` dari project 7) tetap harus unik,
  - return-address label pada `call` wajib unik,
  - label VM (`label X`) harus *function-scoped*.
- **Static variables**:
  - harus di-*namespace* menggunakan nama file `.vm` (contoh: `Class1.3`).

---

## Deliverables
- Kode program **VMTranslator** (siap dijalankan).
- Lulus seluruh test suite Project 8:
  - `BasicLoop`, `FibonacciSeries`, `SimpleFunction`, `FibonacciElement`, `StaticsTest`
  - (`NestedCall` opsional sebagai debugging aid)

---

## Checklist Cepat
- [ ] Translator bisa menerima **file**: `VMTranslator Foo.vm` → `Foo.asm` (tanpa bootstrap)
- [ ] Translator bisa menerima **folder**: `VMTranslator ProgFolder/` → `ProgFolder.asm` (dengan bootstrap)
- [ ] `label/goto/if-goto` lulus (BasicLoop, FibonacciSeries)
- [ ] `function/call/return` lulus (SimpleFunction, FibonacciElement)
- [ ] Multi-file + static lulus (StaticsTest)
- [ ] Bootstrap code hanya untuk multi-file: `SP=256` lalu `call Sys.init`

---

## Reference Links
```text
Project 08 page: https://www.nand2tetris.org/project08
Project 8 PDF: (file yang kamu upload: Project 8.pdf)
```
