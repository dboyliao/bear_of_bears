"""驗證背包、配裝與加權最佳分數，僅使用標準函式庫。"""

import argparse
import json
import math
from pathlib import Path
from fractions import Fraction

STATS = ("attack", "defense", "intelligence", "agility")
SLOTS = ("身體", "飾品", "頭部", "武器", "手部", "鞋子")


def load_items(path):
    items = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError(f"{path}：必須是 JSON 陣列")
    for index, item in enumerate(items, 1):
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("name"), str)
            or type(item.get("slot")) is not int
            or item["slot"] not in range(len(SLOTS))
            or any(type(item.get(key)) is not int for key in STATS)
        ):
            raise ValueError(f"{path}：第 {index} 筆裝備格式不符")
    return items


def identity(item):
    return (item["slot"], item["name"], *(item[key] for key in STATS))


def verify(inventory, selected, weights):
    if not inventory:
        raise ValueError("背包為空，沒有可用裝備")
    if not all(math.isfinite(float(weight)) for weight in weights):
        raise ValueError("權重必須是有限數值")
    records = {identity(item) for item in inventory}
    occupied = set()
    for item in selected:
        if identity(item) not in records:
            raise ValueError(f"入選裝備不在背包中：{item['name']}")
        if item["slot"] in occupied:
            raise ValueError(f"入選部位重複：{SLOTS[item['slot']]}")
        occupied.add(item["slot"])

    exact_weights = [Fraction(str(weight)) for weight in weights]

    def score(item):
        return sum(item[key] * weight for key, weight in zip(STATS, exact_weights))

    best = [Fraction(0)] * len(SLOTS)
    for item in inventory:
        best[item["slot"]] = max(best[item["slot"]], score(item))
    optimum = sum(best)
    actual = sum(score(item) for item in selected)
    if actual != optimum:
        raise ValueError(f"未達最佳分數：入選 {actual}，理論最佳 {optimum}")
    return {
        "裝備數量": len(inventory),
        "各部位數量": {
            name: sum(item["slot"] == slot for item in inventory)
            for slot, name in enumerate(SLOTS)
        },
        "屬性總值": {key: sum(item[key] for item in selected) for key in STATS},
        "加權分數": str(actual),
        "理論最佳分數": str(optimum),
        "驗證結果": "通過",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", help="背包 JSON 路徑")
    parser.add_argument("selected", help="入選裝備 JSON 路徑，格式與背包相同")
    for flag, stat in zip(("a", "d", "i", "g"), STATS):
        parser.add_argument(f"-{flag}", f"--{stat}-weight", default="1.0")
    args = parser.parse_args()
    weights = [getattr(args, f"{stat}_weight") for stat in STATS]
    try:
        result = verify(load_items(args.inventory), load_items(args.selected), weights)
    except (OSError, ValueError, OverflowError) as error:
        parser.exit(1, f"驗證失敗：{error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
