import asyncio
import json

import click
from telethon import TelegramClient as Client

from .cli import bear_of_bears
from .util import (
    _TARGET_BOT,
    Direction,
    get_last_reply,
    is_recall2_done,
    query_inventory,
)


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
@click.pass_context
def wait_and_fight_command(ctx: click.Context, boss: str):
    asyncio.run(_wait_and_fight(boss=boss, **ctx.parent.params))


async def _wait_and_fight(boss: str, session: str, api_id: int, api_hash: str):
    client = Client(
        session,
        api_id=api_id,
        api_hash=api_hash,
    )

    async with client:
        # trigger events
        recall2_done = False
        await client.send_message(_TARGET_BOT, "/look")
        await asyncio.sleep(3)
        reply = await get_last_reply(client)
        if reply:
            recall2_done = is_recall2_done(reply.text)

        while not recall2_done:
            await client.send_message(_TARGET_BOT, "/recall2")
            await asyncio.sleep(3)
            await client.send_message(_TARGET_BOT, "/look")
            await asyncio.sleep(3)
            reply = await get_last_reply(client)
            if reply:
                recall2_done = is_recall2_done(reply.text)
        await client.send_message(_TARGET_BOT, "/rest")
        await asyncio.sleep(3)

        path = [
            Direction.EAST,
            Direction.NORTH,
            Direction.EAST,
            Direction.EAST,
            Direction.EAST,
            Direction.SOUTH,
            Direction.SOUTH,
            Direction.EAST,
            Direction.NORTH,
            Direction.NORTH,
        ]
        for _ in range(2):
            for d in path:
                await client.send_message(_TARGET_BOT, f"/go {d}")
                await asyncio.sleep(3)
            path = [d.inverse() for d in path[::-1]]
