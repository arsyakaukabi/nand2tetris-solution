# Cara Kerja VM, ASM, dan Memory Segmentation (Contoh: `FibonacciElement`)

Dokumen ini menjelaskan alur dari program VM sampai jalan di Hack CPU, pakai test **Project 8: FibonacciElement**.

## 1) Gambaran Besar: VM → ASM → CPU

Pada `FibonacciElement`, ada dua file VM:
- `Sys.vm` (entry point: `Sys.init`)
- `Main.vm` (fungsi rekursif `Main.fibonacci`)

Translator (`VMTranslator.py`) melakukan:
1. Baca command VM (`push`, `call`, `return`, `if-goto`, dll)
2. Ubah tiap command jadi template Hack Assembly
3. Gabungkan hasilnya jadi `FibonacciElement.asm`

Saat `.asm` dijalankan, Hack CPU hanya mengeksekusi instruksi assembly; konsep “function VM” sebenarnya disimulasikan lewat manipulasi stack dan pointer RAM.

## 2) Peran Segmen Memori VM

VM memakai segmen logis, dipetakan ke register/pointer Hack:
- `local`  → basis di `LCL`
- `argument` → basis di `ARG`
- `this` → basis di `THIS`
- `that` → basis di `THAT`
- `temp` → `R5..R12`
- `pointer 0/1` → `THIS` / `THAT`
- `static i` → simbol unik `FileName.i`
- `constant` → nilai literal (tidak baca RAM)

Untuk `FibonacciElement`, yang paling penting adalah `argument`, `local`, dan mekanisme call frame (`LCL`, `ARG`, `THIS`, `THAT`).

## 3) Bootstrap di Program Multi-file

Karena `FibonacciElement` adalah folder multi-file, translator menulis bootstrap:
1. `SP = 256`
2. `call Sys.init 0`

Ini membuat VM punya titik awal standar sebelum fungsi lain dipanggil.

## 4) Mekanisme `call` dan `return` (inti Project 8)

### Saat `call f nArgs`
Translator menghasilkan ASM yang:
1. Push return-address
2. Push `LCL`, `ARG`, `THIS`, `THAT` milik caller
3. Set `ARG = SP - 5 - nArgs`
4. Set `LCL = SP`
5. Lompat ke label fungsi `f`

Artinya kita bikin **stack frame baru** untuk callee.

### Saat `return`
ASM akan:
1. Simpan `FRAME = LCL`
2. Ambil `RET = *(FRAME-5)`
3. Pindahkan nilai return: `*ARG = pop()`
4. Pulihkan `SP = ARG + 1`
5. Restore `THAT`, `THIS`, `ARG`, `LCL` dari frame lama
6. `goto RET`

Jadi kontrol balik ke caller dengan state yang benar.

## 5) Contoh Alur `FibonacciElement`

Ringkasnya:
1. Bootstrap memanggil `Sys.init`
2. `Sys.init` push `4`, lalu `call Main.fibonacci 1`
3. `Main.fibonacci(n)`:
   - jika `n < 2`, return `n` (base case)
   - else hitung rekursif:
     - `fib(n-2)`
     - `fib(n-1)`
     - `add`
     - `return`
4. Hasil akhir (untuk `n=4`) kembali ke caller dan ditaruh di stack sesuai kontrak VM

Semua rekursi ini berjalan benar karena setiap call punya frame sendiri (`LCL/ARG/...`) sehingga argumen dan local antar level rekursi tidak saling menimpa.

## 6) Kenapa VM Membantu?

VM membuat compiler front-end (mis. Jack compiler) tidak perlu tahu detail hardware Hack.  
Cukup hasilkan VM command standar, lalu VM Translator yang menangani detail rendah (ASM, stack frame, label unik, memory mapping).

Di `FibonacciElement`, manfaat ini terlihat jelas: logika rekursif di VM tetap bersih, sedangkan kompleksitas call stack dipindahkan ke translator ASM.
