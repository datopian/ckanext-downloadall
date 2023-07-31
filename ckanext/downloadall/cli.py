# encoding: utf-8

import click

# CKAN 2.9+
from ckan.cli import load_config

from ckan.config.middleware import make_app
from ckan.plugins.toolkit import get_action
from ckan import model

from . import tasks

def get_commands():
    return [downloadall]

@click.group()
@click.help_option(u'-h', u'--help')
@click.pass_context
def downloadall(self, config=None):
    self.config = load_config(config)

@downloadall.command(u'update-zip', short_help=u'Update zip file for a dataset')
@click.argument('dataset_ref')
def update_zip(dataset_ref):
    u''' update-zip <package-name>

    Generates zip file for a dataset, downloading its resources.'''
    tasks.update_zip(dataset_ref)
    click.secho(u'update-zip: SUCCESS', fg=u'green', bold=True)


@downloadall.command(u'update-all-zips',
             short_help=u'Update zip files for all datasets')
def update_all_zips():
    u''' update-all-zips <package-name>

    Generates zip file for all datasets. It is done synchronously.'''
    context = {'model': model, 'session': model.Session}
    datasets = get_action('package_list')(context, {})
    for i, dataset_name in enumerate(datasets):
        print('Processing dataset {}/{}'.format(i + 1, len(datasets)))
        try:
            tasks.update_zip(dataset_name)
        except Exception as e:
            print('Failed to process dataset {}: {}'.format(dataset_name, e))
    click.secho(u'update-all-zips: SUCCESS', fg=u'green', bold=True)
