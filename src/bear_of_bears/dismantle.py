import re
from io import StringIO

import click

from .cli import bear_of_bears

# <emoji>(中文名稱)[ ×N] → 　→ group(1) 為中文名稱
line_pattern = re.compile(
    r'[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]+([\u4e00-\u9fff]+)\s*(?:×(\d+)\s*)?→'
)

def _equipments_to_list(equipments_str: str) -> list[str]:
    equipments = []
    for line in StringIO(equipments_str).readlines():
        match = line_pattern.search(line)
        if match:
            equipment = match.group(1)
            num = match.group(2)
            num = 1 if num is None else int(num)
            for _ in range(num):
                equipments.append(equipment)
    return equipments

@bear_of_bears.command()
@click.option("--equipments", "-e", type=_equipments_to_list, required=True, help="輸入裝備清單，每行一件裝備")
@click.option("--prefix", "-p", default="不朽")
def dismantle(equipments: str, prefix: str = "不朽"):
    for equipment in equipments:
        if equipment.startswith(prefix):
            click.echo(f"/dismantle {equipment}")
