import logging
import os
from typing import List, Optional

import click

from gfw_pixetl import get_module_logger, utils
from gfw_pixetl.grids import Grid, grid_factory
from gfw_pixetl.layers import Layer, layer_factory
from gfw_pixetl.logo import logo
from gfw_pixetl.pipes import Pipe, pipe_factory

logger = get_module_logger(__name__)


@click.command()
@click.argument("name", type=str)
@click.option("-v", "--version", type=str, help="Version of dataset")
@click.option(
    "-s",
    "--source_type",
    type=click.Choice(["raster", "vector", "tcd_raster"]),
    help="Type of input file(s)",
)
@click.option("-f", "--field", type=str, help="Field represented in output dataset")
@click.option(
    "-g",
    "--grid_name",
    type=click.Choice(["10/40000", "90/27008"]),
    default="10/40000",
    help="Grid size of output dataset",
)
@click.option(
    "--subset", type=str, default=None, multiple=True, help="Subset of tiles to process"
)
@click.option(
    "-e",
    "--env",
    type=click.Choice(["test", "dev", "staging", "production"]),
    default="dev",
    help="Environment",
)
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite existing tile in output location",
)
@click.option("-d", "--debug", is_flag=True, default=False, help="Log debug messages")
@click.option("-w", "--cwd", default="/tmp", help="Work directory")
def cli(
    name: str,
    version: str,
    source_type: str,
    field: str,
    grid_name: str,
    subset: Optional[List[str]],
    env: str,
    overwrite: bool,
    debug: bool,
    cwd: str,
) -> None:
    """NAME: Name of dataset"""

    if debug:
        logger.setLevel(logging.DEBUG)

    click.echo(logo)

    logger.info(
        "Start tile prepartion for Layer {name}, Version {version}, grid {grid_name}, source type {source_type}, field {field} with overwrite set to {overwrite}.".format(
            name=name,
            version=version,
            grid_name=grid_name,
            source_type=source_type,
            field=field,
            overwrite=overwrite,
        )
    )

    # Set current work directory to /tmp. This is important when running as AWS Batch job
    # When using the ephemeral-storage launch template /tmp will be the mounting point for the external storage
    # In AWS batch we will then mount host's /tmp directory as docker volume /tmp
    os.chdir(cwd)

    os.environ["ENV"] = env

    if subset:
        logger.info("Running on subset: {}".format(subset))
    else:
        logger.info("Running on full extent")

    utils.verify_version_pattern(version)

    grid: Grid = grid_factory(grid_name)
    layer: Layer = layer_factory(name=name, version=version, grid=grid, field=field)
    pipe: Pipe = pipe_factory(layer, subset)

    pipe.create_tiles(overwrite)


if __name__ == "__main__":
    cli()
