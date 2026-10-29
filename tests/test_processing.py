import unittest

from shared.processing import audio_rms, average_lux, moving_average


class ProcessingTests(unittest.TestCase):
    def test_rms_and_dbfs(self):
        rms, db = audio_rms([1000, -1000])
        self.assertEqual(rms, 1000)
        self.assertAlmostEqual(db, 20 * __import__('math').log10(1000 / 32768))

    def test_lux_average_and_invalid(self):
        self.assertEqual(average_lux([100, 300]), 200)
        with self.assertRaises(ValueError): average_lux([10, -1])

    def test_smoothing(self):
        self.assertEqual(moving_average(None, 8), 8)
        self.assertEqual(moving_average(4, 8), 6)


if __name__ == "__main__": unittest.main()
