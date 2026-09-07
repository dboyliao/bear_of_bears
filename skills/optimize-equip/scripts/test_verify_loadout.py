"""配裝驗證的數值比較與輸入檢查回歸測試。"""

import json
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

_module = runpy.run_path(str(Path(__file__).with_name("verify-loadout.py")))
verify = _module["verify"]
load_items = _module["load_items"]


def item(attack, name="裝備", slot=0):
    return {
        "name": name,
        "slot": slot,
        "attack": attack,
        "defense": 0,
        "intelligence": 0,
        "agility": 0,
    }


class LoadItemsTests(unittest.TestCase):
    def test_valid_items(self):
        gear = [item(1)]
        with patch.object(Path, "read_text", return_value=json.dumps(gear)):
            self.assertEqual(load_items("inventory.json"), gear)

    def test_non_array_is_rejected(self):
        for value in ({}, None, "equipment", 1, True):
            with (
                self.subTest(value=value),
                patch.object(Path, "read_text", return_value=json.dumps(value)),
                self.assertRaisesRegex(TypeError, "JSON 陣列"),
            ):
                load_items("inventory.json")

    def test_invalid_items_are_rejected(self):
        for value in (None, {}, item(True), item(1, slot=True), item(1, slot=6)):
            with (
                self.subTest(value=value),
                patch.object(Path, "read_text", return_value=json.dumps([value])),
                self.assertRaisesRegex(ValueError, "裝備格式不符"),
            ):
                load_items("inventory.json")


class VerifyTests(unittest.TestCase):
    def test_small_positive_score_rejects_empty_loadout(self):
        with self.assertRaisesRegex(ValueError, "未達最佳分數"):
            verify([item(1)], [], ["0.0000001", "0", "0", "0"])

    def test_large_score_rejects_one_point_gap(self):
        best, worse = item(1000000000), item(999999999, "較差裝備")
        with self.assertRaisesRegex(ValueError, "未達最佳分數"):
            verify([best, worse], [worse], ["1", "0", "0", "0"])

    def test_decimal_precision_is_preserved(self):
        gear = item(1)
        weight = "0.10000000000000000001"
        result = verify([gear], [gear], [weight, "0", "0", "0"])
        self.assertEqual(
            result["加權分數"], "10000000000000000001/100000000000000000000"
        )

    def test_negative_weights_allow_empty_loadout(self):
        self.assertEqual(verify([item(1)], [], ["-1", "0", "0", "0"])["加權分數"], "0")

    def test_duplicate_slot_is_rejected(self):
        gear = item(1)
        with self.assertRaisesRegex(ValueError, "部位重複"):
            verify([gear], [gear, gear], ["1"] * 4)

    def test_unknown_item_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "不在背包"):
            verify([item(1)], [item(2)], ["1"] * 4)

    def test_nonfinite_weights_are_rejected(self):
        for weight in ("nan", "inf", "-inf"):
            with (
                self.subTest(weight=weight),
                self.assertRaisesRegex(ValueError, "有限數值"),
            ):
                verify([item(1)], [], [weight, "0", "0", "0"])


if __name__ == "__main__":
    unittest.main()
