# Kerangka PPT

1. Masalah belajar dan ide StudyGuard; pastikan nama/topik disetujui kelompok dan cek keunikan.
2. Tujuan, pengguna, dan batasan sistem.
3. Arsitektur dua edge HP, cloud MQTT, laptop detector.
4. Sensor dan hasil feasibility per HP; tampilkan hanya data yang benar-benar diamati.
5. Processing HP A: PCM → RMS → dBFS relatif; batasan bukan dB SPL.
6. Processing HP B: sampel ambient lux → rata-rata → smoothing.
7. Algoritma keputusan threshold fusion; tunjukkan konfigurasi ambang dan tabel status.
8. MQTT: topic, payload, QoS, freshness, sequence dan keamanan broker publik.
9. Pengujian: unit test sintetis terpisah dari tes HP dan jaringan nyata.
10. Hasil observasi nyata, keterbatasan, kesimpulan dan pengembangan lanjut.
