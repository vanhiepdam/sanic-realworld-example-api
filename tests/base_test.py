# -*- coding: utf-8 -*-
import unittest

from app.bootstrap import create_app
from app.config import TestConfig


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig())
