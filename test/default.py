"""Test module for pbs client."""
from mock import MagicMock
import pbclient


class TestDefault(object):

    """Test class for pbs.helpers."""

    config = MagicMock()
    config.server = 'http://server'
    config.api_key = 'apikey'
    config.pbclient = pbclient
    config.project = {'name': 'name',
                      'description': 'description',
                      'short_name': 'short_name'}

    def tearDown(self):
        """Tear down method."""
        self.error['status'] = 'failed'

    @property
    def error(self, action='GET',
              exception_cls='NotFound',
              exception_msg='(NotFound)',
              status='failed',
              status_code=404,
              target='/api/app'):
        """Error property."""
        return {'action': action,
                'exception_cls': exception_cls,
                'exception_msg': exception_msg,
                'status': status,
                'status_code': status_code,
                'target': target}
