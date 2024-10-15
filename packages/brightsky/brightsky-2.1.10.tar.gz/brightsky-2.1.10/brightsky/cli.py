import json
from multiprocessing import cpu_count

import click
import dwdparse
from falcon.testing import simulate_get
from huey.consumer_options import ConsumerConfig

from brightsky import db, tasks
from brightsky.parsers import get_parser
from brightsky.utils import parse_date
from brightsky.web import app, StandaloneApplication
from brightsky.worker import huey


def dump_records(it):
    for record in it:
        print(json.dumps(record, default=str))


def migrate_callback(ctx, param, value):
    if value:
        db.migrate()


def parse_date_arg(ctx, param, value):
    if not value:
        return
    return parse_date(value)


@click.group()
@click.option(
    '--migrate', help='Migrate database before running command.',
    is_flag=True, is_eager=True, expose_value=False, callback=migrate_callback)
def cli():
    pass


@cli.command()
def migrate():
    """Apply all pending database migrations."""
    db.migrate()


@cli.command()
@click.option('--path', hidden=True)
@click.option('--url', hidden=True)
@click.option(
    '--export/--no-export',
    default=False,
    hidden=True,
)
@click.argument(
    'targets',
    required=False,
    nargs=-1,
    metavar='TARGET [TARGET ...]',
)
def parse(path, url, export, targets):
    """Parse and store observations/forecasts from a URL."""
    # TODO: In v2.2, mark `targets` as required, remove `path`, `url`, and
    #       `export`, and keep only the `elif targets` branch of this function.
    if path or url:
        if path:
            records = dwdparse.parse(path)
        elif url:
            records = dwdparse.parse_url(url)
        if export:
            exporter = get_parser(path or url).exporter()
            exporter.export(list(records))
        else:
            dump_records(records)
        click.echo(
            click.style(
                "WARNING: Parsing DWD files with `python -m brightsky parse` "
                "without exporting to a database is no longer supported and "
                "will be removed in version 2.2. Use `dwdparse` instead.",
                fg='red',
            ),
            err=True,
        )
    elif targets:
        for target in targets:
            tasks.parse(target)
    else:
        raise click.ClickException('Please provide at least one target')


@cli.command()
@click.option(
    '--enqueue/--no-enqueue', default=False,
    help='Enqueue updated files for processing by the worker')
def poll(enqueue):
    """Detect updated files on DWD Open Data Server."""
    files = tasks.poll(enqueue=enqueue)
    if not enqueue:
        dump_records(files)


@cli.command()
def clean():
    """Clean expired forecast and observations from database."""
    tasks.clean()


@cli.command()
@click.option('--workers', default=3, type=int, help='Number of threads')
def work(workers):
    """Start brightsky worker."""
    huey.flush()
    config = ConsumerConfig(worker_type='thread', workers=workers)
    config.validate()
    consumer = huey.create_consumer(**config.values)
    consumer.run()


@cli.command()
@click.option('--bind', default='127.0.0.1:5000', help='Bind address')
@click.option(
    '--reload/--no-reload', default=False,
    help='Reload server on source code changes')
def serve(bind, reload):
    """Start brightsky API webserver."""
    StandaloneApplication(
        'brightsky.web:app',
        bind=bind,
        workers=1 if reload else 2*cpu_count()+1,
        reload=reload
    ).run()


@cli.command(context_settings={'ignore_unknown_options': True})
@click.argument('endpoint')
@click.argument('parameters', nargs=-1, type=click.UNPROCESSED)
def query(endpoint, parameters):
    """Query API and print JSON response.

    Parameters must be supplied as --name value or --name=value. See
    https://brightsky.dev/docs/ for the available endpoints and arguments.

    \b
    Examples:
    python -m brightsky query weather --lat 52 --lon 7.6 --date 2018-08-13
    python -m brightsky query current_weather --lat=52 --lon=7.6
    """
    if not app._router.find(f'/{endpoint}'):
        raise click.UsageError(f"Unknown endpoint '{endpoint}'")
    resp = simulate_get(app, f'/{endpoint}', params=_parse_params(parameters))
    print(json.dumps(resp.json))


def _parse_params(parameters):
    # I'm sure there's a function in click or argparse somewhere that does this
    # but I can't find it
    usage = "Supply API parameters as --name value or --name=value"
    params = {}
    param_name = None
    for param in parameters:
        if param_name is None:
            if not param.startswith('--'):
                raise click.UsageError(usage)
            param = param[2:]
            if '=' in param:
                name, value = param.split('=', 1)
                params[name] = value
            else:
                param_name = param
        else:
            params[param_name] = param
            param_name = None
    if param_name is not None:
        raise click.UsageError(usage)
    return params
