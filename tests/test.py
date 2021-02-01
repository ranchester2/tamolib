# This file is part of tamolib
# Copyright (C) 2021
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

import datetime
import json
import os
import unittest

from dotenv import load_dotenv
from pathlib import Path

import tamo


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

        self.t = tamo.Tamo(
            os.environ["TAMO_USERNAME"], os.environ["TAMO_PASSWORD"])

    def tearDown(self):
        # To not get warnings in tests about unclosed sockets
        self.t.close()

    def test_schedule(self):
        self.assertNotEqual(len(self.t.schedule), 0)
        for didx, day in enumerate(self.t.schedule):
            # We only test the first 3 days and the last because I can't be bothered to write
            # the schedule.json for the rest of them.
            if didx > 2 and didx != 6:
                continue

            self.assertEqual(
                day.empty,
                self.real_schedule[didx]["empty"]
            )

            if day.empty:
                break
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
                    )
                )
                self.assertEqual(
                    lesson.name,
                    self.real_schedule[didx]["lessons"][lidx]["name"]
                )

                self.assertEqual(
                    lesson.teacher.name,
                    self.real_schedule[didx]["lessons"][lidx]["teacher"]["name"]
                )
