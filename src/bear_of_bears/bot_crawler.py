import json

import click
from telethon.sync import TelegramClient as Client
from telethon.sync import events

from .cli import bear_of_bears
from .util import parse_inventory_message, return_none

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
@click.option("--output", "-o", default="inventory.json", help="output file path")
@click.pass_context
def inventory_command(ctx: click.Context, output: str):
    if ctx.parent is None:
        raise click.UsageError("inventory must be invoked under crawl")
    _inventory(output=output, **ctx.parent.params)


def _inventory(output: str, session: str, api_id: int, api_hash: str):
    client = Client(
        session,
        api_id=api_id,
        api_hash=api_hash,
    )

    @client.on(events.NewMessage(chats=_TARGET_BOT, pattern=r"^🎒 背包.*"))
    def inventory_handler(event: events.NewMessage.Event):
        equipments = parse_inventory_message(event.message.text)
        click.echo(f"Found {len(equipments)} equipments in inventory.")
        for equip in equipments:
            click.echo(f"  - {equip!s}")
        click.echo(f"Saving inventory to {output}...")
        with open(output, "w", encoding="utf-8") as f:
            json.dump(
                [equip.json() for equip in equipments], f, indent=4, ensure_ascii=False
            )
        client.disconnect()
        return return_none()

    with client:
        # telethon.sync runs this call synchronously when the loop is stopped.
        _ = client.send_message(_TARGET_BOT, "/inventory")
        client.run_until_disconnected()
