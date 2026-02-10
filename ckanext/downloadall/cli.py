# encoding: utf-8

import click

# CKAN 2.9+
from ckan.cli import load_config
import ckan.model as model
from ckan.config.middleware import make_app
from ckan.plugins.toolkit import get_action
import flask

from . import tasks

def get_commands():
    return [downloadall]

@click.group()
@click.help_option(u'-h', u'--help')
@click.pass_context
def downloadall(ctx, config=None):
    config_dict = load_config(config)
    flask_app = make_app(config_dict)._wsgi_app
    ctx.obj = {'flask_app': flask_app}

@downloadall.command(u'update-zip', short_help=u'Update zip file for a dataset')
@click.argument('dataset_ref')
@click.pass_context
def update_zip(ctx, dataset_ref):
    u''' update-zip <package-name>

    Generates zip file for a dataset, downloading its resources.'''
    flask_app = ctx.obj['flask_app']
    with flask_app.app_context():
        tasks.update_zip(dataset_ref)
    click.secho(u'update-zip: SUCCESS', fg=u'green', bold=True)


@downloadall.command(u'update-all-zips',
             short_help=u'Update zip files for all datasets')
@click.pass_context
def update_all_zips(ctx):
    u''' update-all-zips

    Generates zip file for all datasets. It is done synchronously.'''
    flask_app = ctx.obj['flask_app']
    with flask_app.app_context():
        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        datasets = get_action('package_list')(context, {})
        for i, dataset_name in enumerate(datasets):
            print('Processing dataset {}/{}'.format(i + 1, len(datasets)))
            try:
                tasks.update_zip(dataset_name)
            except Exception as e:
                print('Failed to process dataset {}: {}'.format(dataset_name, e))
    click.secho(u'update-all-zips: SUCCESS', fg=u'green', bold=True)
