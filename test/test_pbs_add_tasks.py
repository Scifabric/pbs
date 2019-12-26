import json
from helpers import *
from default import TestDefault
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions
from pbsexceptions import *
from openpyxl import Workbook

class TestPbsAddTask(TestDefault):

    """Test class for pbs add tasks commands."""

    @patch('helpers.find_project_by_short_name')
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_json_with_info(self, auto_mock, find_mock):
        """Test add_tasks json with info field works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_json_from_filextension(self, auto_mock, find_mock):
        """Test add_tasks json without specifying file extension works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_csv_with_info(self, auto_mock, find_mock):
        """Test add_tasks csv with info field works."""
        auto_mock.return_value = (0, None)
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

    @patch('helpers.openpyxl.load_workbook')
    @patch('helpers.find_project_by_short_name')
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_excel_with_info(self, auto_mock, find_mock, workbook_mock):
        """Test add_tasks excel with info field works."""
        auto_mock.return_value = (0, None)

        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()
        project.id = 1

        wb = Workbook()
        ws = wb.active

        headers = ['Column Name', 'foo']
        ws.append(headers)
        for row in range(2, 10):
            ws.append(['value', 'bar'])

        ws.append([None, None])
        ws.append([None, None])
        file_name = '/tmp/tasks.xlsx'
        wb.save(file_name)

        file_handler = open(file_name)

        find_mock.return_value = project

        tasks = MagicMock()
        tasks.read.return_value = file_handler

        workbook_mock.return_value = wb

        pbclient = MagicMock()
        self.config.pbclient = pbclient
        res = _add_tasks(self.config, file_handler, 'xlsx', 0, 30)
        self.config.pbclient.create_task.assert_called_with(project_id=find_mock().id,
                                                            info={'column_name': 'value',
                                                                  'foo': 'bar'},
                                                            n_answers=30,
                                                            priority_0=0)
        assert res == '8 tasks added to project: short_name', res

    @patch('helpers.find_project_by_short_name')
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_csv_from_filextension(self, auto_mock, find_mock):
        """Test add_tasks csv without specifying file extension works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_json_without_info(self, auto_mock, find_mock):
        """Test add_tasks json without info field works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_csv_without_info(self, auto_mock, find_mock):
        """Test add_tasks csv without info field works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_unknow_type_from_filextension(self, auto_mock, find_mock):
        """Test add_tasks with unknown type from file extension works."""
        auto_mock.return_value = (0, None)
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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_unknow_type(self, auto_mock, find_mock):
        """Test add_tasks with unknown type works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_csv_connection_error(self, auto_mock, find_mock):
        """Test add_tasks csv connection error works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_json_connection_error(self, auto_mock, find_mock):
        """Test add_tasks json connection error works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_another_error(self, auto_mock, find_mock):
        """Test add_tasks another error works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_po_with_info(self, auto_mock, find_mock, po_mock):
        """Test add_tasks po with info field works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_po_from_filextension(self, auto_mock, find_mock, po_mock):
        """Test add_tasks po without specifying file extension works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_properties_with_info(self, auto_mock, find_mock):
        """Test add_tasks properties with info field works."""
        auto_mock.return_value = (0, None)

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
    @patch('helpers.enable_auto_throttling')
    def test_add_tasks_properties_from_filextension(self, auto_mock, find_mock):
        """Test add_tasks properties without specifying file extension works."""
        auto_mock.return_value = (0, None)

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

    def test_empty_row(self):
        """Test that empty_row method detects it properly."""
        empty = [None, None, None, None]
        assert row_empty(empty) is True
        empty = [None, None, None, 'foo']
        assert row_empty(empty) is False
        empty = [None, 'foo', None, 'foo']
        assert row_empty(empty) is False
