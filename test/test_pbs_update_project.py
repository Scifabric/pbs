import pbclient
import json
from helpers import *
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions
from pbsexceptions import ProjectNotFound

class TestPbsUpdateProject(TestDefault):

    """Test class for pbs update project commands."""

    @patch('helpers.find_project_by_short_name')
    def test_update_project_create(self, find_mock):
        """Test update_project works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = "test/template.html"

        results = "test/results.html"

        tutorial = "test/tutorial.html"

        long_description = "test/long_description.md"

        pbclient = MagicMock()
        pbclient.update_project.return_value = {'short_name': 'short_name'}
        self.config.pbclient = pbclient
        res = _update_project(self.config, task_presenter, results,
                              long_description, tutorial)
        assert res == 'Project short_name updated!', res

    @patch('helpers.find_project_by_short_name')
    def test_update_project_connection_error(self, find_mock):
        """Test update_project connection error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = "test/template.html"

        results = "test/results.html"

        tutorial = "test/tutorial.html"

        long_description = "test/long_description.md"

        pbclient = MagicMock()
        pbclient.update_project.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _update_project(self.config, task_presenter, results,
                              long_description, tutorial)
        assert res == "Connection Error! The server http://server is not responding", res

    @patch('helpers.find_project_by_short_name')
    def test_update_project_another_error(self, find_mock):
        """Test update_project another error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = "test/template.html"

        results = "test/results.html"

        tutorial = "test/tutorial.html"

        long_description = "test/long_description.md"

        pbclient = MagicMock()
        pbclient.update_project.return_value = self.error
        self.config.pbclient = pbclient
        res = _update_project(self.config, task_presenter, results,
                              long_description, tutorial)
        msg = ("Project not found! The project: short_name is missing." \
               " Use the flag --all=1 to search in all the server ")
        assert res == msg, msg
