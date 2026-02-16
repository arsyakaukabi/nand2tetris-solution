# Project 11 — Compiler II: Code Generation (Jack → VM) — Requirements & Instructions

## Ringkasan
Compiler Jack di Nand2Tetris terdiri dari dua modul besar:
- **Syntax Analyzer** (Project 10): mem-parse Jack grammar.
- **Code Generator** (Project 11): mengubah hasil parsing menjadi **VM code** yang executable.

Di Project 11 kamu akan **mengubah** Syntax Analyzer dari Project 10 menjadi **Jack compiler penuh** dengan cara “mengganti” output XML pasif menjadi output **VM commands** (one `.vm` per `.jack`).

> Asumsi project ini: source Jack **error-free** (tidak perlu error checking/reporting).

---

## Objective
Extend Syntax Analyzer (Project 10) menjadi **full-scale Jack compiler**, lalu compile dan jalankan seluruh test programs yang disediakan hingga perilakunya sesuai dokumentasi masing-masing program.

---

## Contract
Kamu harus menulis compiler yang:
1) menerima input berupa **1 file** `Xxx.jack` atau **1 folder** berisi banyak `.jack`,  
2) menghasilkan output **satu file `.vm` untuk setiap file `.jack`**,  
3) output `.vm` dapat dijalankan di **VM Emulator**,  
4) semua test programs (di bawah) berjalan benar **tanpa perlu mengubah program test** (test program error-free; kalau fail, yang salah compiler-mu).

---

## Deliverables
- Kode program **JackCompiler** (atau nama lain sesuai implementasimu) yang bisa di-invoke pada file/folder.
- Untuk setiap folder test, output:
  - `ClassName.vm` untuk setiap `ClassName.jack` yang ada.
- (Opsional tapi sangat berguna) mode debug yang bisa menyalakan trace / komentar VM untuk mempermudah debug.

---

## Tools
- Bahasa pemrograman pilihanmu untuk implementasi compiler.
- **VM Emulator** (supplied) untuk menjalankan `.vm` hasil compile.
- Source code Syntax Analyzer (Project 10) sebagai basis.
- Text editor / diff tool untuk inspeksi output `.vm`.

---

# Implementation Stages (disarankan oleh course)

## Stage 0 — Backup
Buat backup code Project 10 yang sudah lulus (tokenizer + parser). Ini penting supaya kamu bisa kembali ke baseline jika terjadi regresi.

## Stage 1 — Symbol Table (semantic understanding)
Bangun modul **SymbolTable** dan gunakan untuk “memperkaya” parsing-mu dengan info identifier.

### 1.1 SymbolTable responsibilities
SymbolTable harus mengelola 2 scope:
- **class scope**: `static`, `field`
- **subroutine scope**: `arg`, `var` (local)

Untuk setiap identifier, table menyimpan:
- **name**
- **type** (mis. `int`, `boolean`, `Square`, dll)
- **kind/category**: `static | field | arg | var`
- **index** (running index per kind, mulai dari 0)

### 1.2 API minimum yang umumnya dipakai
- `startClass()` (opsional) / inisialisasi class table
- `startSubroutine()` (reset table subroutine untuk setiap function/method/constructor)
- `define(name, type, kind)`
- `varCount(kind)`
- `kindOf(name)`
- `typeOf(name)`
- `indexOf(name)`

### 1.3 “Stage 1 output” (mode debug)
Sebelum generate VM, course menyarankan kamu:
- menjalankan parser yang “diperluas” untuk menampilkan info setiap identifier:
  - name, kind, index, scope, serta status **declared vs used**
- output bisa berupa XML dengan markup versi kamu sendiri (bebas format).
Tujuannya: memastikan symbol table dan scoping benar sebelum masuk codegen.

## Stage 1.5 — Backup lagi
Backup versi “extended analyzer + symbol table” yang sudah benar. Ini jadi checkpoint sebelum kamu mulai mengubah pipeline ke codegen.

## Stage 2 — Code Generation (VM)
Ganti rutinitas CompilationEngine yang sebelumnya “emit XML” menjadi “emit VM code”.

Disarankan mengembangkan dan mengetes compiler **bertahap** menggunakan test programs dalam urutan yang ditentukan (lihat bagian Test Programs).

