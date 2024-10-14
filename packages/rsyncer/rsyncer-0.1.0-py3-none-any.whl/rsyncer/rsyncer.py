import click
from shutil import which
from pathlib import Path
import tomllib
import subprocess
from datetime import datetime
from time import sleep
import importlib.metadata

#  ──────────────────────────────────────────────────────────────────────────
# global variables

rsyncer_version = importlib.metadata.version('rsyncer')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

#  ──────────────────────────────────────────────────────────────────────────
# base command

# done for the config
@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(rsyncer_version)
@click.option('-c', '--config', default='~/.config/rsyncer.toml', type=str, help="Config file path", show_default=True)
@click.pass_context
def rsyncer(ctx, config):
    """Simple and quick backup program."""

    # check if rsync and ssh are available
    if which('rsync') and which('ssh'):
        pass
    else:
        raise click.ClickException('rsync and ssh not found')

    # setting up config
    ctx.ensure_object(dict)

    config = Path(config).expanduser()
    if config.exists():

        with open(config, 'rb') as file:
            toml = tomllib.load(file)

        # required config options
        required = ['sources', 'destinations']
        for option in required:
            if option not in toml:
                raise click.ClickException('Config requires "' + key + '" to be set.')

        # setting config
        ctx.obj = toml

    else:
        raise click.ClickException('No config file, exiting.')

#  ──────────────────────────────────────────────────────────────────────────
# run command

@rsyncer.command('run', short_help="Run rsyncer.")
@click.pass_obj
def run(obj):
    """Run"""

    def _log(config, content):
        with open(Path(config['log']['path']).expanduser(), 'a') as file:
            file.write(content + '\n')


    def _run_freq(config, source, destination, frequency):
        # cmd = ['echo', source, destination + '/' + frequency]
        cmd = ['rsync', '--progress', '-r', source, destination + '/' + frequency]
        subprocess.run(cmd)


    def _run(config, frequency):

        for source in config['sources']:
            for path in config['sources'][source]['paths']: # for each source's path
                for destination in config['destinations']: # for each destination

                    if source in ['local']:
                        _run_freq( config, Path(path).expanduser(), destination + ':' + config['destinations'][destination]['path'] , frequency )
                    else:
                        _run_freq( config, source + ':' + str(Path(path).expanduser()), destination + ':' + config['destinations'][destination]['path'], frequency )


    # run time loop
    old_time = datetime.now()
    while True:
        current_time = datetime.now()

        for frequency in obj['frequency']['frequencies']:

            if current_time > old_time:

                if frequency == 'daily':
                    if current_time.day > old_time.day:
                        _run(obj, frequency)
                        _log(obj, current_time.isoformat() + ' ' + frequency)

                elif frequency == 'weekly':
                    if current_time.weekday() == 6: 
                        _run(obj, frequency)
                        _log(obj, current_time.isoformat() + ' ' + frequency)

                elif frequency == 'monthly':
                    if current_time.day == 1: 
                        _run(obj, frequency)
                        _log(obj, current_time.isoformat() + ' ' + frequency)

        old_time = current_time
        sleep(3*3600) # waits for 3 hours
