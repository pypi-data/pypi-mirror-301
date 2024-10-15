from injection.utils import load_packages

from . import services
from .test_case import HundredTestCase

__all__ = ("HundredTestCase",)

load_packages(services)