---

# Recommended Architecture (praktis dan standar)
Biasanya compiler dibuat dari komponen berikut:

## 1) JackTokenizer
Sama seperti Project 10: menghasilkan token stream.

## 2) CompilationEngine (Recursive Descent Parser)
Entry point: `compileClass()`.
Bedanya sekarang: setiap routine `compileXxx()` tidak lagi menulis XML, tapi menulis VM code via VMWriter.

## 3) SymbolTable
Mengelola mapping identifier → (kind/type/index) dan reset scope saat pindah class / subroutine.

## 4) VMWriter
Abstraction layer untuk menulis VM commands yang “well-formed”, misalnya:
- `writePush(segment, index)`
- `writePop(segment, index)`
- `writeArithmetic(cmd)`
- `writeLabel(label)`, `writeGoto(label)`, `writeIf(label)`
- `writeCall(name, nArgs)`
- `writeFunction(name, nLocals)`
- `writeReturn()`

> Memakai VMWriter mengurangi bug formatting dan membuat generator lebih rapi.

---

# Code Generation Rules (yang harus benar)

## A) Variable segments mapping
Saat generate push/pop untuk identifier:
- `static` → VM segment `static`
- `field`  → VM segment `this`
- `arg`    → VM segment `argument`
- `var`    → VM segment `local`

`index` diambil dari SymbolTable.

## B) Subroutine compilation conventions
### Function
- `function ClassName.funcName nLocals`
- Tidak ada setup `this` khusus.

### Method
- `function ClassName.methodName nLocals`
- Method menerima implicit `this` sebagai `argument 0`.
- Prolog: set `pointer 0` (`this`) dari `argument 0`:
  - `push argument 0`
  - `pop pointer 0`

### Constructor
- `function ClassName.new nLocals`
- Harus mengalokasikan memori untuk object (`field` count):
  - `push constant nFields`
  - `call Memory.alloc 1`
  - `pop pointer 0`  (this = allocated base)

## C) Statement compilation
### let
- `let x = expr;` → compile expr, lalu `pop segment index`.
- `let a[i] = expr;` (array assignment):
  - compute base + index,
  - set `that` (`pointer 1`) ke address itu,
  - evaluate RHS,
  - `pop that 0`.

### if / if-else
- Generate label unik (counter) untuk:
  - TRUE, FALSE, END
- `if (cond) { ... } else { ... }`:
  - compile `cond` menghasilkan 0/!0 di stack
  - branch sesuai VM `if-goto` / `goto`

### while
- Buat label LOOP dan END.
- compile condition, negate bila perlu untuk lompat ke END saat false.

### do
- compile subroutine call, lalu buang return value:
  - `pop temp 0`

### return
- `return;` → push 0 (void) lalu `return`
- `return expr;` → compile expr lalu `return`

## D) Expressions & Terms
### Operator mapping (umum)
- `+` → `add`
- `-` → `sub`
- `*` → `call Math.multiply 2`
- `/` → `call Math.divide 2`
- `&` → `and`
- `|` → `or`
- `<` → `lt`
- `>` → `gt`
- `=` → `eq`
Unary:
- `-` → `neg`
- `~` → `not`

### String constants
Konsep: string dibangun via OS `String`:
- `push constant len`
- `call String.new 1`
- untuk tiap karakter `c`:
  - `push constant ascii(c)`
  - `call String.appendChar 2`

### Keyword constants
- `true`  → push 0 lalu `not`
- `false` → push 0
- `null`  → push 0
- `this`  → push pointer 0

### Array access `a[i]`
- compile base `a`
- compile index `i`
- `add` → address
- `pop pointer 1`
- `push that 0`

## E) Subroutine calls (3 bentuk)
1) `f(args)`  
   - berarti method call pada current object (`this`).
   - implicit: push `this` sebagai arg0.
   - call: `call ClassName.f (nArgs + 1)`

2) `obj.m(args)`  
   - `obj` adalah variable (object reference).
   - push `obj` sebagai arg0, call ke `TypeOf(obj).m (nArgs + 1)`

3) `Class.f(args)`  
   - static function call (atau constructor call).
   - tidak ada implicit `this`.
   - call: `call Class.f nArgs`

