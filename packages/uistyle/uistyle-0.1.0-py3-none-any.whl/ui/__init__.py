# __init__.py - Exposes UI functionalities of MyConsoleUI package

from .ui import MyConsoleUI

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

# Optional: Automatically initialize colorama (for colored console output)
from colorama import init

init(autoreset=True)  # Ensures colors reset after each print to prevent leaks

__all__ = ["MyConsoleUI"]  # Defines what gets imported with `from myconsoleui import *`
