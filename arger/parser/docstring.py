from typing import Optional

from docstring_parser import parse


#
# def parse_docstring(doc: Optional[str]):
#     param_docs = {}
#     desc = ""
#     if doc:
#         param_doc = doc.split(':param')
#         desc = param_doc.pop(0).strip()
#         for param in param_doc:
#             param_args = param.split()
#             variable_name = param_args.pop(0)[:-1]
#             param_docs[variable_name] = param_args
#     return desc, param_docs


def parse_docstring(doc: Optional[str]):
    if doc:
        parsed = parse(doc)
        params = {arg.arg_name: arg.description for arg in parsed.params}
        params = {k: val.replace("\n", " ") for k, val in params.items()}
        return (
            "\n".join(
                (
                    desc
                    for desc in (parsed.short_description, parsed.long_description)
                    if desc
                )
            ),
            params,
        )
    return "", {}
