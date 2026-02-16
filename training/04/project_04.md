# Project 4 — Machine Language (Nand to Tetris)

## Ringkasan
Project ini memperkenalkan **pemrograman low-level** menggunakan **Hack assembly language**. Kamu akan:
1) menulis program assembly,  
2) menerjemahkannya menjadi **binary machine code** menggunakan **assembler** yang disediakan, lalu  
3) mengeksekusi binary tersebut menggunakan **CPU Emulator** (karena hardware Hack computer baru selesai di Project 5).

---

## Objectives
- Mendapatkan pengalaman langsung pemrograman mesin (machine language).
- Mengenal **Hack instruction set** sebelum membangun Hack computer di Project 5.
- Mengenal proses **assembly** sebelum membangun assembler sendiri di Project 6.

---

## Tools
### 1) Editor
- Online IDE: editor sudah built-in (panel *source*).
- Desktop tools: gunakan text editor biasa (VS Code, dll).

### 2) Assembler
Assembler akan menerjemahkan `Xxx.asm` (symbolic Hack instructions) menjadi `Xxx.hack` (binary code) yang bisa dieksekusi oleh CPU Emulator / implementasi Hack CPU.

### 3) CPU Emulator
CPU Emulator mengeksekusi Hack machine code dan menampilkan state:
- memory (RAM),
- registers,
- program counter,
- screen,
- keyboard input (aktifkan input keyboard dari host PC).

---

## Warm-up: Jalankan program contoh dulu (recommended)
Sebelum menulis program kamu sendiri, **jalankan program yang sudah ada** untuk dapat “feel” machine language.

Program contoh (tersimpan di folder `projects/6`):
- `Add.asm` — menjumlahkan konstanta 2 dan 3, hasil ke `R0`.
- `Max.asm` — menghitung `max(R0, R1)` dan menyimpan ke `R2`. (Isi dulu nilai `R0` dan `R1` sebelum run.)
- `Rect.asm` — menggambar rectangle di kiri atas screen, lebar 16 pixel, tinggi `R0` pixel. (Isi `R0` sebelum run.)
- `Pong.asm` — game Pong (besar: puluhan ribu instruksi; load bisa agak lama).  
  Sebelum main: klik **enable keyboard**. Gunakan speed slider untuk mengatur kecepatan. Keluar dengan **ESC**.

### Workflow menjalankan program `Prog.asm` (Assembler + CPU Emulator)
Untuk tiap program:
1. Load `Prog.asm` ke assembler, baca dokumentasi tool, inspect code symbolic, lalu **translate** menjadi binary.
2. Klik **load** di panel “binary code” → CPU emulator akan terbuka dan binary akan diload ke emulator.
3. Jika program butuh input RAM: isi nilai di address RAM yang relevan (mis. `R0`, `R1`).
4. Jalankan program (step/run/reset).
5. Amati flow program dan dampaknya ke register, PC, dan memory.

---

## Program execution tips (CPU Emulator)
- Online CPU emulator umumnya self-explanatory.
- Desktop CPU emulator:
  - Jalankan `CPUEmulator.sh` (Mac/Linux) atau `CPUEmulator` (Windows) dari terminal/command line.
  - CPU emulator punya **builtin assembler**: kalau kamu load `.asm`, ia akan translate ke binary internal, termasuk resolve labels/variables.
  - Kamu bisa lihat code symbolic atau binary (pilih `bin` di display format menu panel ROM).
- Untuk program besar atau yang butuh screen/keyboard (mis. `Pong`, `Fill`):
  - Di desktop emulator, pilih **No animation** di menu *Animation* agar eksekusi tidak lambat.
- Ubah kecepatan eksekusi dengan **speed slider**.

---

## Tasks (Yang harus kamu buat)
Setelah warm-up, kembangkan **dua program** berikut.

### A) `Mult.asm` (Arithmetic task)
**Input:**
- `R0` = `RAM[0]`
- `R1` = `RAM[1]`

**Output:**
- `R2` = `RAM[2]` harus berisi `R0 * R1`

**Constraints / assumptions (tidak perlu dites dalam program):**
- `R0 ≥ 0`
- `R1 ≥ 0`
- `R0 * R1 < 32768`
- Program **tidak boleh mengubah** nilai `R0` dan `R1`.

**Testing:**
- Gunakan `Mult.tst` dan `Mult.cmp` untuk formal testing di CPU emulator.

### B) `Fill.asm` (Input/Output task)
Program harus berjalan **infinite loop** dan terus “mendengar” keyboard:

**Behavior:**
- Jika ada tombol ditekan (key down): **blacken** seluruh layar (tulis “black” di setiap pixel).
- Jika tidak ada tombol ditekan: **clear** layar (tulis “white” di setiap pixel).

