__all__ = ['LoginFailedException', 'NoElementException']


class LoginFailedException(Exception):
    """Raise when login failed"""

    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}


class NoElementException(Exception):
    """Raise when required elements cannot be found"""

    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}
