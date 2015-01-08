"""Test module for pbs client."""
from helpers import _update_tasks_redundancy
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from pbsexceptions import *
from requests import exceptions


class TestHelpers(TestDefault):

    """Test class for pbs.helpers."""

    @patch('helpers.find_app_by_short_name')
    def test_update_task_redundancy(self, find_mock):
        """Test update task redundancy works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        # pbclient.update_task.return_value = []
        self.config.pbclient = pbclient
        res = _update_tasks_redundancy(self.config, 1, 5)
        msg = "Task.id = 1 redundancy has been updated to 5"
        assert res == msg, res

    @patch('helpers.find_app_by_short_name')
    def test_update_task_redundancy_fails(self, find_mock):
        """Test update task redundancy fails works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        pbclient.find_tasks.return_value = self.error_task
        self.config.pbclient = pbclient
        assert_raises(TaskNotFound, _update_tasks_redundancy, self.config,
                      9999, 5)

    def test_update_task_redundancy_project_not_found(self):
        """Test update task redundancy project not found works."""
        pbclient = MagicMock()
        pbclient.find_app.return_value = self.error
        self.config.pbclient = pbclient
        assert_raises(ProjectNotFound, _update_tasks_redundancy, self.config,
                      9999, 5)

    def test_update_task_redundancy_connection_failed(self):
        """Test update task redundancy connection fails works."""
        pbclient = MagicMock()
        pbclient.find_app.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _update_tasks_redundancy(self.config, 1, 5)
        assert res == "Connection Error! The server http://server is not responding", res