**Catatan:**
- Urutan menyapu pixel bebas (top-down, bottom-up, spiral, dll).
- Syarat utama:  
  - Menekan tombol terus-menerus cukup lama → layar menjadi **hitam penuh**.  
  - Tidak menekan tombol cukup lama → layar menjadi **putih/bersih penuh**.

**Files:**
- Folder `projects/4` berisi skeleton `Mult.asm` dan `Fill.asm` yang harus kamu lengkapi.
- Untuk setiap program disediakan `Xxx.tst` dan `Xxx.cmp` untuk testing.
- `Fill.asm` juga punya **optional test**: `FillAutomatic.tst` dan `FillAutomatic.cmp` (baca dokumentasi `FillAutomatic.tst` jika ingin memakainya).

---

## Deliverables
- `projects/4/Mult/Mult.asm` (atau path setara di IDE kamu) — sudah lengkap dan lolos test.
- `projects/4/Fill/Fill.asm` — sudah lengkap dan lolos test.
- (Opsional) File hasil translate `Xxx.hack` untuk inspeksi/debug.

---

## Acceptance Criteria (Contract)
- `Mult.asm` harus lulus `Mult.tst` dan output match `Mult.cmp`.
- `Fill.asm` harus lulus `Fill.tst` dan output match `Fill.cmp`.
- Jika memakai optional test: `FillAutomatic.tst` harus match `FillAutomatic.cmp`.

---

## How to develop & test (Online IDE)
1. Load `Xxx.asm` ke editor assembler (panel *source*).
2. Edit `Xxx.asm` (auto-saved di browser). Untuk menyimpan lokal: klik **download** (zip semua `Xxx.asm` di project).
3. Klik **translate** untuk menghasilkan binary (IDE juga membentuk symbol table; belum perlu dipahami di project ini).
4. Klik **load** di panel “binary code” untuk membuka CPU emulator dan load program.
5. Informal testing:
   - Set RAM input jika diperlukan, atau klik **enable keyboard** jika program butuh keyboard.
   - Run/step/reset.
6. Formal testing:
   - Test panel biasanya sudah berisi `Xxx.tst`.
   - Jalankan test script. Jika fail → balik ke langkah 2.

---

## How to develop & test (Desktop tools)
0. Buka 3 window: editor (text editor), assembler, CPU emulator.
1. Edit `Xxx.asm` dan save.
2. Load `Xxx.asm` ke assembler dan translate (jika syntax error → kembali ke editor).
3. (Opsional) Save `Xxx.hack` di folder yang sama.
4. Load `Xxx.asm` atau `Xxx.hack` ke CPU emulator (boleh salah satu).
5. Informal testing:
   - Set RAM input / enable keyboard, lalu run/step/reset.
6. Formal testing:
   - Klik “load script”, load `projects/4/Xxx/Xxx.tst`, lalu execute.

### CLI assembler (opsional)
- Mac/Linux: `Assembler.sh Xxx.asm`
- Windows: `Assembler Xxx.asm`
Jika `Xxx.asm` valid, akan dibuat `Xxx.hack` di folder saat ini (tanpa output). Jika error, assembler menampilkan pesan error.

---

## Known bug / gotcha (dest mnemonic)
Secara spesifikasi Hack C-instruction, destinasi `DM=...` dan `ADM=...` valid. Namun beberapa assembler menganggap ini syntax error.
**Workaround:** gunakan `MD=...` atau `AMD=...` sebagai pengganti sampai bug diperbaiki.

---

## Programming tips (Hack assembly)
- Bahasa Hack **case sensitive**:
  - `@foo` dan `@Foo` adalah **dua simbol berbeda**.
- Hindari lowercase dan spasi dalam instruksi:
  - `m=1` atau `M = 1` → error.
  - Yang benar: `M=1`

**Best practices:**
- Label pakai UPPERCASE: `LOOP`, `END`
- Variabel pakai lowercase: `sum`, `i`
- Indent baris instruksi (yang bukan deklarasi label) beberapa spasi ke kanan.
- Tulis komentar seperlunya agar readable.
- Ikuti gaya program contoh (lecture/book).
- Strive for code yang rapi, efisien, dan self-explanatory.

---

## Checklist Cepat
- [ ] Sudah menjalankan `Add.asm`, `Max.asm`, `Rect.asm`, `Pong.asm` untuk warm-up
- [ ] `Mult.asm`:
  - [ ] tidak mengubah `R0`/`R1`
  - [ ] output benar di `R2`
  - [ ] lulus `Mult.tst`
- [ ] `Fill.asm`:
  - [ ] loop tak berhingga (continually listening keyboard)
  - [ ] key pressed → black screen, no key → white screen
  - [ ] lulus `Fill.tst` (opsional: `FillAutomatic.tst`)
- [ ] Tidak memakai dest `DM`/`ADM` (gunakan `MD`/`AMD`)

---

*Copyright notice (as in original materials): nand2tetris.org — Noam Nisan & Shimon Schocken.*
