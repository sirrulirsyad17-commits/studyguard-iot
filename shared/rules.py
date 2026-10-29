"""Fusi sensor rule-based; tidak melakukan I/O."""
from __future__ import annotations


RECOMMENDATIONS = {
    "IDEAL": "Kondisi terpantau sesuai ambang demo. Pertahankan suasana belajar.",
    "TOO_NOISY": "Kurangi kebisingan di sekitar tempat belajar.",
    "TOO_DARK": "Tambah pencahayaan ruangan.",
    "NOT_CONDUCIVE": "Kurangi kebisingan dan tambah pencahayaan.",
    "INCOMPLETE_DATA": "Periksa koneksi dan sensor kedua perangkat.",
}


def classify(noise_dbfs: float | None, lux: float | None,
             noise_threshold_dbfs: float, light_threshold_lux: float) -> tuple[str, str]:
    if noise_dbfs is None or lux is None:
        status = "INCOMPLETE_DATA"
    else:
        noisy = noise_dbfs > noise_threshold_dbfs
        dark = lux < light_threshold_lux
        status = ("NOT_CONDUCIVE" if noisy and dark else "TOO_NOISY" if noisy
                  else "TOO_DARK" if dark else "IDEAL")
    return status, RECOMMENDATIONS[status]
