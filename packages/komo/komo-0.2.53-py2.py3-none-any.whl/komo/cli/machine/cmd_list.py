import os
from typing import List, Optional

import click
import textwrap3
from tabulate import tabulate

from komo import printing
from komo.cli.utils import handle_errors
from komo.core import list_machines


@click.command("list")
@handle_errors
def cmd_list():
    machines = list_machines()
    machines_to_print = [
        [
            machine.name,
            machine.status.value,
            machine.notebook_token is not None,
            machine.cloud.value if machine.cloud else None,
            machine.accelerators,
            textwrap3.fill(
                machine.status_message,
                width=50,
                replace_whitespace=False,
                drop_whitespace=False,
            ),
        ]
        for machine in machines
    ]

    printing.header(f"Found {len(machines)} Komodo machines\n", bold=True)
    printing.info(
        tabulate(
            machines_to_print,
            headers=[
                "Name",
                "Status",
                "Notebook",
                "Cloud",
                "Accelerators",
                "Message",
            ],
            tablefmt="simple_grid",
        ),
    )
