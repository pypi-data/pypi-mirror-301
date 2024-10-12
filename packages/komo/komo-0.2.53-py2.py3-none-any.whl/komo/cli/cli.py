import os

import click
import sentry_sdk
from sentry_sdk import set_user

from komo import printing
from komo.api_client import APIClient
from komo.cli.agent.agent import agent
from komo.cli.aws.aws import aws
from komo.cli.cmd_login import cmd_login
from komo.cli.cmd_update import cmd_update
from komo.cli.job.job import job
from komo.cli.lambda_labs.lambda_labs import lambda_labs
from komo.cli.machine.machine import machine
from komo.cli.service.service import service
from komo.cli.utils import prompt_update
from komo.version import __version__

sentry_sdk.init(
    dsn="https://9ad4d8eed531ed220436cd5753f7bc76@o4507336556412928.ingest.us.sentry.io/4507708558999552",
    sample_rate=1.0,
    environment="production",
    enable_tracing=False,
    release=__version__,
)


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)
    # Skip update prompt if the command is 'update'
    if ctx.invoked_subcommand != "update":
        try:
            prompt_update()
        except click.exceptions.Abort:
            printing.info("\nUpdate skipped.")


cli.add_command(cmd_login)
cli.add_command(aws)
cli.add_command(lambda_labs)
cli.add_command(machine)
cli.add_command(job)
cli.add_command(service)
cli.add_command(cmd_update)

# agent is not to be used by the user, but only but running komodo workflows
if os.environ.get("__KOMODO_INTERNAL_AGENT__", None):
    cli.add_command(agent)
