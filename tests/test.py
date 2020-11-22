# This file is part of tamolib
# Copyright (C) 2020
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import tamo
import unittest
from dotenv import load_dotenv
from pathlib import Path
import os


class LoginTest(unittest.TestCase):
    def setUp(self):
        load_dotenv(dotenv_path=Path("tests") / "secrets" / ".env")
        self.real_t = tamo.Tamo(os.environ["TAMO_USERNAME"], os.environ["TAMO_PASSWORD"])

        self.fake_t = tamo.Tamo("user", "password")

    def test_login(self):
        self.assertTrue(self.real_t.logged_in)
        self.assertFalse(self.fake_t.logged_in)

    def tearDown(self):
        self.real_t.close()
        self.fake_t.close()
