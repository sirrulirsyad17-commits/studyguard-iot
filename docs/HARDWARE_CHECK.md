# Pemeriksaan hardware Android

Panduan ini belum dijalankan pada HP kelompok. Simpan hasil nyata di `RESULTS_TEMPLATE.md`.

## Persiapan

Gunakan dua HP Android, WiFi/hotspot yang sama dan internet. Pasang Termux serta Termux:API yang kompatibel dari sumber yang sama. Pastikan aplikasi Termux:API pendamping terpasang. Berikan izin mikrofon hanya kepada HP A ketika diminta. Jangan rekam percakapan orang lain.

## HP B: sensor cahaya

1. Buka Termux dan jalankan `termux-sensor -l`.
2. Cari sensor dengan nama/tipe ambient light/light. Catat nama persisnya.
3. Uji beberapa sampel: `termux-sensor -s "<nama-sensor-terdeteksi>" -n 5`.
4. Pastikan output sensor berubah saat sensor ditutup/dibuka atau kondisi pencahayaan berubah dan nilainya numerik/nonnegatif dalam lux.
5. Bila sensor tak ada, output kosong, atau unit tidak dapat dipastikan, catat `BLOCKED_HARDWARE`; pilih HP lain atau sepakati perubahan rancangan. Jangan pakai brightness layar sebagai lux.

## HP A: mikrofon

1. Periksa bantuan versi yang terpasang dengan `termux-microphone-record --help`.
2. Berikan izin mikrofon. Buat klip uji singkat di tempat aman dan tenang. Tentukan opsi durasi, codec, sample rate, kanal, dan format berdasarkan bantuan aktual; jangan menganggap format WAV/PCM tersedia.
3. Periksa file dan metadata menggunakan utilitas yang tersedia. Jika file WAV PCM, verifikasi dapat dibuka sebagai PCM 16-bit oleh Python `wave`; hitung RMS dari sampel, bukan mengirim file audio.
4. Bandingkan level relatif dalam suasana tenang dan bunyi tepuk singkat. Hapus file uji segera setelah diproses.
5. Bila format tidak dapat didekode atau API tidak mendukung rekaman singkat, jangan mengaktifkan edge nyata. Pertimbangkan aplikasi Android kecil menggunakan `AudioRecord` dan mikrofon fisik untuk menghasilkan PCM lokal, RMS/dBFS, lalu menghapus buffer.

Kode StudyGuard hanya menerima WAV PCM 16-bit untuk adapter Termux. Ketidakcocokan ditampilkan sebagai error yang jelas, bukan diganti simulasi. dBFS adalah level digital relatif dan bukan dB SPL terkalibrasi.

## Menjalankan edge nyata

Di setiap HP, buka folder proyek yang dapat diakses Termux (`termux-setup-storage` bila diperlukan), instal Python dan dependensi MQTT di Termux, salin `.env` dengan PROJECT_ID sama, lalu jalankan `python edge/audio_edge.py` pada HP A atau `python edge/light_edge.py` pada HP B. Isi `LIGHT_SENSOR_NAME` dengan nama terdeteksi. Atur broker dan ambang berdasarkan uji kelompok. Jangan jalankan edge yang sensornya belum lolos pemeriksaan.
