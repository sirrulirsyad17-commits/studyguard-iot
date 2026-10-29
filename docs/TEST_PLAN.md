# Rencana pengujian

## Unit otomatis

Jalankan `python -m unittest discover -s tests -v`. Tes memakai data sintetis dan hanya membuktikan processing, rules, serta validasi lokal. Catat hasil aktual; belum dijalankan pada saat dokumen ini dibuat.

| Skenario | Input/aksi | Hasil yang diharapkan |
|---|---|---|
| Tenang + cukup cahaya | di bawah ambang noise, di atas ambang lux | IDEAL |
| Bising + cukup cahaya | di atas ambang noise | TOO_NOISY |
| Tenang + gelap | di bawah ambang lux | TOO_DARK |
| Bising + gelap | kedua kondisi melewati ambang | NOT_CONDUCIVE |
| Edge offline | hentikan salah satu edge lebih dari freshness | INCOMPLETE_DATA |
| Stale | publish timestamp lebih lama dari batas | ditolak/INCOMPLETE_DATA |
| Duplicate/out-of-order | kirim sequence sama atau lebih kecil | payload ditolak |
| Invalid | nilai negatif, bukan numerik, rentang audio salah, JSON rusak | payload ditolak |
| MQTT reconnect | putuskan lalu pulihkan jaringan/broker | koneksi pulih; sistem kembali menerima telemetri |
| Dashboard LAN | buka alamat IP LAN laptop dari perangkat lain | UI/status tampil; harus diuji manual |

## Uji perangkat nyata (belum dilakukan)

Ikuti `HARDWARE_CHECK.md`. Catat model HP/versi Android, nama dan output sensor, izin, format/codec/sample rate audio, rentang relatif tenang/berisik, latensi, stabilitas MQTT, serta kondisi jaringan. Jangan masukkan percakapan atau data pribadi ke bukti/laporan.
