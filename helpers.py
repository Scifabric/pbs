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
Helper functions for the pbs command line client.

This module exports the following methods:
    * find_app_by_short_name: return the project by short_name.
    * check_api_errors: check for API errors returned by a PyBossa server.
    * format_error: format error message.
    * format_json_task: format a CSV row into JSON.
"""
import csv
import json
import logging
import StringIO
from requests import exceptions

__all__ = ['find_app_by_short_name', 'check_api_error',
           'format_error', 'format_json_task', '_create_project',
           '_update_project', '_add_tasks']

def _create_project(config):
    """Create a project in a PyBossa server."""
    try:
        response = config.pbclient.create_app(config.project['name'],
                                              config.project['short_name'],
                                              config.project['description'])
        check_api_error(response)
        return ("Project: %s created!" % config.project['short_name'])
    except exceptions.ConnectionError:
        return("Connection Error! The server %s is not responding" % config.server)
    except:
        return format_error("pbclient.create_app", response)


def _update_project(config, task_presenter, long_description, tutorial):
    """Update a project."""
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
        return ("Project %s updated!" % config.project['short_name'])
    except exceptions.ConnectionError:
        return ("Connection Error! The server %s is not responding" % config.server)
    except:
        return format_error("pbclient.update_app", response)


def _add_tasks(config, tasks_file, tasks_type, priority, redundancy):
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
            return ("%s tasks added to project: %s" % (len(data),
                                                      config.project['short_name']))
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
            return ("Unknown format for the tasks file. Use json or csv.")

    except exceptions.ConnectionError:
        return ("Connection Error! The server %s is not responding" % config.server)
    except:
        return format_error("pbclient.create_task", response)



def find_app_by_short_name(short_name, pbclient):
    """Return project by short_name."""
    try:
        response = pbclient.find_app(short_name=short_name)
        check_api_error(response)
        return response[0]
    except exceptions.ConnectionError:
        raise
    except:
        format_error("pbclient.find_app", response)


def check_api_error(api_response):
    """Check if returned API response contains an error."""
    if type(api_response) == dict and (api_response.get('status') == 'failed'):
        raise exceptions.HTTPError


def format_error(module, error):
    """Format the error for the given module."""
    logging.error(module)
    # Beautify JSON error
    if type(error) == list:
        print "Project not found"
    else:
        print json.dumps(error, sort_keys=True, indent=4, separators=(',', ': '))
    exit(1)


def format_json_task(task_info):
    """Format task_info into JSON if applicable."""
    try:
        return json.loads(task_info)
    except:
        return task_info
