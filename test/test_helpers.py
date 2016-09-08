"""Test module for pbs client."""
import pbclient
import json
from default import TestDefault
from helpers import *
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions
from pbsexceptions import *


class TestHelpers(TestDefault):

    """Test class for pbs.helpers."""

    @patch('pbclient.find_project')
    def test_find_project_by_short_name(self, mock):
        """Test find_project_by_short_name returns a project."""
        mock.return_value = ['project']
        project = find_project_by_short_name('project', pbclient)
        err_msg = "It shoul return: project"
        assert project == 'project', err_msg

    @patch('pbclient.find_project')
    def test_find_project_by_short_name_returns_no_project(self, mock):
        """Test find_project_by_short_name returns a project."""
        mock.return_value = []
        assert_raises(ProjectNotFound,
                      find_project_by_short_name,
                      'project',
                      pbclient)


    @patch('pbclient.find_project')
    def test_find_project_by_short_name_connection_error(self, mock):
        """Test find_project_by_short_name connection_error is raised."""
        mock.side_effect = exceptions.ConnectionError
        assert_raises(exceptions.ConnectionError,
                      find_project_by_short_name,
                      'project',
                      pbclient)

    @patch('helpers.format_error')
    @patch('pbclient.find_project')
    def test_find_project_by_short_name_error(self, mock, mock2):
        """Test find_project_by_short_name error is printed."""
        mock.return_value = self.error
        assert_raises(ProjectNotFound, find_project_by_short_name, 'project',
                      pbclient)

    def test_check_api_error_raises_exception(self):
        """Test check_api_error raises HTTPError exception."""
        error = dict(status='failed', target='diff')
        assert_raises(exceptions.HTTPError, check_api_error, error)

    def test_check_api_error_returns_none(self):
        """Test check_api_error returns none."""
        error = self.error
        error['status'] = 'wrong'
        check_api_error(error)
        error = 'not_a_dict'
        check_api_error(error)

    @patch('pbclient.find_project')
    def test_format_error(self, mock):
        """Test format_error works."""
        e = ProjectNotFound(message="m", error=dict(error="error"))
        assert_raises(SystemExit, format_error, 'pbclient.find_project', e)

    def test_format_json_task(self):
        """Test format_json_task works."""
        tmp = {'key': 'value'}
        res = format_json_task(json.dumps(tmp))
        err_msg = "It should return a JSON object"
        assert type(res) == dict, err_msg
        assert res['key'] == tmp['key'], err_msg

        tmp = "key: value"
        res = format_json_task(tmp)
        err_msg = "It should return a string"
        assert type(res) == str, err_msg
        assert res == tmp, err_msg

    def test_create_task_info(self):
        """Test create_task_info works."""
        task = {'info': {'k': 'v'}}
        res = create_task_info(task)
        assert res == task['info']

        task = {'k': 'v'}
        res = create_task_info(task)
        assert res == task

    def test_enable_auto_throttling(self):
        """Test enable_auto_throttling works."""
        sleep, msg = enable_auto_throttling(range(10), 9)
        assert sleep is True, "Throttling should be enabled"
        assert msg is not None, "Throttling should be enabled"
        sleep, msg = enable_auto_throttling(range(10), 10)
        assert sleep is False, "Throttling should not be enabled"
        assert msg is None, "Throttling should not be enabled"

    def test_pbs_handler(self):
        """Test PbsHandler patterns works."""
        obj = PbsHandler(None, None, None, None, None)
        patterns = ['*/template.html', '*/tutorial.html',
                    '*/long_description.md', '*/results.html']
        assert obj.patterns == patterns, obj.patterns

    @patch('helpers._update_project')
    def test_pbs_handler_on_modified(self, mock):
        """Test PbsHanlder.on_modified works."""
        obj = PbsHandler('config', 'task_presenter', 'results',
                         'long_description', 'tutorial')
        event = MagicMock()
        event.src_path = '/tmp/path.html'
        obj.on_modified(event)
        mock.assert_called_with('config', 'task_presenter', 'results',
                                'long_description', 'tutorial')
