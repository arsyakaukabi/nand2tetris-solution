# Project 6 — Assembler (Nand to Tetris)

## Ringkasan
Program low-level yang ditulis dalam **symbolic machine language** disebut **assembly program**. Program yang menerjemahkan assembly menjadi binary machine code disebut **assembler**.

Di Project 6 kamu akan membuat **Hack Assembler**: menerjemahkan file `Prog.asm` (Hack assembly) menjadi `Prog.hack` (Hack binary code).

---

## Objective
- Develop an assembler yang menerjemahkan **Hack assembly language** → **Hack binary code**.
- Versi assembler untuk project ini **mengasumsikan source assembly valid** (tidak perlu error checking / reporting).
- Jika kamu tidak punya pengalaman programming, kamu boleh melakukan **manual assembly** (opsi manual ada di bawah).

---

## Contract (Kontrak)
Saat diberi input `Prog.asm` yang valid, assembler kamu harus:
1. menerjemahkan program dengan benar menjadi Hack binary,
2. menyimpan output ke file **`Prog.hack`**,
3. file output berada di **folder yang sama** dengan file sumber,
4. jika `Prog.hack` sudah ada, **overwrite**,
5. output `Prog.hack` harus **identik** dengan output dari assembler resmi (supplied assembler).

---

## Test Programs (Disediakan)
Empat program uji (sama seperti Project 4):
- `Add.asm` — menambahkan konstanta 2 dan 3, simpan hasil ke `R0`.
- `Max.asm` — hitung `max(R0, R1)`, simpan ke `R2`.
- `Rect.asm` — gambar rectangle di top-left, lebar 16 pixel, tinggi `R0`.
- `Pong.asm` — game Pong; file assembly besar untuk **stress-test** assembler.

---

## Tools
Yang kamu butuhkan:
- Bahasa pemrograman pilihanmu untuk mengimplementasikan assembler (Python/Java/Go/JS, dll).
- **Supplied assembler** (resmi) untuk membandingkan output `Prog.hack` buatanmu.
- (Opsional) **CPU Emulator** untuk mengeksekusi `Prog.hack` dan melihat perilakunya.

> Menjalankan `Prog.hack` di CPU emulator bukan bagian dari assembly process, tapi bisa jadi uji tidak langsung yang memuaskan.

---

## Development Plan (Disarankan: 2 tahap)
Bangun dan test assembler dalam **dua stage**:

### Stage I — Basic assembler (tanpa simbol)
Target: mendukung program yang **tidak memiliki symbolic references** (tanpa variables & labels).

**Test Stage I pada:**
- `Add.asm`
- `MaxL.asm`
- `RectL.asm`
- `PongL.asm`

> `ProgL.asm` adalah versi **tanpa** symbolic references dari `Prog.asm` (Max/Rect/Pong).

### Stage II — Full assembler (dengan simbol)
Tambahkan kemampuan symbol handling (variables & labels).

**Test Stage II pada:**
- `Add.asm`
- `Max.asm`
- `Rect.asm`
- `Pong.asm`

---

## Testing Your Assembler
Ada 2 cara utama untuk verifikasi:

### A) Behavioral test (execute di CPU emulator)
1. Jalankan assembler kamu → hasilkan `Prog.hack`.
2. Load `Prog.hack` ke CPU emulator.
3. Eksekusi program, pastikan behavior sesuai dokumentasi program (mis. Max benar, Rect menggambar benar, Pong playable).

### B) Golden test (compare dengan supplied assembler) — paling tegas
Pastikan output `Prog.hack` kamu **identik** dengan output assembler resmi.

#### Online IDE workflow (Compare code panel)
1. Load `Prog.asm` ke assembler tool online, klik **Translate**.
2. Ambil output `Prog.hack` hasil assembler kamu (di text editor), **copy-paste** ke panel **Compare code**.
3. Klik **Compare** → harus “Comparison successful”.

#### Desktop assembler workflow (Equals button)
1. Rename `Prog.hack` buatanmu menjadi, misalnya, `Prog1.hack`.
2. Load `Prog.asm` ke desktop assembler resmi dan **Translate**.
3. Klik tombol **equals**, load `Prog1.hack`, lalu compare.

