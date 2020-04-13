from arger import Arger
import sh

arger = Arger(description="Common set of tasks to run")


@arger.add_cmd
def release(type: str):
    """Bump version, tag and push them.

    # todo: create an Enum
    :param type: one of patch, minor, major, prepatch, preminor, premajor, prerelease. as supported by poetry version
    """
    version = sh()
