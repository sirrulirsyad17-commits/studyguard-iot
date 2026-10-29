import json
import unittest

from shared.schemas import PayloadValidator


class ValidationTests(unittest.TestCase):
    def setUp(self): self.v = PayloadValidator(15)
    def item(self, seq=1, timestamp=100, value=-40, mode="REAL"):
        return json.dumps({"device_id": "audio", "sequence": seq, "timestamp": timestamp,
                           "noise_dbfs": value, "mode": mode})
    def test_accepts_and_rejects_duplicate(self):
        self.assertEqual(self.v.parse("audio", self.item(), now=100)["noise_dbfs"], -40)
        with self.assertRaises(ValueError): self.v.parse("audio", self.item(), now=100)
    def test_rejects_stale_invalid_range_and_bad_mode(self):
        for payload in (self.item(timestamp=1), self.item(value=2), self.item(mode="FAKE")):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                PayloadValidator().parse("audio", payload, now=100)


if __name__ == "__main__": unittest.main()
