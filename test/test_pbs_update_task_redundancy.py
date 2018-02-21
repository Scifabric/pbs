"""Test module for pbs client."""
from helpers import _update_tasks_redundancy
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from pbsexceptions import *
from requests import exceptions


class TestPbsUpdateTaskRedundancy(TestDefault):

    """Test class for pbs update task redundancy commands."""

    def fake_return_tasks(self, project_id, limit, offset):
        """Fake return tasks method."""
        task = MagicMock()
        task.id = 1
        if offset == 0:
            return [task]
        else:
            return []

    @patch('helpers.find_project_by_short_name')
    @patch('helpers.enable_auto_throttling')
    def test_update_task_redundancy_individually(self, auto_mock, find_mock):
        """Test update task redundancy individually works."""
        auto_mock.return_value = (0, None)

        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        pbclient = MagicMock()
        self.config.pbclient = pbclient
        res = _update_tasks_redundancy(self.config, 1, 5)
        msg = "Task.id = 1 redundancy has been updated to 5"
        assert res == msg, res

    @patch('helpers.find_project_by_short_name')
    @patch('helpers.enable_auto_throttling')
    def test_update_task_redundancy_all_tasks(self, auto_mock, find_mock):
        """Test update task redundancy all tasks works."""
        auto_mock.return_value = (0, None)

        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project


        pbclient = MagicMock()
        pbclient.get_tasks = self.fake_return_tasks
        self.config.pbclient = pbclient
        res = _update_tasks_redundancy(self.config, None, 5)
        msg = "All tasks redundancy have been updated"
        assert res == msg, res


    @patch('helpers.find_project_by_short_name')
    @patch('helpers.enable_auto_throttling')
    def test_update_task_redundancy_fails(self, auto_mock, find_mock):
        """Test update task redundancy fails works."""
        auto_mock.return_value = (0, None)

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
        pbclient.find_project.return_value = self.error
        self.config.pbclient = pbclient
        assert_raises(ProjectNotFound, _update_tasks_redundancy, self.config,
                      9999, 5)

    def test_update_task_redundancy_connection_failed(self):
        """Test update task redundancy connection fails works."""
        pbclient = MagicMock()
        pbclient.find_project.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _update_tasks_redundancy(self.config, 1, 5)
        assert res == "Connection Error! The server http://server is not responding", res