---

# Testing Routine (wajib, per test program)
Untuk setiap test program folder:
1) **Compile folder** menggunakan compiler kamu → menghasilkan `.vm` per `.jack`.
2) **Inspect output `.vm`**: kalau terlihat salah/aneh, fix compiler → ulangi compile.
3) **Load folder ke VM Emulator** dan jalankan sesuai execution guidelines test program.
4) Jika behavior salah atau emulator error → fix compiler → ulangi dari step 1.

Ingat: semua test programs **bug-free**. Kalau gagal, yang harus diperbaiki adalah compiler-mu.

---

# Test Programs (unit-test incremental untuk codegen)
Disediakan 6 program untuk menguji kemampuan code generation secara bertahap. Kerjakan dalam urutan ini:

## 1) Seven
- Menguji: expression dengan integer constants (tanpa variables), `do`, `return`.
- Perilaku: menghitung `1 + (3 * 2)` dan print hasil `7` di kiri atas screen.
- Cara test: run di VM Emulator, pastikan tampil **7**.

## 2) ConvertToBin
- Menguji elemen prosedural Jack:
  - expressions (tanpa arrays atau method calls),
  - functions,
  - statements: `if`, `while`, `do`, `let`, `return`.
- Tidak menguji: methods, constructors, arrays, strings, static variables, field variables.
- Perilaku:
  - baca nilai desimal 16-bit dari `RAM[8000]`,
  - konversi jadi biner dan simpan bit di `RAM[8001]..RAM[8016]` (tiap lokasi 0 atau 1),
  - sebelum konversi, inisialisasi `RAM[8001]..RAM[8016]` ke `-1`.
- Cara test:
  - isi `RAM[8000]` dengan nilai desimal,
  - run beberapa detik, stop,
  - cek `RAM[8001]..RAM[8016]` berisi bit benar dan tidak ada `-1` tersisa.

## 3) Square (sama seperti Project 9 / Square)
- Menguji fitur object-based:
  - constructors, methods, fields,
  - expressions yang termasuk method calls.
- Tidak menguji: static variables.
- Perilaku: game kecil menggerakkan kotak dengan arrow keys, resize dengan `z`/`x`, quit dengan `q`.
- Cara test: mainkan di VM Emulator (pakai “no animation” + speed slider).

## 4) Average (sama seperti Project 9 Average / Project 10 ArrayTest)
- Menguji: arrays dan strings.
- Perilaku: menghitung rata-rata dari input integer sequence.
- Cara test: run dan ikuti instruksi di layar.

## 5) Pong
- Uji lengkap aplikasi object-based, termasuk **objects dan static variables**.
- Perilaku: game Pong klasik, ada score, paddle mengecil saat score naik, game over jika miss.
- Cara test: mainkan; pastikan score tampil dan berubah (no animation + speed slider).

## 6) ComplexArrays
- Menguji: complex array references dan expressions.
- Perilaku: melakukan 5 kalkulasi kompleks menggunakan arrays, lalu print “expected vs actual”.
- Cara test: pastikan expected == actual untuk semua kasus.

---

# Acceptance Criteria
Kamu dianggap selesai jika:
- compiler-mu menghasilkan `.vm` per `.jack` untuk file/folder input,
- semua test programs di atas **berjalan benar** di VM Emulator sesuai guideline masing-masing,
- tidak ada kebutuhan untuk memodifikasi program test.

---

# Checklist Cepat
- [ ] Backup Project 10 (Stage 0)
- [ ] SymbolTable benar untuk class + subroutine scope (Stage 1)
- [ ] Backup checkpoint (Stage 1.5)
- [ ] Codegen statements: let/if/while/do/return OK
- [ ] Codegen expressions (operators, unary, parentheses) OK
- [ ] Method/constructor semantics (this, Memory.alloc) OK
- [ ] Arrays (a[i]) OK
- [ ] Strings (String.new/appendChar) OK
- [ ] Static vars OK
- [ ] Lulus urutan test: Seven → ConvertToBin → Square → Average → Pong → ComplexArrays

---

## Links
- Project 11 page: https://www.nand2tetris.org/project11
- PDF guideline: Project 11.pdf (file yang kamu upload)
