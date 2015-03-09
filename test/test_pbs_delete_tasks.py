"""Test module for pbs client."""
import pbclient
import json
from helpers import *
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions
from pbsexceptions import *


class TestPbsDeleteTask(TestDefault):

    """Test class for pbs delete task commands."""

    @patch('helpers.find_project_by_short_name')
    def test_delete_task(self, find_mock):
        """Test delete task works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        pbclient.delete_task.return_value = []
        self.config.pbclient = pbclient
        res = _delete_tasks(self.config, 1)
        assert res == "Task.id = 1 and its associated task_runs have been deleted", res

    @patch('helpers.find_project_by_short_name')
    def test_delete_all_tasks(self, find_mock):
        """Test delete all tasks works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task = MagicMock()
        task.id = 1

        pbclient = MagicMock()
        pbclient.get_tasks.side_effect = [[task], []]
        self.config.pbclient = pbclient

        res = _delete_tasks(self.config, None, limit=1, offset=0)
        assert res == "All tasks and task_runs have been deleted", res

    @patch('helpers.find_project_by_short_name')
    def test_delete_connection_error(self, find_mock):
        """Test delete tasks connection error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        pbclient.delete_task.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _delete_tasks(self.config, 1)
        assert res == "Connection Error! The server http://server is not responding", res

    @patch('helpers.find_project_by_short_name')
    def test_delete_connection_error_all_tasks(self, find_mock):
        """Test delete tasks connection error works for all tasks."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        pbclient.delete_task.side_effect = exceptions.ConnectionError
        task = MagicMock()
        task.id = 1
        pbclient.get_tasks.return_value = [task]
        self.config.pbclient = pbclient
        res = _delete_tasks(self.config, None)
        assert res == "Connection Error! The server http://server is not responding", res

    @patch('helpers.find_project_by_short_name')
    def test_delete_another_error_all_tasks(self, find_mock):
        """Test delete tasks another error works for all tasks."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        pbclient.delete_task.return_value = self.error
        task = MagicMock()
        task.id = 1
        pbclient.get_tasks.return_value = [task]
        self.config.pbclient = pbclient
        assert_raises(ProjectNotFound, _delete_tasks, self.config, None)

    @patch('helpers.find_project_by_short_name')
    def test_delete_another_error_one_tasks(self, find_mock):
        """Test delete tasks another error works for one task."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        pbclient.delete_task.return_value = self.error_task
        self.config.pbclient = pbclient
        assert_raises(TaskNotFound, _delete_tasks, self.config, 1)
