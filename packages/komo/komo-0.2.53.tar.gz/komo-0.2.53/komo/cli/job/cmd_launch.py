import os
import time
from typing import List, Optional, Tuple

import click

from komo import printing
from komo.cli.utils import _add_cli_envs_to_overrides, handle_errors
from komo.core import get_job, launch_job, print_job_logs
from komo.types import Cloud, JobConfig, JobStatus


@click.command("launch")
@click.option("--num-nodes", type=int, required=False, default=None)
@click.option("--gpus", type=str, default=None)
@click.option("--name", type=str, default=None)
@click.option("--cloud", "-c", type=str, default=None)
@click.option("--detach", "-d", is_flag=True)
@click.option("--run", "-r", type=str, default=None)
@click.option("--env", "-e", type=str, multiple=True, default=None)
@click.argument("config_file", type=str)
@handle_errors
def cmd_launch(
    num_nodes: Optional[int],
    gpus: Optional[str],
    name: Optional[str],
    cloud: Optional[str],
    detach: bool,
    run: List[str],
    env: Tuple[str],
    config_file: str,
):
    overrides = {}
    if num_nodes:
        overrides["num_nodes"] = num_nodes
    if gpus:
        overrides["resources/accelerators"] = gpus
    if cloud:
        overrides["resources/cloud"] = cloud
    if run:
        overrides["run"] = run
    if env:
        _add_cli_envs_to_overrides(env, overrides)

    job_config = JobConfig.from_yaml(config_file, **overrides)

    job = launch_job(
        job_config,
        name,
    )
    printing.success(f"Created job {job.name} (ID {job.id})")

    if detach:
        return

    last_message = None
    printing.info(
        f"Waiting for job {job.name} to start (this will take several minutes, you can"
        " safely Ctrl-C now)..."
    )
    while True:
        job = get_job(job.id)

        should_break = False
        error = False
        if job.status in [JobStatus.PENDING, JobStatus.INITIALIZING]:
            pass
        elif job.status in [
            JobStatus.RUNNING_SETUP,
            JobStatus.RUNNING,
            JobStatus.FINISHED,
            JobStatus.SHUTTING_DOWN,
        ]:
            should_break = True
        else:
            printing.error(f"Job status is {job.status.name}")
            should_break = True
            error = True

        if job.status_message and job.status_message != last_message:
            if error:
                printing.error(job.status_message)
            else:
                printing.info(job.status_message)

            last_message = job.status_message

        if should_break:
            break

        time.sleep(2)

    if job.status in [
        JobStatus.RUNNING_SETUP,
        JobStatus.RUNNING,
        JobStatus.FINISHED,
        JobStatus.SHUTTING_DOWN,
    ]:
        printing.success(f"Job successfully started")

        print_job_logs(job.id, 0, True)
