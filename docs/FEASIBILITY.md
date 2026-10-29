# Audit kelayakan StudyGuard

Tanggal audit: 23 Oktober 2026. Audit dilakukan dari laptop Windows yang menjalankan workspace ini.

## Hasil audit lingkungan

| Pemeriksaan | Hasil |
|---|---|
| Sistem operasi | Windows (workspace PowerShell) |
| Python | Python 3.13.5 tersedia; memenuhi syarat Python 3.10+ |
| Android/ADB | `adb` tidak tersedia di PATH; tidak ada perangkat Android terhubung yang dapat diuji |
| Termux API | `termux-sensor` dan `termux-microphone-record` tidak tersedia di laptop Windows; kemampuan di HP belum diverifikasi |
| Proyek/folder yang sudah ada | Ada beberapa proyek IoT. Semuanya dipertahankan; StudyGuard ditempatkan di folder terpisah `studyguard/` |
| MQTT/internet | Belum diuji dari edge Android atau terhadap broker cloud |

## Status sensor dan batasan

**BLOCKED_HARDWARE (belum diverifikasi):** sensor ambient light pada HP B belum diketahui. Jangan memakai brightness layar sebagai pengganti lux lingkungan. Di HP B, pasang Termux dan Termux:API yang kompatibel dari sumber yang sama, lalu jalankan `termux-sensor -l`. Pilih nama sensor cahaya yang benar-benar terdaftar dan uji pembacaan melalui `termux-sensor -s "<nama-sensor-terdeteksi>" -n 5`. Nama dan format keluaran berbeda antarperangkat/API; adapter hanya boleh mengirim nilai numerik nonnegatif yang berhasil dipetakan ke lux. Jika tidak ada sensor cahaya atau tidak dapat dibaca, gunakan HP B lain atau minta persetujuan kelompok untuk mengubah rancangan sensor.

Kemampuan dan format `termux-microphone-record` juga **belum diverifikasi pada HP nyata**. Perintah Termux API umumnya merekam klip ke file, tetapi pilihan format, izin, dan akses rekaman bergantung pada versi aplikasi/API dan Android. Sebelum implementasi nyata: lihat `termux-microphone-record --help`, rekam sampel pendek WAV/PCM bila didukung, periksa format aktual dengan `file`/metadata, pastikan PCM dapat di-decode, hitung RMS, lalu hapus berkas sementara. Hindari perekaman kontinu dan jangan menyimpan/mengirim audio percakapan.

Jika API hanya menghasilkan format yang tidak praktis didekode pada Termux, jalur alternatif yang tetap menggunakan **mikrofon fisik** adalah aplikasi Android kecil (Kotlin/Java) dengan `AudioRecord` mono PCM 16-bit pada sample rate yang didukung perangkat. Ambil jendela singkat (sekitar 1 detik), hitung RMS dan dBFS lokal, buang buffer segera, lalu kirim hanya agregat melalui MQTT. Ini memerlukan pembangunan/pemasangan aplikasi dan izin mikrofon; belum dilakukan atau diuji.

## Prasyarat dan pekerjaan yang menunggu perangkat

- Dua HP Android: HP A dengan mikrofon; HP B dengan ambient light sensor yang dapat diakses.
- Termux dan Termux:API dari sumber yang kompatibel, izin mikrofon untuk HP A serta akses sensor untuk HP B.
- Laptop dengan Python 3.10+, WiFi/hotspot bersama, serta internet.
- Uji sensor nyata, format audio, izin, MQTT dari ponsel, latensi, dan dashboard LAN harus dilakukan manual. Tidak ada hasil uji perangkat nyata dalam audit ini.

Mode SIMULATION boleh dipakai untuk menguji logika lokal, tetapi setiap payload/keluaran simulasi harus mempertahankan label `SIMULATION`. Data simulasi bukan bukti hardware.
