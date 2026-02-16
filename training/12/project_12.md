# Project 12 — Operating System (Jack OS) — Requirements & Instructions

## Ringkasan
Operating System (OS) adalah kumpulan layanan software yang “menjembatani” gap antara hardware dan software tingkat tinggi. Dalam ekosistem Nand2Tetris, program Jack yang berinteraksi dengan **keyboard** dan **screen** akan memanggil rutin OS seperti `Keyboard.*`, `Screen.*`, `Output.*`, dll.

Di Project 12 (project terakhir), kamu akan mengimplementasikan **Jack OS**: **8 kelas** OS dalam Jack yang menyediakan layanan umum seperti I/O, operasi matematika, string processing, dan memory management.

---

## Objective
Implementasikan **operating system** yang dijelaskan di lecture (Jack OS).

---

## Contract
- Implementasikan Jack OS dalam **Jack**.
- Uji implementasimu menggunakan test programs dan skenario testing yang disediakan.
- Setiap kelas OS dapat diimplementasikan dan **unit-tested secara terpisah** dan **dalam urutan apa pun**.

---

## Deliverables
Folder `projects/12` akan berisi **8 file skeletal** (berisi signature semua subroutine). Tugasmu adalah mengisi implementasinya:

- `Math.jack`
- `String.jack`
- `Array.jack`
- `Memory.jack`
- `Screen.jack`
- `Output.jack`
- `Keyboard.jack`
- `Sys.jack`

Deliverable final:
- Implementasi lengkap 8 file `.jack` di atas, sehingga seluruh test lulus.
- (Opsional tapi sangat membantu) komentar internal dan helper private methods untuk mempermudah debug.

---

## Tools yang Dibutuhkan
- **Jack language** (kamu menulis OS dalam Jack).
- **Supplied Jack compiler** (untuk compile `.jack → .vm`).
- **Supplied VM Emulator** (untuk menjalankan `.vm` dan test scripts).
- **Test programs** (disediakan, ditulis juga dalam Jack).

Tambahan resource resmi:
- **Jack OS API** + daftar **OS error codes** dan artinya (dipakai sebagai spesifikasi fungsi & perilaku).

---

## Built-in OS di VM Emulator (penting untuk strategi test)
VM Emulator memiliki implementasi OS **builtin**.

Saat emulator mengeksekusi VM command `call Foo`:
- Jika function `Foo` ada di code base yang kamu load (hasil compile folder), emulator menjalankan VM code kamu.
- Jika `Foo` **tidak** ada di code base yang kamu load, emulator mengecek apakah `Foo` adalah fungsi OS builtin.
  - Jika ya, emulator menjalankan builtin implementation.

Konsekuensi penting:
- Kamu bisa **test satu kelas OS** dulu, walaupun kelas itu memanggil layanan OS lain yang belum kamu implementasi—emulator akan fallback ke builtin untuk fungsi yang belum ada.

---

# Testing Plan (cara test per kelas)

## Struktur test
Di `projects/12` ada **8 folder test** (satu per kelas), misalnya:
- `MathTest`, `MemoryTest`, …, dst.
Setiap folder berisi program Jack yang menguji layanan dari kelas OS terkait.
Beberapa folder punya `.tst` script + `.cmp` compare file, beberapa hanya `.jack`.

## Prosedur umum untuk test kelas OS `Xxx`
1) **Inspect** source test program di `XxxTest/*.jack`.
   - Pahami layanan apa yang diuji dan bagaimana cara mengujinya.
2) Copy file OS yang sedang kamu implementasikan (`Xxx.jack`) ke folder `XxxTest/`.
3) **Compile folder** `XxxTest/` menggunakan supplied Jack compiler.
   - Hasilnya: `.vm` untuk OS class kamu + `.vm` untuk test program, semuanya di folder yang sama.
4) Jalankan test:
   - Jika folder punya `XxxTest.tst` → load script ini ke VM Emulator.
   - Jika tidak ada `.tst` → load folder ke VM Emulator.
5) Ikuti guideline test spesifik untuk kelas tersebut (lihat bagian berikut).

---

## Guideline test spesifik per kelas

### 1) Math / Memory / Array (script + compare)
Folder test untuk tiga kelas ini menyertakan:
- `.tst` test script dan `.cmp` compare file

Pola test script:
- `load` → load semua `.vm` di folder saat ini
- buat output file
- load compare file
- jalankan serangkaian test dan bandingkan output dengan compare file

Target lulus:
- seluruh perbandingan berakhir sukses (“Comparison ended successfully”).

