#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:
# Description:

import typer
from rich.console import Console
from rich import print
from piprm import (
    get_registry,
    get_registrys,
    set_registry,
    get_use_registry,
    test_latency,
)

console = Console()

app = typer.Typer()


@app.command()
def ls():
    registrys = get_registrys()
    use_registry = get_use_registry()
    is_use = False
    for r in registrys:
        name = f"{r.name} "
        if use_registry and use_registry.name == r.name:
            is_use = True
        use = '*' if is_use else ' '
        print(f"{use} {name:-<20} {r.index_url}")
        is_use = False


@app.command()
def use(name: str):
    set_registry(name)
    msg = f"The registry has been changed to '{name}'."
    print(msg)


@app.command()
def test(name: str):
    r = get_registry(name)
    t = test_latency(r.index_url)
    print(f"{name} ------ {t} ms")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
