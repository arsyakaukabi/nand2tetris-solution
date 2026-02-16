# Step-by-Step Simulasi `FibonacciElement` di Web-IDE

Panduan ini untuk menjalankan simulasi Project 8 (`FibonacciElement`) dari instalasi sampai test.

## 1) Prasyarat

- OS: macOS / Linux / Windows
- Node.js LTS (disarankan v20+)
- npm (ikut Node.js)
- Git

Cek cepat:

```bash
node -v
npm -v
git --version
```

## 2) Clone dan install dependency

```bash
git clone https://github.com/arsyakaukabi/nand2tetris-solution.git
cd nand2tetris/web-ide
npm install
```

## 3) Build dan jalankan Web-IDE lokal

```bash
npm run build
npm run start
```

Setelah itu terminal akan menampilkan URL lokal (biasanya `http://localhost:5173` atau sejenis).  
Buka URL tersebut di browser.

## 4) Siapkan file uji `FibonacciElement`

Di repo ini file test ada di:
- `training/08/project_08/FunctionCalls/FibonacciElement/Main.vm`
- `training/08/project_08/FunctionCalls/FibonacciElement/Sys.vm`
- `training/08/project_08/FunctionCalls/FibonacciElement/FibonacciElementVME.tst`
- `training/08/project_08/FunctionCalls/FibonacciElement/FibonacciElement.tst`
- `training/08/project_08/FunctionCalls/FibonacciElement/FibonacciElement.cmp`
- `training/08/project_08/FunctionCalls/FibonacciElement/FibonacciElement.asm`

Di UI web-ide, buat folder `FibonacciElement/`, lalu copy isi file-file di atas ke file dengan nama yang sama.

## 5) Simulasi mode VM (cek logic VM dulu)

1. Masuk ke tab/halaman **VM**.
2. Buka `FibonacciElement/FibonacciElementVME.tst`.
3. Jalankan test (`Run` / `▶`).
4. Pastikan output dibandingkan ke `FibonacciElement.cmp` dan status **pass**.

Tujuan tahap ini: validasi perilaku VM program (`Main.vm` + `Sys.vm`) sebelum fokus ke level ASM.

## 6) Simulasi mode CPU (cek hasil translasi ASM)

1. Masuk ke tab/halaman **CPU**.
2. Buka `FibonacciElement/FibonacciElement.tst`.
3. Pastikan file `FibonacciElement.asm` ada di folder yang sama.
4. Jalankan test.
5. Pastikan compare dengan `FibonacciElement.cmp` menghasilkan **pass**.

Tujuan tahap ini: validasi output translator VM (`.asm`) berjalan benar di CPU Hack.

## 7) Alur debug jika gagal

Urutan debug paling aman:

1. Jalankan dulu `FibonacciElementVME.tst` (VM mode)
2. Jika VM pass tapi CPU fail, masalah biasanya di `VMTranslator` (template ASM `call/return/bootstrap`)
3. Cek ulang poin kritis:
   - bootstrap: `SP=256` lalu `call Sys.init`
   - `call`: push return address + `LCL/ARG/THIS/THAT`
   - `return`: restore frame dan jump ke return address
   - static symbol harus namespace per file

## 8) Opsional: verifikasi via CLI (lebih cepat untuk regression)

Jika CLI sudah terpasang:

```bash
cd training/08/project_08/FunctionCalls/FibonacciElement
nand2tetris run FibonacciElement.tst
```

Ini berguna untuk cek cepat setelah edit translator, lalu final check tetap bisa dilihat di web-ide.
