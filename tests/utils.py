from collections import namedtuple


CaseT = namedtuple("Case", ["cmd", "out", "err", "haserr"],)


def Case(
    cmd, out="", err="", haserr=False,
):
    return CaseT(cmd, out, err, haserr)
