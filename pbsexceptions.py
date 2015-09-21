# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.
"""Pbs class exceptions module."""


class PbsException(Exception):

    """Generic exception."""

    pass


class ProjectNotFound(PbsException):

    """ProjectNotFound exception."""

    def __init__(self, message, error):
        """Init method."""
        # Call the base class constructor with the parameters it needs
        super(ProjectNotFound, self).__init__(message)

        self.error = error
        self.message = "PyBossa project not found."


class TaskNotFound(PbsException):

    """TaskNotFound exception."""

    def __init__(self, message, error):
        """Init method."""
        # Call the base class constructor with the parameters it needs
        super(TaskNotFound, self).__init__(message, error)

        self.message = message
        self.error = error