Catatan penting:
- Test yang disediakan **tidak mencakup pengujian penuh** untuk `Memory.alloc` dan `Memory.deAlloc`.
  - Kalau kamu ingin menguji lebih lengkap, lakukan step-by-step debugging di VM Emulator dan inspeksi lokasi RAM yang berubah.

### 2) String
Test string bersifat “expected output” di screen.
Target:
- Menjalankan program test harus menghasilkan output string test tertentu (lihat screenshot expected output di PDF).

### 3) Output
Test output juga berbasis “expected output”.
Target:
- Menjalankan program test harus menghasilkan tampilan teks/karakter sesuai screenshot expected output di PDF.

### 4) Screen
Test screen juga berbasis “expected output” (gambar).
Target:
- Menjalankan program test harus menggambar scene (mis. bentuk rumah + matahari, dll) sesuai screenshot expected output di PDF.

### 5) Keyboard
Test keyboard berbasis interaksi user.
Untuk setiap fungsi di `Keyboard`:
- `keyPressed`
- `readChar`
- `readLine`
- `readInt`

Program akan meminta user menekan/memasukkan sesuatu.
- Jika implementasi benar (dan input yang diminta diberikan), program print `"ok"` dan lanjut ke test berikutnya.
- Jika salah, program mengulang request.
Jika semua sukses, program akan print `"Test ended successfully"` dan layar akan sesuai screenshot di PDF.

### 6) Sys
- Test yang disediakan menguji `Sys.wait`:
  - program meminta user menekan key (any key),
  - lalu menunggu 2 detik via `Sys.wait`,
  - lalu print message.
  - Pastikan delay dari key-release ke message kurang lebih **2 detik**.

- `Sys.init` **tidak** diuji secara eksplisit.
  - Namun `Sys.init` melakukan inisialisasi OS dan memanggil `Main.main` dari test program.
  - Jadi, secara praktis, kalau `Sys.init` salah, “seharusnya tidak ada yang jalan dengan benar”.

---

## Complete integrated test (end-to-end)
Setelah semua kelas lulus unit-test, lakukan test integrasi memakai **Pong** (dari project sebelumnya):
1) Ambil source Pong dari `projects/11/Pong`.
2) Copy **8 file OS `.jack`** kamu ke folder `Pong/`.
3) Compile folder Pong dengan supplied Jack compiler.
4) Load folder Pong di VM Emulator, jalankan game, dan pastikan bekerja normal.

Catatan:
- Jika kamu baru mengimplementasikan sebagian OS, integrated test masih bisa jalan karena emulator akan fallback ke builtin OS untuk fungsi yang belum ada.

---

# Implementation Notes (praktis, biar eksekusi mulus)

## Build order yang biasanya efisien (opsional)
Kamu *boleh* implementasi dalam urutan apa pun, tetapi urutan berikut sering memudahkan:
1) `Math` (paling isolated)
2) `Memory` + `Array` (heap/array support)
3) `String` (butuh Memory/Array)
4) `Output` (butuh Screen/String)
5) `Screen`
6) `Keyboard`
7) `Sys` (init + wait)

> Karena ada builtin OS, kamu bisa tetap mengerjakan “yang kamu mau dulu” tanpa deadlock dependency.

## Prinsip debugging
- Kalau test berbasis `.tst/.cmp` gagal → gunakan “step” + inspeksi output file / RAM.
- Kalau test berbasis screenshot output (String/Output/Screen/Keyboard) → jalankan program test dan bandingkan tampilan dengan expected output (di PDF).
- Selalu isolasi: test satu kelas dulu di folder `XxxTest` sebelum lanjut implementasi kelas lain.

---

## Checklist Cepat
- [ ] 8 kelas OS (`Math`, `String`, `Array`, `Memory`, `Screen`, `Output`, `Keyboard`, `Sys`) terisi implementasi
- [ ] MathTest / MemoryTest / ArrayTest lulus `.tst` vs `.cmp`
- [ ] String test output sesuai screenshot
- [ ] Output test output sesuai screenshot
- [ ] Screen test output sesuai screenshot
- [ ] Keyboard test: semua step print `"ok"` dan berakhir `"Test ended successfully"`
- [ ] Sys.wait delay ~2 detik dan Sys.init membuat test berjalan
- [ ] Integrated test: Pong berjalan normal dengan OS kamu

---

## Links
- Project 12 page: https://www.nand2tetris.org/project12
- PDF guideline: Project 12.pdf (file yang kamu upload)
