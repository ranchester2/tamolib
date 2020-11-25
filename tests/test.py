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
import json
import datetime


class LoginTest(unittest.TestCase):
    def setUp(self):
        load_dotenv(dotenv_path=Path("tests") / "secrets" / ".env")
        self.real_t = tamo.Tamo(
            os.environ["TAMO_USERNAME"], os.environ["TAMO_PASSWORD"])

        self.fake_t = tamo.Tamo("user", "password")

    def test_login(self):
        self.assertTrue(self.real_t.logged_in)
        self.assertFalse(self.fake_t.logged_in)

    def tearDown(self):
        self.real_t.close()
        self.fake_t.close()


class ScheduleTest(unittest.TestCase):
    def setUp(self):
        load_dotenv(dotenv_path=Path("tests") / "secrets" / ".env")

        with open(Path("tests") / "secrets" / "schedule.json") as f:
            self.real_schedule = json.load(f)

    def test_schedule(self):
        self.t = tamo.Tamo(
            os.environ["TAMO_USERNAME"], os.environ["TAMO_PASSWORD"])

        for didx, day in enumerate(self.t.schedule):
            self.assertEqual(
                day.empty,
                self.real_schedule[didx]["empty"]
            )
            for lidx, lesson in enumerate(day):
                self.assertEqual(
                    lesson.num_in_day,
                    self.real_schedule[didx]["lessons"][lidx]["num_in_day"]
                )
                self.assertEqual(
                    lesson.start,
                    datetime.datetime.strptime(
                        self.real_schedule[didx]["lessons"][lidx]["start"],
                        "%H:%M"
                    ),
                )
                self.assertEqual(
                    lesson.end,
                    datetime.datetime.strptime(
                        self.real_schedule[didx]["lessons"][lidx]["end"],
                        "%H:%M"
                    ),
                )
                self.assertEqual(
                    lesson.name,
                    self.real_schedule[didx]["lessons"][lidx]["name"]
                )

                
                self.assertEqual(
                    lesson.teacher.name,
                    self.real_schedule[didx]["lessons"][lidx]["teacher"]["name"]
                )
