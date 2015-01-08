"""Pbs class exceptions module."""


class PbsException(Exception):

    """Generic exception."""

    pass


class ProjectNotFound(Exception):

    """ProjectNotFound exception."""

    def __init__(self, message, error):
        """Init method."""
        # Call the base class constructor with the parameters it needs
        super(ProjectNotFound, self).__init__(message)

        self.error = error
        self.message = "PyBossa project not found."


class TaskNotFound(Exception):

    """TaskNotFound exception."""

    def __init__(self, message, error):
        """Init method."""
        # Call the base class constructor with the parameters it needs
        super(TaskNotFound, self).__init__(message, error)

        self.message = message
        self.error = error
