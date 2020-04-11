def _reprint(**kwargs):
    for param, value in sorted(kwargs.items()):
        print(f"{param} ({type(value)}): {value}")
