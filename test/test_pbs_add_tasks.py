import json
from helpers import *
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions
from pbsexceptions import *

class TestPbsAddTask(TestDefault):

    """Test class for pbs add tasks commands."""

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_json_with_info(self, find_mock):
        """Test add_tasks json with info field works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = json.dumps([{'info': {'key': 'value'}}])

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'json', 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_json_from_filextension(self, find_mock):
        """Test add_tasks json without specifying file extension works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.name = 'tasks.json'
        tasks.read.return_value = json.dumps([{'info': {'key': 'value'}}])

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, None, 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_csv_with_info(self, find_mock):
        """Test add_tasks csv with info field works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = "info, value\n, %s, 2" % json.dumps({'key':'value'})

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'csv', 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_csv_from_filextension(self, find_mock):
        """Test add_tasks csv without specifying file extension works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.name = 'tasks.csv'
        tasks.read.return_value = "info, value\n, %s, 2" % json.dumps({'key':'value'})

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, None, 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_json_without_info(self, find_mock):
        """Test add_tasks json without info field works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = json.dumps([{'key': 'value'}])

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'json', 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_csv_without_info(self, find_mock):
        """Test add_tasks csv without info field works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = "key, value\n, 1, 2"

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'csv', 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_unknow_type_from_filextension(self, find_mock):
        """Test add_tasks with unknown type from file extension works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.name = 'tasks.doc'
        tasks.read.return_value = "key, value\n, 1, 2"

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, None, 0, 30)
        assert res == ("Unknown format for the tasks file. Use json, csv, po or "
                      "properties."), res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_unknow_type(self, find_mock):
        """Test add_tasks with unknown type works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = "key, value\n, 1, 2"

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'key': 'value'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'doc', 0, 30)
        assert res == ("Unknown format for the tasks file. Use json, csv, po or "
                      "properties."), res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_csv_connection_error(self, find_mock):
        """Test add_tasks csv connection error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = "key, value\n, 1, 2"

        pbclient = MagicMock()
        pbclient.create_task.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'csv', 0, 30)
        assert res == "Connection Error! The server http://server is not responding", res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_json_connection_error(self, find_mock):
        """Test add_tasks json connection error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = json.dumps([{'key': 'value'}])

        pbclient = MagicMock()
        pbclient.create_task.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'json', 0, 30)
        assert res == "Connection Error! The server http://server is not responding", res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_another_error(self, find_mock):
        """Test add_tasks another error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = json.dumps([{'key': 'value'}])

        pbclient = MagicMock()
        pbclient.create_task.return_value = self.error
        self.config.pbclient = pbclient
        assert_raises(ProjectNotFound, _add_tasks, self.config,
                      tasks, 'json', 0, 30)

    @patch('polib.pofile')
    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_po_with_info(self, find_mock, po_mock):
        """Test add_tasks po with info field works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()
        find_mock.return_value = project

        entry = MagicMock()
        entry.msgid = 'English'
        entry.msgtr = ''
        po = MagicMock()
        po.untranslated_entries.return_value = [entry]
        po_mock.return_value = po

        tasks = MagicMock()
        tasks.read.return_value = json.dumps([{'info': {'msgid': 'English',
                                                        'msgtr':''}}])

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'msgid': 'English',
                                                               'msgtr': ''}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'po', 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('polib.pofile')
    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_po_from_filextension(self, find_mock, po_mock):
        """Test add_tasks po without specifying file extension works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()
        find_mock.return_value = project

        entry = MagicMock()
        entry.msgid = 'English'
        entry.msgtr = ''
        po = MagicMock()
        po.untranslated_entries.return_value = [entry]
        po_mock.return_value = po

        tasks = MagicMock()
        tasks.name = 'tasks.po'
        tasks.read.return_value = json.dumps([{'info': {'msgid': 'English',
                                                        'msgtr':''}}])

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'msgid': 'English',
                                                               'msgtr': ''}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, None, 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_properties_with_info(self, find_mock):
        """Test add_tasks properties with info field works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()
        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = "foo_id= foo\n"

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'var_id': 'foo_id',
                                                               'string': ' foo'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, 'properties', 0, 30)
        assert res == '1 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    def test_add_tasks_properties_from_filextension(self, find_mock):
        """Test add_tasks properties without specifying file extension works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()
        find_mock.return_value = project

        tasks = MagicMock()
        tasks.name = 'tasks.properties'
        tasks.read.return_value = "foo_id= foo\n"

        pbclient = MagicMock()
        pbclient.create_task.return_value = {'id': 1, 'info': {'var_id': 'foo_id',
                                                               'string': ' foo'}}
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, tasks, None, 0, 30)
        assert res == '1 tasks added to project: short_name', res
