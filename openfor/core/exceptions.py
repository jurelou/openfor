class OpenforException(Exception):
    """Base Openfor exceptions class."""

class InvalidExtractor(OpenforException):
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

    def __str__(self):
        return f'Invalid extractor definition for {self.name}: {self.reason}.'

class ExtractorNotFound(OpenforException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Extractor {self.name} not found.'
