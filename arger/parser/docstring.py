import functools
import re
from typing import Any, Dict, List, NamedTuple, Optional, Tuple


class ParamDocTp(NamedTuple):
    type_hint: Any
    flags: List[str]
    doc: str


class _ParamDoc(NamedTuple):
    name: str
    type_hint: Any
    doc: List[str]  # lines


class DocstringTp(NamedTuple):
    description: str
    epilog: str
    params: Dict[str, ParamDocTp]


def get_flags_from_param_doc(doc: str, flag_symbol='-') -> Tuple[List[str], str]:
    """Parse flags defined in param's doc

    Examples:
        ''':param arg1: -a --arg this is the document'''
    """
    doc_parts = []
    flags = []
    for part in doc.split():
        if part.startswith(flag_symbol) and not doc_parts:
            # strip both comma and empty space
            flags.append(part.strip(", ").strip())
        else:
            doc_parts.append(part)
    return flags, " ".join(doc_parts)


class DocstringParser:
    """Abstract class"""

    pattern: re.Pattern

    def parse(self, doc: str) -> DocstringTp:
        raise NotImplementedError

    def matches(self, doc: str) -> bool:
        return bool(self.pattern.search(doc))


class NumpyDocParser(DocstringParser):
    """Implement Numpy Docstring format parser
    `Example <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy>`_
    """

    def __init__(self):
        self.pattern = re.compile(r'(Parameters\n[-]+)')
        self.section_ptrn = re.compile(r'\n\s*(?P<section>\w+)\n\s*[-]+\n+')
        self.param_ptrn = re.compile(
            r'^(?P<param>\w+)[ \t]*:[ \t]*(?P<type>\w+)?'
        )  # matches parameter_name e.g. param1: or param2 (int):

    def get_rest_of_section(self, params: str) -> (str, str):
        other_sect = self.section_ptrn.search(params)
        if other_sect:
            pos = other_sect.start()
            return params[pos:].strip(), params[:pos]
        return '', params

    def parse_params(self, params: str) -> Dict[str, ParamDocTp]:
        docs: List[_ParamDoc] = []
        for line in params.splitlines():
            match = self.param_ptrn.search(line)
            if match:
                result = match.groupdict()
                doc = [result['doc']] if 'doc' in result else []
                docs.append(_ParamDoc(result['param'], result['type'], doc))
            elif docs:
                docs[-1].doc.append(line)

        return {
            p.name.strip('*'): ParamDocTp(
                p.type_hint, *get_flags_from_param_doc(' '.join(p.doc))
            )
            for p in docs
        }

    def parse(self, doc: str) -> DocstringTp:
        desc, _, params = self.pattern.split(doc, maxsplit=1)
        other_sect, params = self.get_rest_of_section(params)
        return DocstringTp(desc, other_sect, params=self.parse_params(params))


class GoogleDocParser(NumpyDocParser):
    """Implement Google Docstring format parser
    `Example <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_
    """

    def __init__(self):
        self.pattern = re.compile(r'\s(Args|Arguments):\s')
        self.section_ptrn = re.compile(r'\n(?P<section>[A-Z]\w+):\n+')
        self.param_ptrn = re.compile(
            r'^\s+(?P<param>[*\w]+)\s*(\((?P<type>[\s,`:\w]+)\))?:\s*(?P<doc>[\s\S]+)'
        )  # matches parameter_name e.g. param1 (type): description


class RstDocParser(DocstringParser):
    """Sphinx rst-style docstrings parser
    `Example <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
    """

    def __init__(self):
        self.pattern = re.compile(r':param')
        self.section_ptrn = re.compile(
            r'\n:[\w]+\s'
        )  # matches any start of the section
        self.param_ptrn = re.compile(r'^\s+(?P<param>\w+):\s+(?P<doc>[\s\S]+)')

    def parse(self, doc: str) -> DocstringTp:
        lines = self.pattern.split(doc)
        long_desc = lines.pop(0)
        params = {}
        for lin in lines:
            param_doc, _ = self.section_ptrn.split(lin, maxsplit=1)
            match = self.param_ptrn.match(param_doc)
            if match:
                param, doc = match.groups()
                params[param] = ParamDocTp(None, *get_flags_from_param_doc(doc))

        return DocstringTp(long_desc, epilog='', params=params)


@functools.lru_cache(None)
def get_parsers():
    """Cache costly init phase per session."""
    return [cls() for cls in DocstringParser.__subclasses__()]


def parse_docstring(doc: Optional[str]) -> DocstringTp:
    if doc:
        for parser in get_parsers():
            if parser.matches(doc):
                return parser.parse(doc)
    return DocstringTp(description=doc, epilog='', params={})
