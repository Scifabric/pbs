import pbclient
import json
from helpers import *
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions

class TestHelpers(TestDefault):

    """Test class for pbs.helpers."""

    @patch('helpers.find_app_by_short_name')
    def test_update_project_create(self, find_mock):
        """Test update_project works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = MagicMock()
        task_presenter.read.return_value = "presenter"

        tutorial = MagicMock()
        tutorial.read.return_value = "tutorial"

        long_description = MagicMock()
        long_description.read.return_value = "long_description"

        pbclient = MagicMock()
        pbclient.update_app.return_value = {'short_name': 'short_name'}
        self.config.pbclient = pbclient
        res = _update_project(self.config, task_presenter,
                              long_description, tutorial)
        assert res == 'Project short_name updated!', res

    @patch('helpers.find_app_by_short_name')
    def test_update_project_connection_error(self, find_mock):
        """Test update_project connection error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = MagicMock()
        task_presenter.read.return_value = "presenter"

        tutorial = MagicMock()
        tutorial.read.return_value = "tutorial"

        long_description = MagicMock()
        long_description.read.return_value = "long_description"

        pbclient = MagicMock()
        pbclient.update_app.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _update_project(self.config, task_presenter,
                              long_description, tutorial)
        assert res == "Connection Error! The server http://server is not responding", res

    @patch('helpers.find_app_by_short_name')
    def test_update_project_another_error(self, find_mock):
        """Test update_project another error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = MagicMock()
        task_presenter.read.return_value = "presenter"

        tutorial = MagicMock()
        tutorial.read.return_value = "tutorial"

        long_description = MagicMock()
        long_description.read.return_value = "long_description"

        pbclient = MagicMock()
        pbclient.update_app.return_value = self.error
        self.config.pbclient = pbclient
        assert_raises(SystemExit, _update_project, self.config,
                      task_presenter, long_description, tutorial)
