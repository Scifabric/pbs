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
"""
A very simple PyBossa command line client.

This module is a pybossa-client that runs the following commands:

    * create_project: to create a PyBossa proejct
    * add_tasks: to add tasks to an existing project
    * delete_tasks: to delete all tasks and task_runs from an existing project

"""

import click
import pbclient
import json
import StringIO
import csv
import ConfigParser
import os.path
from os.path import expanduser
from helpers import *
from requests import exceptions


class Config(object):

    """Config class for the command line."""

    def __init__(self):
        """Init the configuration default values."""
        self.verbose = False
        self.server = None
        self.api_key = None
        self.project = None
        self.pbclient = pbclient
        self.parser = ConfigParser.ConfigParser()

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--server',  help='The PyBossa server')
@click.option('--api-key', help='Your PyBossa API-KEY')
@click.option('--credentials', help='Use your PyBossa credentials in .pybossa.cfg file',
              default="default")
@click.option('--project', type=click.File('r'), default='project.json')
@pass_config
def cli(config, verbose, server, api_key, credentials, project):
    """Create the cli command line."""
    # Check first for the pybossa.rc file to configure server and api-key
    home = expanduser("~")
    if os.path.isfile(os.path.join(home, '.pybossa.cfg')):
        config.parser.read(os.path.join(home, '.pybossa.cfg'))
        config.server = config.parser.get(credentials,'server')
        config.api_key = config.parser.get(credentials, 'apikey')
    config.verbose = verbose
    if server:
        config.server = server
    if api_key:
        config.api_key = api_key
    config.project = json.loads(project.read())
    config.pbclient = pbclient
    config.pbclient.set('endpoint', config.server)
    config.pbclient.set('api_key', config.api_key)
    click.echo("Config done!")


@cli.command()
@pass_config
def create_project(config):
    """Create the PyBossa project."""
    res = _create_project(config)
    click.echo(res)


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
        project = find_app_by_short_name(config.project['short_name'],
                                         config.pbclient)
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
        project = find_app_by_short_name(config.project['short_name'],
                                         config.pbclient)
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
        elif tasks_type == 'csv':
            data = StringIO.StringIO(tasks)
            reader = csv.DictReader(data, delimiter=',')
            for line in reader:
                if line.get('info'):
                    try:
                        print format_json_task(line['info'])
                    except:
                        print line['info']
        else:
            click.echo("Unknown format for the tasks file. Use json or csv.")

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
        project = find_app_by_short_name(config.project['short_name'],
                                         config.pbclient)
        if task_id:
            response = config.pbclient.delete_task(task_id)
            check_api_error(response)
        elif click.confirm("Are you sure you want to delete all the tasks and associated task runs?"):
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
