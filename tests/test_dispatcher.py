from pathlib import Path
from typing import Any, Callable, List

import pytest

from arger import Arger


@pytest.fixture
def arger(pyfile: Path) -> Arger:
    ctx: dict = {}
    exec(pyfile.read_text(), ctx)
    return ctx["arger"]


@pytest.fixture
def args(cmd: str):
    args = cmd.strip("$ ").split(" ")
    args.pop(0)  # python
    args.pop(0)  # filename
    return args


def test_example(capsys, arger, args, expected: str):
    if "error" in expected or expected.startswith('usage:'):
        with pytest.raises(SystemExit):
            arger.run(*args)  # start function
    else:
        arger.run(*args)

    capture = capsys.readouterr()
    out = capture.err or capture.out

    if out != expected:
        import time

        tmp = Path('-'.join(args) + str(time.time()) + ".log")
        tmp.write_text("\n\n\n".join([out, expected]))
    assert out == expected


# def test_var_positional_help(capsys, arg):
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(*filenames):
#         "list files"
#         pass
#
#     raises(SystemExit, main, ["--help"])
#     out, error = capture.reset()
#     assert error == ""
#     assert (
#         out.strip()
#         == """usage: py.test [-h] [filenames [filenames ...]]
# list files
# positional arguments:
#   filenames
# optional arguments:
#   -h, --help  show this help message and exit"""
#     )