---

## Output / Deliverables
- Program assembler kamu (kode sumber) yang dapat dijalankan untuk menerjemahkan `Xxx.asm` → `Xxx.hack`.
- Untuk setiap test program, hasil `Xxx.hack` buatanmu harus match output assembler resmi.

Minimal bukti kerja:
- Stage I: `Add.hack`, `MaxL.hack`, `RectL.hack`, `PongL.hack` match.
- Stage II: `Add.hack`, `Max.hack`, `Rect.hack`, `Pong.hack` match.

---

## Implementation Notes (Praktis, supaya eksekusi mulus)

### Arsitektur solusi yang umum
Buat komponen berikut (nama bebas):
- **Parser**: baca file, buang whitespace & komentar, iterasi instruction per instruction.
- **SymbolTable**: mapping `symbol → address`.
- **Code module**: mapping mnemonic ke bit pattern (`dest`, `comp`, `jump`).

### Two-pass algorithm (intinya)
1. **First pass (labels)**  
   - Jalanin parser, hitung ROM address untuk tiap instruction.
   - Saat ketemu `(LABEL)`: simpan `LABEL → current_rom_address` ke symbol table.
   - Tidak generate code.

2. **Second pass (codegen)**  
   - Translate tiap instruction jadi 16-bit binary.
   - Untuk `@symbol`:
     - Jika `symbol` angka → pakai langsung.
     - Jika `symbol` label/predefined → resolve dari symbol table.
     - Jika `symbol` variable baru → assign ke RAM mulai dari address 16, simpan ke symbol table.
   - Untuk C-instruction → encode `comp/dest/jump`.

---

## Software Update (Desktop tools only)
Jika kamu memakai desktop assembler, pastikan file Project 6 kamu versi terbaru:
- re-download paket Nand2Tetris,
- copy folder `projects/6` dari paket baru ke `projects/6` di PC-mu
- folder project lain tidak perlu diubah.

Lakukan ini **sebelum** mulai Project 6.

---

## Known Bug / Gotcha (dest mnemonic)
Menurut spesifikasi Hack C-instruction, destinasi `DM=...` dan `ADM=...` valid.
Namun beberapa assembler menganggap itu syntax error dan mengharapkan `MD=...` serta `AMD=...`.

**Requirement untuk assembler kamu:**
- Terima **DM atau MD** sebagai destinasi dengan d-bits `011`
- Terima **ADM atau AMD** sebagai destinasi dengan d-bits `111`

---

## Manual Assembler Option (Jika tidak coding)
Jika kamu belum siap membuat program assembler, kamu bisa latihan dengan menerjemahkan `.asm` → `.hack` secara manual:
- Pakai text editor,
- output adalah barisan baris 16-bit (`0/1`) per instruction,
- lakukan **first pass** untuk label (bangun symbol table; generate no code),
- lakukan **second pass** untuk menerjemahkan instruksi, sambil menambahkan variables ke symbol table.

**Testing manual translation (disarankan bertahap):**
- Tahap 1 (tanpa simbol): translate `Add.asm`, `MaxL.asm`, `RectL.asm`.
- Tahap 2 (dengan simbol): translate `Max.asm`, `Rect.asm`.
- `Pong.asm` terlalu panjang → tidak wajib diterjemahkan manual.

Setelah translate manual, test output `.hack` dengan cara compare terhadap assembler resmi (lihat bagian Testing).

---

## Tutorials / References
- Assembler tutorial (desktop)
- CPU Emulator demo/tutorial (untuk menjalankan `.hack`)

---

## Checklist Cepat
- [ ] Memahami contract: `Prog.asm` → `Prog.hack` (same folder, overwrite, output identik assembler resmi)
- [ ] Stage I selesai & match: Add, MaxL, RectL, PongL
- [ ] Stage II selesai & match: Add, Max, Rect, Pong
- [ ] Testing via compare (online Compare code / desktop equals)
- [ ] Desktop: sudah update folder `projects/6` (jika perlu)
- [ ] Handle bug dest: DM/MD dan ADM/AMD dianggap setara

---

*Copyright notice (as in original materials): nand2tetris.org — Noam Nisan & Shimon Schocken.*
