import unittest

from oif_model_intelligence.profile import validate_model, estimate_weight_memory_gib, assess_fit


class ModelProfileTests(unittest.TestCase):
    def setUp(self):
        self.model = {
            "id": "m1", "name": "Model", "architecture": "transformer",
            "parameter_count": 1_000_000_000, "weight_bits": 8,
            "licenses": {"weights": "unknown", "code": "unknown", "training_data": "unknown"},
        }

    def test_validates_complete_profile(self):
        self.assertEqual(validate_model(self.model), [])

    def test_requires_license_dimensions(self):
        bad = dict(self.model, licenses={"weights": "unknown"})
        self.assertTrue(any("licenses.code" in e for e in validate_model(bad)))

    def test_memory_estimate(self):
        self.assertAlmostEqual(estimate_weight_memory_gib(1_000_000_000, 8), 0.931, places=2)

    def test_fit_accounts_for_headroom(self):
        result = assess_fit(self.model, available_memory_gib=2, headroom=1.25)
        self.assertTrue(result["weight_only_fit"])
        self.assertIn("Weight-only", result["warning"])


if __name__ == "__main__":
    unittest.main()
