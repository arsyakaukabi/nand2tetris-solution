# Project 10 — Compiler I: Syntax Analysis (Jack) — Requirements & Instructions

## Ringkasan
Pada **Project 10** kamu mulai membangun **compiler Jack** dalam 2 tahap besar:
- **Project 10:** *syntax analysis / parsing* → output **XML** yang merepresentasikan struktur sintaks program Jack.
- **Project 11:** extend parsing menjadi compiler penuh → output **VM code** yang executable.

Versi Project 10 ini mengasumsikan input Jack **valid** (error-free). Jadi kamu **tidak wajib** membuat error checking / reporting.

---

## Objective
Bangun **syntax analyzer** yang mem-parse program Jack sesuai **Jack grammar**, lalu mengeluarkan **XML** yang merefleksikan struktur sintaks dari source.

---

## Contract
Tulis **JackAnalyzer** (program utama) yang:
- menerima input berupa **1 file** `Xxx.jack` **atau** sebuah **folder** berisi banyak `.jack`,
- memproses setiap file `.jack` secara terpisah,
- menghasilkan file output XML sesuai spesifikasi,
- dan output XML harus **identik** dengan file compare (`.xml`) yang disediakan **(perbedaan whitespace diabaikan)**.

---

## Tools yang Dibutuhkan
- Bahasa pemrograman pilihanmu (untuk implementasi analyzer).
- **TextComparer** (atau tool serupa) untuk membandingkan file sambil mengabaikan whitespace.
- (Opsional) XML viewer: browser apa pun (File → Open untuk melihat XML).

---

## Test Files (disediakan)
Project menyediakan beberapa file `.jack` untuk testing, termasuk program:
- **Square** (3 class) — program interaktif “gerak kotak”.
- **ArrayTest** (1 class) — menghitung rata-rata angka input menggunakan array.

Catatan: source ini sudah “diperkaya” agar mencakup lebih banyak fitur grammar Jack (mis. `static`, `else`, unary operators), sehingga parser-mu diuji lebih lengkap.

---

# Deliverables
Kamu akan menghasilkan dua jenis output (dua milestone utama):

## Deliverable A — Tokenizer output (XxxT.xml)
Untuk setiap input `Xxx.jack`, buat output:
- `XxxT.xml` (**T = tokenized output**)

Output ini adalah daftar token yang sudah di-tokenize, satu token per baris, dengan format:
```xml
<tokens>
  <tokenType> token </tokenType>
  ...
</tokens>
```
`tokenType` adalah salah satu dari 5 tipe token Jack:
- `keyword`
- `symbol`
- `identifier`
- `integerConstant`
- `stringConstant`

## Deliverable B — Parsed output (Xxx.xml)
Untuk setiap input `Xxx.jack`, buat output:
- `Xxx.xml` (hasil parsing / syntax tree dalam format XML)

Output ini dihasilkan oleh **CompilationEngine** yang memanggil rutinitas compile secara rekursif dan “emit” XML structure.

---

# Program Architecture (yang disarankan / standar course)

## 1) JackAnalyzer (main)
Program CLI yang dipanggil sebagai:
```bash
JackAnalyzer source
```
Di mana `source` adalah:
- `Xxx.jack` (extension wajib), atau
- nama folder (tanpa extension), yang berisi satu atau lebih `.jack`

**Behavior:**
- Jika input = file → proses file itu.
- Jika input = folder → temukan semua file `*.jack` di folder tersebut, proses satu per satu.
- Untuk setiap file, buat tokenizer + output file, lalu jalankan pipeline sesuai milestone.

## 2) JackTokenizer
Modul tokenizer sesuai lecture:
- membaca char stream,
- membuang whitespace & comments,
- memproduksi token stream (advance/peek),
- expose API untuk: `tokenType`, `keyword`, `symbol`, `identifier`, `intVal`, `stringVal`, dll.

## 3) CompilationEngine
Modul parser (recursive descent) yang:
- menerima tokenizer (token stream),
- menjalankan `compileClass()` sebagai entry point,
- dan memanggil metode compile lain secara rekursif,
- sambil menulis XML output `Xxx.xml`.

---

# Milestone Plan (urut yang paling aman)

