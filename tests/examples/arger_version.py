"""
this following are equivalent of other than the function body

.. literalinclude:: ./argparser/subparsers.py
"""

from arger import Arger


arg = Arger("Test Commands")


@arg
def list(dirname):
    """List contents

    :param dirname: name of directory
    """
    return dirname


@arg
def create(dirname, read_only=False):
    """Create a directory

    :param dirname: 'New directory to create'
    """
    return dirname, read_only


@arg
def delete(dirname, recursive=False):
    """Remove a directory

    :param recursive: Remove the contents of the directory, too
    :param dirname: The directory to remove
    """
    return dirname, recursive


if __name__ == '__main__':
    arg.dispatch()