#
# def test_required_positional():
#     result = Checker()
#
#     @opterate
#     def main(source, dest):
#         "move a file"
#         result.source = source
#         result.dest = dest
#
#     main(["sourcename", "destname"])
#     assert result.source == "sourcename"
#     assert result.dest == "destname"
#
#
# def test_too_many_positional():
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(source, dest):
#         "copy a file"
#         pass
#
#     raises(SystemExit, main, ["sourcename", "destname", "somethingextra"])
#     out, error = capture.reset()
#     assert out == ""
#     assert (
#         error.strip()
#         == """usage: py.test [-h] source dest
# py.test: error: unrecognized arguments: somethingextra"""
#     )
#
#
# def test_not_enough_positional():
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(source, dest):
#         "copy a file"
#         pass
#
#     raises(SystemExit, main, ["sourcename"])
#     out, error = capture.reset()
#     assert out == ""
#     assert error.strip() in (  # python2, python 3 versions of argparse
#         """usage: py.test [-h] source dest
# py.test: error: too few arguments""",
#         """usage: py.test [-h] source dest
# py.test: error: the following arguments are required: dest""",
#     )
#
#
# def test_positional_help_text():
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(source, dest):
#         "copy a file"
#         pass
#
#     raises(SystemExit, main, ["-h"])
#     out, error = capture.reset()
#     assert error == ""
#     assert (
#         out.strip()
#         == """usage: py.test [-h] source dest
# copy a file
# positional arguments:
#   source
#   dest
# optional arguments:
#   -h, --help  show this help message and exit"""
#     )
#
#
# def test_positional_help_text_descriptions():
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(source, dest):
#         """copy a file
#         :param source: The filename to copy
#         :param dest: The name of the new copied file"""
#         pass
#
#     raises(SystemExit, main, ["-h"])
#     out, error = capture.reset()
#     assert error == ""
#     assert (
#         out.strip()
#         == """usage: py.test [-h] source dest
# copy a file
# positional arguments:
#   source      The filename to copy
#   dest        The name of the new copied file
# optional arguments:
#   -h, --help  show this help message and exit"""
#     )
#
#
# def test_keyword_option():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main(["--mine", "avalue"])
#     assert result.myoption == "avalue"
#
#
# def test_keyword_option_short():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main(["-m", "avalue"])
#     assert result.myoption == "avalue"
#
#
# def test_keyword_option_default_helptext():
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option."""
#         print("never called")
#
#     raises(SystemExit, main, ["-h"])
#     out, error = capture.reset()
#     assert error == ""
#     print(out)
#     assert (
#         out.strip()
#         == """usage: py.test [-h] [-m MYOPTION]
# A script with one optional option.
# optional arguments:
#   -h, --help            show this help message and exit
#   -m MYOPTION, --myoption MYOPTION"""
#     )
#
#
# def test_keyword_option_helptext():
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: -m --mine the myoption helptext"""
#         print("never called")
#
#     raises(SystemExit, main, ["-h"])
#     out, error = capture.reset()
#     assert error == ""
#     assert (
#         out.strip()
#         == """usage: py.test [-h] [-m MYOPTION]
# A script with one optional option.
# optional arguments:
#   -h, --help            show this help message and exit
#   -m MYOPTION, --mine MYOPTION
#                         the myoption helptext"""
#     )
#
#
# def test_short_option_only():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: -m the myoption helptext"""
#         result.myoption = myoption
#
#     main(["-m", "avalue"])
#     assert result.myoption == "avalue"
#
#
# def test_long_option_only():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main(["--mine", "avalue"])
#     assert result.myoption == "avalue"
#
#
# def test_keyword_option_is_optional():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main([])
#     assert result.myoption == "novalue"
#
#
# def test_keyword_option_no_identifier():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: the myoption helptext"""
#         result.myoption = myoption
#
#     main(["--myoption", "avalue"])
#     assert result.myoption == "avalue"
#
#
# def test_keyword_option_no_identifier_helptext():
#     capture = py.io.StdCapture()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option.
#         :param myoption: the myoption helptext"""
#         print("never called")
#
#     raises(SystemExit, main, ["-h"])
#     out, error = capture.reset()
#     assert error == ""
#     assert (
#         out.strip()
#         == """usage: py.test [-h] [-m MYOPTION]
# A script with one optional option.
# optional arguments:
#   -h, --help            show this help message and exit
#   -m MYOPTION, --myoption MYOPTION
#                         the myoption helptext"""
#     )
#
#
# def test_keyword_option_no_identifier_docstring():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue"):
#         """A script with one optional option, but no parameter in docstring."""
#         result.myoption = myoption
#
#     main(["--myoption", "avalue"])
#     assert result.myoption == "avalue"
#
#
# def test_keyword_list_option():
#     result = Checker()
#
#     @opterate
#     def main(myoption=[]):
#         """A script with one optional option that can be repeated.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main(["-m", "hi"])
#     assert result.myoption == ["hi"]
#
#
# def test_keyword_list_multiple_options():
#     result = Checker()
#
#     @opterate
#     def main(myoption=[]):
#         """A script with one optional option that can be repeated.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main(["-m", "hi", "-m", "yo"])
#     assert result.myoption == ["hi", "yo"]
#
#
# def test_keyword_list_no_options():
#     result = Checker()
#
#     @opterate
#     def main(myoption=[]):
#         """A script with one optional option that can be repeated.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main([])
#     assert result.myoption == []
#
#
# def test_keyword_list_choices():
#     result = Checker()
#
#     @opterate
#     def main(myoption=["hi", "hello"]):
#         """A script with one optional option that can be repeated.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#
#     main(["-m", "hi"])
#     assert result.myoption == "hi"
#
#
# def test_required_arg_kw_option():
#     result = Checker()
#
#     @opterate
#     def main(firstarg, myoption="novalue"):
#         """A script with one required argument and one optional value.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#         result.firstarg = firstarg
#
#     main(["-m", "avalue", "thearg"])
#     assert result.myoption == "avalue"
#     assert result.firstarg == "thearg"
#
#
# def test_required_arg_kw_option_is_optional():
#     result = Checker()
#
#     @opterate
#     def main(firstarg, myoption="novalue"):
#         """A script with one required argument and one optional value.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#         result.firstarg = firstarg
#
#     main(["thearg"])
#     assert result.myoption == "novalue"
#     assert result.firstarg == "thearg"
#
#
# def test_varargs_kw_option():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue", *someargs):
#         """A script with one required argument and one optional value.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#         result.someargs = someargs
#
#     main(["-m", "avalue", "anarg", "thearg"])
#     assert result.myoption == "avalue"
#     assert result.someargs == ("anarg", "thearg")
#
#
# def test_varargs_kw_option_is_optional():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue", *someargs):
#         """A script with one required argument and one optional value.
#         :param myoption: -m --mine the myoption helptext"""
#         result.myoption = myoption
#         result.someargs = someargs
#
#     main(["anarg", "thearg"])
#     assert result.myoption == "novalue"
#     assert result.someargs == ("anarg", "thearg")
#
#
# def test_two_kw_options():
#     result = Checker()
#
#     @opterate
#     def main(myoption="novalue", secondoption=False):
#         """A script with one required argument and one optional value.
#         :param myoption: -m --mine the myoption helptext
#         :param secondoption: -s --second the second helptext"""
#         result.myoption = myoption
#         result.secondoption = secondoption
#
#     main(["-m", "avalue", "--second"])
#     assert result.myoption == "avalue"
#     assert result.secondoption is True
#
#
# def test_two_kw_options_same_first_letter():
#     result = Checker()
#
#     @opterate
#     def main(myoption=False, mysecondoption=False):
#         """A script with two optional values.
#         :param myoption: the myoption helptext
#         :param secondoption: the second helptext"""
#         result.myoption = myoption
#         result.mysecondoption = mysecondoption
#
#     main(["-m", "-y"])
#     assert result.myoption is True
#     assert result.mysecondoption is True
#
#
# def test_kw_options_no_letters_left():
#     result = Checker()
#
#     @opterate
#     def main(m_opt=False, y_opt=False, my=False):
#         """A script with three optional values, no short option left for last
#         value.
#         :param m_opt: the m_opt helptext
#         :param y_opt: the y_opt helptext
#         :param my: the my helptext"""
#         result.m_opt = m_opt
#         result.y_opt = y_opt
#         result.my = my
#
#     capture = py.io.StdCapture()
#     raises(SystemExit, main, ["-h"])
#     out, error = capture.reset()
#     assert error == ""
#     print(out)
#     assert (
#         out.strip()
#         == """usage: py.test [-h] [-m] [-y] [--my]
# A script with three optional values, no short option left for last value.
# optional arguments:
#   -h, --help   show this help message and exit
#   -m, --m_opt  the m_opt helptext
#   -y, --y_opt  the y_opt helptext
#   --my         the my helptext"""
#     )
#
#
# def test_comprehensive_example():
#     result = Checker()
#
#     @opterate
#     def main(
#         filename1,
#         filename2,
#         recursive=False,
#         interactive=False,
#         suffix="~",
#         *other_filenames,
#     ):
#         """An example copy script with some example parameters borrowed from
#         the cp man page. Illustrates some of the simplicity and pitfalls of
#         this option parsing method.
#         :param recursive: -r --recursive copy directories
#             recursively
#         :param interactive: -i --interactive prompt before
#             overwrite
#         :param suffix: -S --suffix override the usual backup
#             suffix """
#         # When two filenames are required and others optional you have to build
#         # funny lists like this.
#         filenames = [filename1, filename2] + list(other_filenames)
#         filenames.pop()
#         # call function that does the actual checking, copying, like with any
#         # option parsed app.
#         #
#         # ...
#         result.filename1 = filename1
#         result.filename2 = filename2
#         result.recursive = recursive
#         result.interactive = interactive
#         result.suffix = suffix
#         result.other_filenames = other_filenames
#
#     capture = py.io.StdCapture()
#     raises(SystemExit, main, ["-h"])
#     out, error = capture.reset()
#
#     assert error == ""
#     assert (
#         out.strip()
#         == """usage: py.test [-h] [-r] [-i] [-S SUFFIX]
#                filename1 filename2 [other_filenames [other_filenames ...]]
# An example copy script with some example parameters borrowed from the cp man
# page. Illustrates some of the simplicity and pitfalls of this option parsing
# method.
# positional arguments:
#   filename1
#   filename2
#   other_filenames
# optional arguments:
#   -h, --help            show this help message and exit
#   -r, --recursive       copy directories recursively
#   -i, --interactive     prompt before overwrite
#   -S SUFFIX, --suffix SUFFIX
#                         override the usual backup suffix"""
#     )
#
#     main(["source", "dest"])
#     assert result.filename1 == "source"
#     assert result.filename2 == "dest"
#     assert result.recursive is False
#     assert result.interactive is False
#     assert result.suffix == "~"
#     assert not result.other_filenames
#
#     main(["source", "dest", "-r"])
#     assert result.filename1 == "source"
#     assert result.filename2 == "dest"
#     assert result.recursive is True
#     assert result.interactive is False
#     assert result.suffix == "~"
#     assert not result.other_filenames
#
#     main(["-i", "source", "-r", "dest", "another", "directory"])
#     assert result.filename1 == "source"
#     assert result.filename2 == "dest"
#     assert result.recursive is True
#     assert result.interactive is True
#     assert result.suffix == "~"
#     assert result.other_filenames == ("another", "directory")
#
#     # NOTE: can't put -r in the middle, due to argparse bug
#     # See: http://bugs.python.org/issue14191
#
#     main(["-i", "source", "dest", "another", "directory", "-r"])
#     assert result.filename1 == "source"
#     assert result.filename2 == "dest"
#     assert result.recursive is True
#     assert result.interactive is True
#     assert result.suffix == "~"
#     assert result.other_filenames == ("another", "directory")
