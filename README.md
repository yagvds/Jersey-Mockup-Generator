# Sports Jersey Prompt Generator

Aplikasi Python sederhana berbasis Streamlit untuk membuat prompt mockup dan photoshoot jersey olahraga yang realistis, natural, dan profesional.

Aplikasi ini tidak membuat gambar langsung. Hasil prompt bisa Anda copy atau download sebagai file TXT, lalu digunakan di ChatGPT atau image generator bersama gambar desain jersey yang Anda upload.

Dropdown aplikasi dibuat dalam bahasa Indonesia agar mudah dipahami. Prompt akhir tetap otomatis disusun dalam bahasa Inggris karena biasanya lebih cocok untuk image generator.

## Isi Project

```text
sports_jersey_prompt_generator/
|-- app.py
|-- requirements.txt
`-- README.md
```

## Fitur

- Preset untuk jenis model, jumlah model, pose, ekspresi, komposisi, background sport, lighting, camera angle, lens look, outfit, mood, dan tipe output.
- Pilihan jenis olahraga, seperti sepak bola, futsal, running, badminton, padel, basket, voli, tenis, gym, dan lainnya.
- Pilihan jenis hasil foto: jersey dipakai atlet, detail produk jersey, jersey digantung, jersey di kursi stadion, locker room, close-up logo, tampak belakang nama nomor, flat lay, dan katalog produk.
- Tema detail produk untuk kebutuhan presentasi klien, preview sebelum produksi, katalog, dan konten promosi.
- Data preset lebih banyak agar hasil random tidak monoton.
- Minimal 30+ model, 50+ pose, 30+ background, 20+ lighting, 20+ camera angle, 20+ mood, 20+ outfit, dan 15+ komposisi.
- Tombol Generate Prompt.
- Tombol Generate Random Prompt.
- Tombol Copy/Download Prompt TXT.
- Negative prompt otomatis.
- Instruksi khusus agar desain jersey dari gambar referensi tidak berubah.

## 1. Install Python di Windows

1. Buka website resmi Python: https://www.python.org/downloads/
2. Download Python versi terbaru untuk Windows.
3. Jalankan installer.
4. Centang pilihan **Add python.exe to PATH**.
5. Klik **Install Now**.
6. Setelah selesai, buka CMD atau PowerShell lalu cek:

```bash
python --version
```

Jika muncul versi Python, berarti instalasi berhasil.

## 2. Masuk ke Folder Project

Buka CMD atau PowerShell, lalu masuk ke folder project ini.

Contoh:

```bash
cd sports_jersey_prompt_generator
```

Jika folder berada di lokasi lain, sesuaikan path-nya.

## 3. Membuat Virtual Environment

Virtual environment berguna agar library project tidak bercampur dengan project lain.

Jalankan:

```bash
python -m venv venv
```

Setelah berhasil, akan muncul folder baru bernama `venv`.

## 4. Activate Virtual Environment

### Jika memakai CMD

```bash
venv\Scripts\activate
```

### Jika memakai PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

Jika aktif, biasanya akan muncul tanda seperti ini di awal baris terminal:

```text
(venv)
```

## 5. Install Requirements

Pastikan virtual environment sudah aktif, lalu jalankan:

```bash
pip install -r requirements.txt
```

Tunggu sampai proses install selesai.

## 6. Menjalankan Aplikasi Streamlit

Jalankan:

```bash
streamlit run app.py
```

Biasanya browser akan terbuka otomatis.

Jika tidak terbuka, lihat alamat yang muncul di terminal, biasanya:

```text
http://localhost:8501
```

Buka alamat tersebut di browser.

## 7. Cara Menggunakan Aplikasi

1. Pilih preset photoshoot yang Anda inginkan.
2. Isi catatan tambahan jika perlu.
3. Klik **Generate Prompt** untuk membuat prompt dari pilihan Anda.
4. Klik **Generate Random Prompt** jika ingin kombinasi acak.
5. Copy prompt dari kotak hasil, atau klik **Copy/Download Prompt TXT** untuk mengunduh file `.txt`.
6. Upload gambar desain jersey Anda ke ChatGPT atau image generator.
7. Tempel prompt yang sudah dibuat.

## 8. Mematikan Aplikasi

Klik terminal tempat Streamlit berjalan, lalu tekan:

```text
Ctrl + C
```

Jika diminta konfirmasi, tekan `Y` lalu Enter.

## Error Umum dan Solusinya

### `python` tidak dikenali

Penyebab:
Python belum terinstall atau belum masuk PATH.

Solusi:
- Install ulang Python.
- Pastikan mencentang **Add python.exe to PATH** saat install.
- Tutup dan buka ulang CMD atau PowerShell.

### PowerShell tidak bisa activate venv

Pesan error biasanya berhubungan dengan execution policy.

Solusi cepat:
Gunakan CMD, lalu jalankan:

```bash
venv\Scripts\activate
```

Atau jika tetap ingin memakai PowerShell, jalankan PowerShell sebagai user biasa lalu ketik:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Setelah itu coba lagi:

```powershell
.\venv\Scripts\Activate.ps1
```

### `streamlit` tidak dikenali

Penyebab:
Virtual environment belum aktif atau requirements belum diinstall.

Solusi:

```bash
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Untuk PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

### Port 8501 sudah dipakai

Penyebab:
Ada aplikasi Streamlit lain yang masih berjalan.

Solusi:
- Matikan terminal Streamlit lama dengan `Ctrl + C`.
- Atau jalankan di port lain:

```bash
streamlit run app.py --server.port 8502
```

### Browser tidak terbuka otomatis

Solusi:
Copy alamat yang muncul di terminal, lalu buka manual di browser.

Contoh:

```text
http://localhost:8501
```

## Cara Edit Preset

Buka file `app.py`, lalu cari bagian:

```python
PRESETS = {
    ...
}
```

Anda bisa menambah, mengurangi, atau mengubah pilihan preset di sana.

Contoh menambah background:

```python
"beach football campaign",
```

Simpan file, lalu refresh browser Streamlit.
