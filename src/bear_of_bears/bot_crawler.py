import json

import click

from .cli import bear_of_bears
from .util import query_inventory

_TARGET_BOT = "BearOfBearsBot"


@bear_of_bears.group()
@click.option("--session", default="bot", help="session name")
@click.option(
    "--api-id",
    prompt="請輸入 API ID",
    envvar="TELEGRAM_API_ID",
    type=int,
    help="telegram MTProto API ID",
)
@click.option(
    "--api-hash",
    prompt="請輸入 API HASH",
    envvar="TELEGRAM_API_HASH",
    help="telegram MTProto API HASH",
)
def crawl(*args, **kwargs): ...


@crawl.command(name="inventory")
@click.option("--user", "-u", required=True, help="user name")
@click.option("--output", "-o", default="inventory.json", help="output file path")
def inventory_command(user: str, output: str):
    equipments = query_inventory(user=user)
    click.secho(
        f"Found {len(equipments)} equipments in inventory.", bold=True, color="white"
    )
    for equip in equipments:
        click.echo(f"- {equip}")
    click.secho(f"Saving inventory to {output}...", bold=True, color="cyan")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(
            [equip.json() for equip in equipments], f, indent=4, ensure_ascii=False
        )
    return 0
