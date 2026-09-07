import click
from dotenv import load_dotenv

__all__ = ["bear_of_bears"]

load_dotenv(".env.local")


@click.group(name="bear-of-bears")
def bear_of_bears():
    pass
