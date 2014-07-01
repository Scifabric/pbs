#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.


import click
import pbclient
import json
import logging
from requests import exceptions

class Config(object):

    def __init__(self):
        self.verbose = False
        self.server = None
        self.api_key = None
        self.pbclient = pbclient

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--server',  help='The PyBossa server', default='http://localhost:5000')
@click.option('--api-key', help='Your PyBossa API-KEY', default=None)
@click.option('--project', type=click.File('r'), default='project.json')
@pass_config
def cli(config, verbose, server, api_key, project):
    config.verbose = verbose
    config.server = server
    config.api_key = api_key
    config.project = json.loads(project.read())
    config.pbclient = pbclient
    config.pbclient.set('endpoint', config.server)
    config.pbclient.set('api_key', config.api_key)


@cli.command()
@pass_config
def create_project(config):
    """Create the PyBossa project."""
    try:
        response = pbclient.create_app(config.project['name'],
                                       config.project['short_name'],
                                       config.project['description'])
        check_api_error(response)
    except exceptions.ConnectionError:
        click.echo("Connection Error! The server %s is not responding" % config.server)
    except:
        format_error("pbclient.create_app", response)


@cli.command()
@click.option('--task-presenter', help='The project task presenter file',
              type=click.File('r'), default='template.html')
@click.option('--long-description', help='The project long description file (Markdown)',
              type=click.File('r'), default='long_description.md')
@click.option('--tutorial', help='The project tutorial file',
              type=click.File('r'), default='tutorial.html')
@pass_config
def update_project(config, task_presenter, long_description, tutorial):
    """Update project templates and information."""
    try:
        # Get project
        project = find_app_by_short_name(config.project['short_name'])
        # Update attributes
        project.name = config.project['name']
        project.short_name = config.project['short_name']
        project.description = config.project['description']
        project.long_description = long_description.read()
        # Update task presenter
        project.info['task_presenter'] = task_presenter.read()
        # Update tutorial
        project.info['tutorial'] = tutorial.read()
        response = config.pbclient.update_app(project)
        check_api_error(response)
    except exceptions.ConnectionError:
        click.echo("Connection Error! The server %s is not responding" % config.server)
    except:
        raise
        format_error("pbclient.update_app", response)


@cli.command()
@click.option('--tasks-file', help='File with tasks',
               default='project.tasks', type=click.File('r'))
@click.option('--tasks-type', help='Tasks type: JSON|CSV',
               default='json', type=click.Choice(['json', 'csv']))
@click.option('--priority', help="Priority for the tasks.", default=0)
@click.option('--redundancy', help="Redundancy for tasks.", default=30)
@pass_config
def add_tasks(config, tasks_file, tasks_type, priority, redundancy):
    """Add tasks to a project."""
    try:
        project = find_app_by_short_name(config.project['short_name'])
        tasks = tasks_file.read()
        if tasks_type == 'json':
            data = json.loads(tasks)
            for d in data:
                if d.get('info'):
                    task_info = d['info']
                    response = config.pbclient.create_task(app_id=project.id,
                                                           info=task_info,
                                                           n_answers=redundancy,
                                                           priority_0=priority)
        #else:
        #    data = StringIO.StringIO(tasks)
        #    reader = csv.reader(data, delimiter=',')
        #    for row in reader:
        #        task_info = dict(

    except exceptions.ConnectionError:
        click.echo("Connection Error! The server %s is not responding" % config.server)
    except:
        raise
        format_error("pbclient.create_task", response)


@cli.command()
@click.option('--task-id', help='Task ID to delete from project', default=None)
@pass_config
def delete_tasks(config, task_id):
    """Add tasks to a project."""
    try:
        project = find_app_by_short_name(config.project['short_name'])
        if task_id:
            response = config.pbclient.delete_task(task_id)
            check_api_error(response)
        else:
            limit = 100
            offset = 0
            tasks = config.pbclient.get_tasks(project.id, limit, offset)
            while len(tasks) > 0:
                for t in tasks:
                    config.pbclient.delete_task(t.id)
                offset += limit
                tasks = config.pbclient.get_tasks(project.id, limit, offset)

    except exceptions.ConnectionError:
        click.echo("Connection Error! The server %s is not responding" % config.server)
    except:
        format_error("pbclient.delete_task", response)


def find_app_by_short_name(short_name):
    try:
        response = pbclient.find_app(short_name=short_name)
        check_api_error(response)
        return response[0]
    except exceptions.ConnectionError:
        raise
    except:
        format_error("pbclient.find_app", response)


def check_api_error(api_response):
    """Check if returned API response contains an error"""
    if type(api_response) == dict and (api_response.get('status') == 'failed'):
        raise exceptions.HTTPError

def format_error(module, error):
    """Format the error for the given module"""
    logging.error(module)
    # Beautify JSON error
    if type(error) == list:
        print "Application not found"
    else:
        print json.dumps(error, sort_keys=True, indent=4, separators=(',', ': '))
    exit(1)
