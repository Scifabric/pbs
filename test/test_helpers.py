"""Test module for pbs client."""
import pbclient
import json
from default import TestDefault
from helpers import *
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions
from pbsexceptions import *
import calendar
import datetime


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
        """Test find_project_by_short_name raises ProjectNotFound for all=0."""
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
        error = dict(status='failed', target='diff', exception_cls='err')
        assert_raises(exceptions.HTTPError, check_api_error, error)

    def test_check_general_http_api_error_raises_exception(self):
        """Test check_api_error raises HTTPError exception."""
        error = dict(code=500)
        assert_raises(exceptions.HTTPError, check_api_error, error)

    def test_check_api_error_raises_database_error(self):
        """Test check_api_error raises DatabaseError exception."""
        error = dict(status='failed', target='diff',
                     exception_cls='ProgrammingError')
        assert_raises(DatabaseError, check_api_error, error)

    def test_check_api_error_raises_database_error(self):
        """Test check_api_error raises ProjectAlreadyExists exception."""
        error = dict(status='failed', target='project',
                     exception_cls='DBIntegrityError')
        assert_raises(ProjectAlreadyExists, check_api_error, error)

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

    @patch('requests.head')
    def test_enable_auto_throttling(self, mock):
        """Test enable_auto_throttling works."""
        mock.return_value = MagicMock(['headers'])
        config = MagicMock(['server'])

        now = calendar.timegm(datetime.datetime.utcnow().utctimetuple()) + 10

        mock.return_value.headers = {'X-RateLimit-Remaining': 9,
                                     'X-RateLimit-Reset': now}
        sleep, msg = enable_auto_throttling(config, list(range(10)))
        assert sleep > 0, "Throttling should be enabled"
        assert msg is not None, "Throttling should be enabled"

        mock.return_value.headers = {'X-RateLimit-Remaining': 11}
        sleep, msg = enable_auto_throttling(config, list(range(10)))
        assert sleep == 0, "Throttling should not be enabled"
        assert msg is None, "Throttling should not be enabled"

    def test_pbs_handler(self):
        """Test PbsHandler patterns works."""
        obj = PbsHandler(None, None, None, None, None)
        patterns = ['*/template.html', '*/tutorial.html',
                    '*/long_description.md', '*/results.html',
                    '*/bundle.js', '*/bundle.min.js']
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

    @patch('helpers.os.path.isfile')
    def test_update_bundle_js(self, mock):
        """Test update task presenter with bundle js."""
        mock.return_value = False
        presenter = '<div></div>'
        project_dict = dict(short_name='foo',
                            id=1,
                            info={'task_presenter': presenter})
        project = pbclient.Project(project_dict)
        _update_task_presenter_bundle_js(project)
        err_msg = "There should not be any JS as there is no bundle.js or bundle.min.js"
        assert project.info['task_presenter'] == presenter, err_msg

    @patch('helpers.os.path.isfile')
    def test_update_not_bundle_js(self, mock):
        """Test update task presenter with bundle js."""
        mock.return_value = False
        presenter = '<div></div>'
        project_dict = dict(short_name='foo',
                            id=1,
                            info={'task_presenter': presenter})
        project = pbclient.Project(project_dict)
        _update_task_presenter_bundle_js(project)
        err_msg = "There should not be any JS as there is no bundle.js or bundle.min.js"
        assert project.info['task_presenter'] == presenter, err_msg

    @patch('helpers.os.path.isfile')
    def test_update_bundle_js(self, mock):
        """Test update task presenter with bundle js."""
        items = [False, True]
        def return_effect(*args):
            return items.pop(0)
        mock.side_effect = return_effect
        presenter = '<div></div>'
        project_dict = dict(short_name='foo',
                            id=1,
                            info={'task_presenter': presenter})
        project = pbclient.Project(project_dict)
        _update_task_presenter_bundle_js(project)
        with open('bundle.js') as f:
            js = f.read()
        err_msg = "There should be the content of bundle.js"
        assert js in project.info['task_presenter'], err_msg

    @patch('helpers.os.path.isfile')
    def test_update_bundle_min_js(self, mock):
        """Test update task presenter with bundle.min.js."""
        items = [True, False]
        def return_effect(*args):
            return items.pop(0)
        mock.side_effect = return_effect
        presenter = '<div></div>'
        project_dict = dict(short_name='foo',
                            id=1,
                            info={'task_presenter': presenter})
        project = pbclient.Project(project_dict)
        _update_task_presenter_bundle_js(project)
        with open('bundle.min.js') as f:
            js = f.read()
        err_msg = "There should be the content of bundle.min.js"
        assert js in project.info['task_presenter'], err_msg
