"""Test module for pbs client."""
import pbclient
import json
from helpers import *
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions
from pbsexceptions import ProjectNotFound


class TestPbsCreateProject(TestDefault):

    """Test class for pbs create project commands."""

    def test_create_project_create(self):
        """Test create_project works."""
        pbclient = MagicMock()
        pbclient.create_project.return_value = {'short_name': 'short_name', 'status_code': 200}
        self.config.pbclient = pbclient
        res = _create_project(self.config)
        assert res == 'Project: short_name created!', res

    def test_create_project_connection_error(self):
        """Test create_project connection error works."""
        pbclient = MagicMock()
        pbclient.create_project.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _create_project(self.config)
        assert res == "Connection Error! The server http://server is not responding", res

    def test_create_project_another_error(self):
        """Test create_project another error works."""
        pbclient = MagicMock()
        pbclient.create_project.return_value = self.error
        self.config.pbclient = pbclient
        assert_raises(ProjectNotFound, _create_project, self.config)
