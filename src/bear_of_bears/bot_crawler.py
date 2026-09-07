import json
import re
import time

import click
from telethon import TelegramClient as Client
from telethon import events

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


@crawl.command(name="wait-and-fight")
@click.option("--boss", required=True, help="boss name to fight")
@click.option("--skill", required=True, help="skill name to use")
@click.pass_context
def wait_and_fight_command(ctx: click.Context, boss: str, skill: str):
    _wait_and_fight(boss=boss, skill=skill, **ctx.parent.params)


def _wait_and_fight(boss: str, skill: str, session: str, api_id: int, api_hash: str):
    client = Client(
        session,
        api_id=api_id,
        api_hash=api_hash,
    )

    RESPAWN_PATTERN = re.compile(rf"重生中：.*{boss}\s+.*(\d+)秒")

    def is_respawn_message(message: str) -> bool:
        return RESPAWN_PATTERN.search(message) is not None

    def is_home(message: str) -> bool:
        return message.startswith("🏘️ 熊熊村廣場")

    @client.on(events.NewMessage(chats=_TARGET_BOT, pattern=is_respawn_message))
    def dispatch(event: events.NewMessage.Event):
        click.echo(f"Received fight message:\n{event.message.text}")
        print("重生!")
        time.sleep(10)
        return client.send_message(_TARGET_BOT, "/look")

    @client.on(events.NewMessage(chats=_TARGET_BOT, pattern=is_home))
    def handle_home(event: events.NewMessage.Event):
        click.echo(f"Received home message:\n{event.message.text}")
        time.sleep(10)
        return client.send_message(_TARGET_BOT, "/look")

    with client:
        # trigger events
        client.send_message(_TARGET_BOT, "/look")
        client.run_until_disconnected()
