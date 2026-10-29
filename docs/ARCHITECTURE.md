# Arsitektur

HP A merekam jendela pendek dari mikrofon, memvalidasi PCM 16-bit mono, menghitung RMS dan dBFS, menghapus file sementara, lalu menerbitkan agregat. HP B meminta beberapa sampel sensor ambient-light dengan nama yang telah diverifikasi, menghitung rata-rata dan exponential moving average, lalu menerbitkan lux. Keduanya mengirim JSON berisi device_id, sequence, timestamp Unix, nilai dan mode.

Laptop menerima topic `studyguard/<PROJECT_ID>/edge/audio/telemetry` dan `.../edge/light/telemetry`. Validator menolak format, nilai, umur, mode, dan sequence yang tidak valid. Detector mengecek stale/disconnected, menggabungkan data hanya bila kedua edge segar dan mode konsisten, kemudian mencetak serta menerbitkan status pada `studyguard/<PROJECT_ID>/status`.

Processing tidak bercampur dengan keputusan: `shared.processing` berisi fungsi numerik murni, `shared.rules` berisi klasifikasi murni, dan `shared.schemas` memvalidasi protokol. Dashboard lokal membaca state detector melalui HTTP; ia opsional dan tidak mengganti detector.

Jendela audio 1 detik mengurangi jeda dan durasi penyimpanan tetapi dapat melewatkan bunyi sangat singkat; sampling berulang dengan interval konfigurasi menambah beban dan latensi pengamatan. Nilai dBFS hanya untuk perbandingan relatif perangkat/ruangan, bukan SPL. Smoothing lux meredam fluktuasi namun menambah respons lambat.

Mode awal edge hanya REAL. Simulator merupakan command terpisah yang memberi label SIMULATION pada kedua payload. Broker publik dipakai untuk demo sementara; PROJECT_ID unik mengurangi tabrakan nama, tetapi tidak memberi autentikasi atau privasi.
