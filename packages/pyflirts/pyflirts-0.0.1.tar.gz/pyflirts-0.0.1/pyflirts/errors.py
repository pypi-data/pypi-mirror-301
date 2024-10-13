class PyflirtsError(Exception):
    "main class for all pyflirts exceptions"

class LanguageNotFoundError(PyflirtsError):
    pass

class CategoryNotFoundError(PyflirtsError):
    pass
