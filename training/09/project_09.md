# Project 9 — High-Level Programming (Jack) — Requirements & Instructions

## Ringkasan
Di project ini kamu akan menulis **program interaktif** dalam bahasa **Jack** (mirip Java, OOP sederhana). Ini “pemanasan wajib” sebelum:
- Project 10–11: membangun **Jack compiler**, dan
- Project 12: membangun **Jack OS**.

Selain itu, ini juga latihan penting untuk membuat program yang menggabungkan **grafik + animasi + input user**.

---

## Objective
**Invent / adopt** ide aplikasi (biasanya game sederhana) dan implementasikan dalam **Jack**.  
Contoh ide: Tetris, Snake, Space Invaders, Sokoban, Pong, Hangman, dsb.

> Kamu tidak harus membuat game “complete”. Versi basic / subset fitur sudah cukup, asal interaktif dan jelas.

---

## Contract (Kontrak)
Buat sebuah program interaktif dalam Jack, terdiri dari **1 atau lebih class** (`ClassName.jack`), dan bisa:
1) di-compile dengan **supplied JackCompiler** menjadi file-file `.vm`, lalu
2) dijalankan di **VM Emulator**, dengan perilaku sesuai desain game-mu.

---

## Deliverables
Minimal:
- 1 folder program (mis. `FlappyBird/`)
- Berisi **source** `.jack` (1 class per file)
- Berisi hasil compile `.vm` (generated oleh JackCompiler)

Jika kamu mengikuti Coursera (submission umum):
- Zip berisi folder program (dengan `.vm`), dan
- folder `source/` yang berisi semua file `.jack` (source yang readable + documented).

---

## Tools yang kamu pakai
- **Text editor** untuk menulis `.jack`
- **JackCompiler** (supplied) untuk compile `.jack → .vm`
- **VM Emulator** (supplied) untuk menjalankan & debug runtime

---

## Cara Compile & Run (Workflow resmi yang aman)
0) Buat folder program (contoh: `FlappyBird/`)  
1) Tulis program Jack: beberapa file `ClassName.jack` di folder itu  
2) Jalankan **JackCompiler** pada folder tersebut  
   - Compiler akan menerjemahkan semua `.jack` menjadi `.vm` di folder yang sama  
   - Jika ada error compile → perbaiki `.jack` → compile ulang sampai clean  
3) Jalankan program:
   - Load folder program ke **VM Emulator**
   - Run / step / debug
   - Jika runtime error / behavior salah → perbaiki `.jack` → balik ke step 2

---

## The Jack OS (Native vs Builtin)
Menulis Jack biasanya memanggil service OS seperti `Screen.*`, `Keyboard.*`, `Output.*`, `Math.*`, dll.

Ada 2 cara menggunakan Jack OS:
1) **Builtin OS** (lebih cepat): OS di-embed di VM Emulator → kamu **tidak perlu** copy file OS.  
2) **Native / Compiled OS**: OS disediakan sebagai 8 file `.vm` (Math, Screen, Output, Keyboard, Memory, String, Array, Sys).  
   - Lokasi umum: `nand2tetris/tools/os/`  
   - Jika kamu ingin pakai ini, copy 8 file `.vm` tersebut ke folder program-mu sebelum run.

VM Emulator akan:
- pakai implementasi OS dari folder program **jika tersedia**, dan
- fallback ke builtin OS untuk fungsi OS yang tidak ada di folder program.

> Untuk Project 9, pakai builtin OS saja biasanya paling simpel.

---

## Resources yang direkomendasikan
- **Sample program**: `nand2tetris/projects/09/Square/` (3-class). Disarankan kamu baca & mainkan dulu.  
- **Jack OS API** & error codes (berguna untuk debug).
- **Bitmap editor / sprite generator** (opsional) untuk grafik cepat, kalau butuh sprite berulang.

---

## Kriteria evaluasi (umum di course)
Biasanya dinilai dari:
- Code quality + documentation: ~40%
- User experience: ~50%
- Originality: ~10%
- Bonus untuk program yang “keren”: +10%

---

# Rencana Game: Flappy Bird Sederhana (Jack)

Di bawah ini proposal desain yang realistis untuk Nand2Tetris (Jack + Screen/Keyboard) — cukup kecil untuk selesai, tapi tetap “game banget”.

