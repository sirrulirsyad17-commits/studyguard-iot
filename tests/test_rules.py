import unittest

from shared.rules import classify


class RuleTests(unittest.TestCase):
    def test_scenarios(self):
        cases = [(-45, 400, "IDEAL"), (-20, 400, "TOO_NOISY"),
                 (-45, 100, "TOO_DARK"), (-20, 100, "NOT_CONDUCIVE"),
                 (None, 100, "INCOMPLETE_DATA"), (-45, None, "INCOMPLETE_DATA")]
        for noise, lux, expected in cases:
            with self.subTest(noise=noise, lux=lux):
                self.assertEqual(classify(noise, lux, -35, 300)[0], expected)


if __name__ == "__main__": unittest.main()
