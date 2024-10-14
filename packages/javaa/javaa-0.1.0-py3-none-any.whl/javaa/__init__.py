# __init__.py for the javax package

# Import functions or classes to be exposed at package level
from .main import hello_javax

# Package-level metadata
__version__ = "0.1.0"


# Optionally, define functions here that are directly accessible
def greet():
    return "Greetings from javax!"
