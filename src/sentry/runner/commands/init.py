"""
sentry.runner.commands.init
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, print_function

import os
import click


@click.command()
@click.argument('directory', required=False)
@click.pass_context
def init(ctx, directory):
    "Initialize new configuration directory."
    from sentry.runner.settings import discover_configs, generate_settings
    if directory is not None:
        ctx.obj['config'] = directory

    directory, py, yaml = discover_configs(ctx)

    # In this case, the config is pointing directly to a file, so we
    # must maintain old behavior, and just abort
    if yaml is None and os.path.isfile(py):
        # TODO: Link to docs explaining about new behavior of SENTRY_CONF?
        raise click.ClickException("Found legacy '%s' file, so aborting." % click.format_filename(py))

    if yaml is None:
        raise click.ClickException("DIRECTORY must not be a file.")

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    py_contents, yaml_contents = generate_settings()

    if os.path.isfile(yaml):
        click.confirm("File already exists at '%s', overwrite?" % click.format_filename(yaml), abort=True)

    with click.open_file(yaml, 'wb') as fp:
        fp.write(yaml_contents)

    if os.path.isfile(py):
        click.confirm("File already exists at '%s', overwrite?" % click.format_filename(py), abort=True)

    with click.open_file(py, 'wb') as fp:
        fp.write(py_contents)
