import json

import click
import requests
import requests.exceptions

from .cli import bear_of_bears
from .util import parse_inventory

_TARGET_BOT = "BearOfBearsBot"
_USER_DARTA_URL = "https://lab4.kvzhuang.net/gen-art/bears-life-detail/"


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
    return _inventory(output=output, user=user)


def _inventory(output: str, user: str):
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
    equipments = parse_inventory(user_data)
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
