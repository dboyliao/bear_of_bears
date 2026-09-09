import re

import click
import requests

from .data import Equipment, Slot


async def return_none():
    return


# 例：  3. 🔴👑絕世裂界王權秘環·神 ✨+3【裝備中】（ATK 310→347　...）— ...
_ITEM_PATTERN = re.compile(r"^\s*\d+\.\s*(?P<body>.+?)\s*$")

# 括號內帶箭頭的強化數值，例：ATK 310→347（取箭頭右側）
_REFINED_ITEM_PATTERN = re.compile(
    r"(?P<label>ATK|DEF|INT|AGI)\s*\d+\s*→\s*(?P<value>\d+)"
)

# 描述文字的加成，例：攻擊 +139、防禦 +86、INT +86、敏捷 +94
_DESC_RE = re.compile(
    r"(?P<label>攻擊|防禦|智力|敏捷|INT|ATK|DEF|AGI)\s*\+\s*(?P<value>\d+)"
)

# 裝備名稱中的 emoji / 符號（含稀有度、類型圖示、變體選擇符、ZWJ）
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001f000-\U0001faff"  # 各式 emoji
    "\U00002600-\U000027bf"  # 雜項符號與裝飾符號
    "\U00002b00-\U00002bff"  # 雜項符號與箭頭
    "\U0001f1e6-\U0001f1ff"  # 區域指示符
    "\U0000fe00-\U0000fe0f"  # 變體選擇符
    "\U0000200d"  # 零寬連接符（ZWJ）
    "]+"
)


def _strip_emoji(name: str) -> str:
    return _EMOJI_PATTERN.sub("", name).strip()


# 依關鍵字判斷裝備欄位，順序即優先序（越前面越優先）
_SLOT_KEYWORDS: list[tuple[Slot, tuple[str, ...]]] = [
    (Slot.HANDS, ("護手", "手甲", "臂鎧")),
    (Slot.FEET, ("靴",)),
    (Slot.HEAD, ("冠", "盔")),
    (Slot.ACCESSORY, ("環", "符", "戒", "墜")),
    (Slot.BODY, ("鎧", "甲")),
    (Slot.WEAPON, ("法典", "劍", "斧", "爪", "杖", "刃", "角", "棒", "槍", "弓")),
]

# 標籤對應到 Equipment 的欄位名稱
_LABEL2FIELD = {
    "ATK": "attack",
    "攻擊": "attack",
    "DEF": "defense",
    "防禦": "defense",
    "INT": "intelligence",
    "智力": "intelligence",
    "AGI": "agility",
    "敏捷": "agility",
}

_USER_DARTA_URL = "https://lab4.kvzhuang.net/gen-art/bears-life-detail/"


def guess_slot(name: str) -> str:
    for slot, keywords in _SLOT_KEYWORDS:
        if any(keyword in name for keyword in keywords):
            return slot.name
    return Slot.ACCESSORY.name


def parse_inventory(user_data: dict) -> list[Equipment]:
    if "inventory" not in user_data:
        return []
    equipment_list: list[Equipment] = []
    item: dict
    for item in user_data["inventory"]:
        name = item.get("name", "")
        if not name:
            continue
        stats = item.get(
            "eff_stats",
            item.get(
                "stats",
                {},
            ),
        )
        if not stats:
            continue

        stats_kwargs = {
            "attack": stats.get("atk", 0),
            "defense": stats.get("def", 0),
            "intelligence": stats.get("int", 0),
            "agility": stats.get("agi", 0),
        }
        slot = stats.get("slot", "")
        if not slot:
            slot = guess_slot(name)

        equipment_list.append(
            Equipment(
                name=name,
                slot=Slot.from_str(slot),
                **stats_kwargs,
            )
        )
    return equipment_list


def query_inventory(user: str) -> list[Equipment]:
    url = f"{_USER_DARTA_URL}?u={user}&format=json"
    response = requests.get(url)
    if response.status_code != 200:
        click.secho(
            f"Failed to fetch user data for {user}",
            fg="red",
        )
        return 1
    try:
        user_data = response.json()
    except requests.exceptions.JSONDecodeError:
        click.secho(
            f"Failed to parse user data for {user}",
            fg="red",
        )
        return 1
    return parse_inventory(user_data)
