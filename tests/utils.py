def _reprint(**kwargs):
    for param, value in kwargs.items():
        print(f"{param} ({type(value)}): {value}")