## Game Spec (MVP)
### Core gameplay
- **Bird** berada di x tetap (mis. `x=80`), hanya bergerak **naik/turun**.
- **Gravity** menarik bird turun setiap frame.
- **Flap**: ketika user menekan tombol (mis. SPACE), velocity bird diset ke nilai negatif (naik).
- **Pipes** bergerak dari kanan ke kiri dengan **gap** (lubang) di tengah.
- **Collision**:
  - Bird menabrak pipa (bagian atas/bawah), atau
  - Bird menyentuh ground / ceiling → game over.
- **Score** bertambah ketika bird berhasil melewati pipa.

### UI states
- **Start screen**: “Press SPACE to start”
- **Running**
- **Game Over**: tampilkan score, “Press SPACE to retry”

## Rendering Strategy (supaya performa aman)
Jack/VM emulator bukan GPU, jadi hindari redraw terlalu berat:
- Gambar bird & pipes sebagai **rectangle** (Screen.drawRectangle).
- Render frame dengan teknik:
  - (A) Clear screen setiap frame (simple, tapi bisa lebih lambat), atau
  - (B) Erase hanya area sprite lama (lebih cepat, tapi implementasi lebih ribet).

Untuk MVP: mulai dari (A) dulu, baru optimize kalau terasa lambat.

## Input
Gunakan `Keyboard.keyPressed()`:
- `0` berarti tidak ada key
- selain 0 berarti ada key (cek key code untuk SPACE/arrow sesuai emulator).  
MVP bisa: “kalau ada key pressed apa pun → flap”.

## Timing / Game loop
Gunakan loop tak berhingga + delay:
- Jika OS menyediakan `Sys.wait(n)`, gunakan untuk mengatur speed.
- Kalau tidak, buat busy-loop sederhana (kurang presisi, tapi cukup).

Target: 20–40 “ticks” per detik (tergantung emulator speed).

---

# Desain Kelas (recommended)

## Struktur folder
```text
projects/09/FlappyBird/
  Main.jack
  Game.jack
  Bird.jack
  Pipe.jack
  PipeManager.jack
  Scoreboard.jack        (opsional)
  Rand.jack              (opsional, pseudo-random)
```

## Tanggung jawab class (high-level)
### `Main`
- Entry point: `function void main()`
- Buat `Game` dan panggil `run()`

### `Game`
- State machine: START → RUNNING → GAME_OVER
- Main loop (tick):
  - baca input
  - update physics (bird + pipes)
  - cek collision
  - update score
  - render frame

### `Bird`
- Field: `x, y, vy, size`
- Method:
  - `flap()`
  - `update()` (gravity + clamp)
  - `draw()`

### `Pipe`
- Field: `x, gapY, gapH, width`
- Method:
  - `update()` (x--)
  - `draw()` (gambar top & bottom)
  - `collides(birdX, birdY, birdSize)`

### `PipeManager`
- Manage beberapa pipe sekaligus (array/list)
- Spawn pipe baru setiap beberapa tick
- Hapus pipe yang keluar layar
- Hitung score saat pipe melewati bird

### `Scoreboard` (opsional)
- Tampilkan score menggunakan `Output.printString` / `Output.printInt`.

### `Rand` (opsional)
- Pseudo-random gapY (LCG sederhana) atau sequence deterministik (lebih mudah).

---

# Milestone Plan (biar cepat jadi, minim frustrasi)

## Milestone 0 — “Hello Screen”
- Clear screen
- Gambar rectangle sebagai bird
- Print teks sederhana

## Milestone 1 — Bird physics
- Bird jatuh (gravity)
- Key press → flap (naik)
- Clamp: tidak boleh lewat ceiling / ground

## Milestone 2 — Pipes satu buah
- Spawn 1 pipe
- Pipe bergerak ke kiri, respawn di kanan setelah keluar layar
- Gap fixed dulu

## Milestone 3 — Collision + Game over
- Collision check
- Game over screen + restart

## Milestone 4 — Score + multi pipes
- Score naik saat pipe lewat
- Pipe manager: 2–3 pipe di layar

## Milestone 5 — Polish (opsional)
- Gap random / variasi
- Speed naik perlahan
- Animasi bird (2 frame) atau efek sederhana

---

## Checklist akhir (untuk “lulus” Project 9)
- [ ] Program bisa di-compile clean oleh JackCompiler
- [ ] Program bisa dijalankan di VM Emulator tanpa crash
- [ ] Ada interaksi user (keyboard) + animasi (loop) + grafik (Screen.*)
- [ ] Kode cukup rapi & ada komentar (apalagi kalau submission Coursera)

---

## Links
- Project 09 page: https://www.nand2tetris.org/project09
- PDF guideline: lihat file yang kamu upload (Project 9.pdf)
