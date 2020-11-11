import functools
import inspect
import re
import typing as tp


class ParamDocTp(tp.NamedTuple):
    type_hint: tp.Any
    flags: tp.Tuple[str, ...]
    doc: str

    @classmethod
    def init(cls, type_hint: tp.Any, doc: str, flag_symbol='-'):
        """Parse flags defined in param's doc

        Examples:
            ''':param arg1: -a --arg this is the document'''
        """
        doc_parts: tp.List[str] = []
        flags: tp.List[str] = []
        for part in doc.split():
            if part.startswith(flag_symbol) and not doc_parts:
                # strip both comma and empty space
                flags.append(part.strip(", ").strip())
            else:
                doc_parts.append(part)

        return cls(type_hint, flags=tuple(flags), doc=" ".join(doc_parts))


class DocstringTp(tp.NamedTuple):
    description: str
    epilog: str
    params: tp.Dict[str, ParamDocTp]


class DocstringParser:
    """Abstract class"""

    pattern: tp.Pattern
    section_ptrn: tp.Pattern
    param_ptrn: tp.Pattern

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
        self.param_ptrn = re.compile(r'^(?P<param>\w+)[ \t]*:?[ \t]*(?P<type>\w+)?')

    def get_rest_of_section(self, params: str) -> tp.Tuple[str, str]:
        other_sect = self.section_ptrn.search(params)
        if other_sect:
            pos = other_sect.start()
            return params[pos:].strip(), params[:pos]
        return '', params

    def parse_params(self, params: str) -> tp.Dict[str, ParamDocTp]:
        docs = []
        for line in params.splitlines():
            match = self.param_ptrn.search(line)
            if match:
                result = match.groupdict()
                doc = result.get('doc', '')
                docs.append([result['param'], result['type'], doc])
            elif docs:
                docs[-1][-1] += line

        return {
            param.strip('*'): ParamDocTp.init(tphint, doc)
            for param, tphint, doc in docs
        }

    def parse(self, doc: str) -> DocstringTp:
        desc, _, params = self.pattern.split(doc, maxsplit=1)
        other_sect, params = self.get_rest_of_section(params)
        return DocstringTp(desc.strip(), other_sect, params=self.parse_params(params))


class GoogleDocParser(NumpyDocParser):
    """Implement Google Docstring format parser
    `Example <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_
    """

    def __init__(self):  # pylint: disable=super-init-not-called
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
        self.section_ptrn = re.compile(r'\n:[\w]+')  # matches any start of the section
        self.param_ptrn = re.compile(r'^[ ]+(?P<tp_param>.+):[ ]*(?P<doc>[\s\S]+)')

    def parse_doc(self, line: str, params: tp.Dict[str, ParamDocTp]):
        match = self.param_ptrn.match(line)
        if match:
            tp_param, doc = match.groups()  # type: str, str
            parts = tp_param.strip().rsplit(' ', maxsplit=1)
            param = parts[-1].strip()
            type_hint = None
            if len(parts) > 1:
                type_hint = parts[0].strip()
            params[param] = ParamDocTp.init(type_hint, doc)

    def parse(self, doc: str) -> DocstringTp:
        lines = self.pattern.split(doc)
        long_desc = lines.pop(0)
        epilog = ''
        params: tp.Dict[str, ParamDocTp] = {}
        for idx, lin in enumerate(lines):
            sections = self.section_ptrn.split(lin, maxsplit=1)
            if idx + 1 == len(lines) and len(sections) > 1:
                epilog = sections[-1]
            self.parse_doc(sections[0], params)

        return DocstringTp(long_desc.strip(), epilog, params)


@functools.lru_cache(None)
def _docstring_parsers():
    """Cache costly init phase per session."""
    return [NumpyDocParser(), GoogleDocParser(), RstDocParser()]


def parse_docstring(func: tp.Optional[tp.Callable]) -> DocstringTp:
    doc = (inspect.getdoc(func) or '') if func else ''
    if doc:
        for parser in _docstring_parsers():
            if parser.matches(doc):
                return parser.parse(doc)
    return DocstringTp(description=doc, epilog='', params={})