## Milestone 1 — Tokenizer + JackAnalyzer versi tokenization
### Task
- Implement **JackTokenizer**.
- Buat JackAnalyzer “basic” yang:
  - untuk tiap `Xxx.jack` menghasilkan `XxxT.xml`
  - looping token demi token (advance) sampai habis
  - print satu token per baris dalam format XML.

### XML technicalities (wajib)
1) File output token harus dibungkus tag:
```xml
<tokens>
...
</tokens>
```

2) String constant: **abaikan tanda kutip ganda**
- Input: `"yes"`
- Output token: `<stringConstant> yes </stringConstant>` (tanpa `"`)

3) Escape sequence untuk simbol yang bentrok dengan markup XML:
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`
- `&` → `&amp;`

Contoh: jika input berisi simbol `<`, output token:
```xml
<symbol> &lt; </symbol>
```

### Testing
- Jalankan analyzer pada test `.jack`.
- Compare `XxxT.xml` hasilmu dengan compare file `XxxT.xml` yang disediakan menggunakan TextComparer (ignore whitespace).
- Karena nama file sama, simpan output kamu dan compare files di folder terpisah.

---

## Milestone 2 — Parser tanpa expressions & arrays (ExpressionlessSquare)
### Task
- Implement **CompilationEngine** untuk semua elemen Jack **kecuali**:
  - routines yang menangani **expressions**, dan
  - routines yang menangani **array-oriented commands**.
- Update JackAnalyzer agar:
  - output parser bernama `Xxx.xml`
  - setelah membuat tokenizer + output writer, langsung memanggil:
    - `CompilationEngine.compileClass()`

### Unit test khusus
- Test pada folder **ExpressionlessSquare**.
  - Ini adalah versi Square di mana setiap expression diganti dengan **single identifier**.
  - Kodenya “nonsensical secara semantik”, tapi tetap valid secara sintaks—bagus untuk menguji parser struktural.

### Testing
- Compare XML output yang kamu hasilkan dengan compare files yang disediakan.

---

## Milestone 3 — Tambahkan expression parsing (test pada Square)
### Task
- Lengkapi routines CompilationEngine untuk **expressions**.
- Test kembali menggunakan folder **Square**.

---

## Milestone 4 — Tambahkan array handling (test pada ArrayTest)
### Task
- Lengkapi routines CompilationEngine untuk **array-oriented commands**.
- Test menggunakan folder **ArrayTest**.

---

# Acceptance Criteria (Contract Check)
Kamu dianggap selesai jika:
- `JackAnalyzer source` berjalan untuk file maupun folder,
- menghasilkan `XxxT.xml` tokenized output yang match compare files (whitespace ignored),
- menghasilkan `Xxx.xml` parsed output yang match compare files (whitespace ignored),
- lulus test sequence:
  1) Token tests (`*T.xml`),
  2) ExpressionlessSquare,
  3) Square,
  4) ArrayTest.

---

# Technical Notes (penting untuk menghindari mismatch)
1) **Whitespace normalization**  
   Setelah comments & whitespace dibuang, whitespace diperlakukan sebagai satu spasi.  
   Contoh: `let__x___=_17;` harus diperlakukan seperti `let_x_=_17;`.

2) **Keywords tidak boleh jadi identifier**  
   Jadi tokenizer/parser tidak boleh mengkategorikan keyword sebagai identifier.

3) **Empty tags harus 2 baris**  
   Jika ada tag pembuka dan penutup tanpa isi di antara keduanya, format harus:
```xml
<xxx>
</xxx>
```
Bukan `<xxx></xxx>`. Ini penting terutama untuk empty parameter list.

4) **Indentation netral**  
   Indentasi tidak dinilai (ignored), tapi sangat disarankan agar output mudah dibaca dan debug lebih cepat.

---

# Checklist Cepat
- [ ] `JackAnalyzer Xxx.jack` menghasilkan `XxxT.xml`
- [ ] `JackAnalyzer Folder/` memproses semua `.jack` dalam folder
- [ ] Escape XML symbols: `<, >, ", &` → `&lt; &gt; &quot; &amp;`
- [ ] String constant output tidak mengandung `"`
- [ ] Parser stage-by-stage lulus: ExpressionlessSquare → Square → ArrayTest
- [ ] Output match compare files (whitespace ignored)

---

## Links
- Project 10 page: https://www.nand2tetris.org/project10
- PDF guideline: Project 10.pdf (file yang kamu upload)
