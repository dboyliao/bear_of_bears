import re

from .data import Equipment, Slot


async def return_none():
    return


# 例：  3. 🔴👑絕世裂界王權秘環·神 ✨+3【裝備中】（ATK 310→347　...）— ...
_ITEM_PATTERN = re.compile(r"^\s*\d+\.\s*(?P<body>.+?)\s*$")

# 括號內帶箭頭的強化數值，例：ATK 310→347（取箭頭右側）
_REFINED_ITEM_PATTERN = re.compile(r"(?P<label>ATK|DEF|INT)\s*\d+\s*→\s*(?P<value>\d+)")

# 描述文字的加成，例：攻擊 +139、防禦 +86、INT +86
_DESC_RE = re.compile(r"(?P<label>攻擊|防禦|智力|INT|ATK|DEF)\s*\+\s*(?P<value>\d+)")

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
    (Slot.HAND, ("護手",)),
    (Slot.SHOES, ("靴",)),
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
}


def guess_slot(name: str) -> Slot:
    for slot, keywords in _SLOT_KEYWORDS:
        if any(keyword in name for keyword in keywords):
            return slot
    return Slot.ACCESSORY


def parse_inventory_message(message: str) -> list[Equipment]:
    equipment_list: list[Equipment] = []
    for line in message.splitlines():
        matched = _ITEM_PATTERN.match(line)
        if matched is None:
            continue
        body = matched.group("body")

        # 名稱：取到第一個空白為止，並去除稀有度/類型 emoji
        name = _strip_emoji(body.split(maxsplit=1)[0])

        stats = {"attack": 0, "defense": 0, "intelligence": 0}

        # 出現 ✨+N 等強化字樣時，最終數值以括號內箭頭右側為準；
        # 括號內帶箭頭的數值只在強化裝上出現，故優先採用。
        arrow_matches = list(_REFINED_ITEM_PATTERN.finditer(body))
        if arrow_matches:
            for m in arrow_matches:
                stats[_LABEL2FIELD[m.group("label")]] = int(m.group("value"))
        else:
            for m in _DESC_RE.finditer(body):
                stats[_LABEL2FIELD[m.group("label")]] = int(m.group("value"))

        # 跳過任何沒有跟 ATK / DEF / INT 相關的項目
        if not any(stats.values()):
            continue

        equipment_list.append(
            Equipment(
                name=name,
                # TODO: use /inspect to get slot info
                slot=guess_slot(name),
                **stats,
            )
        )
    return equipment_list
