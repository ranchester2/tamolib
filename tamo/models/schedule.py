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
import bs4
from pathlib import Path
import json
import datetime
from .tamo_users import Teacher


class Lesson:
    """
    A lesson of a day

    Attributes:
        :num_in_day: value of type `int` of which lesson in the day is it
        :start: `datetime.datetime` object of when the lesson starts in the day
        :end: `datetime.datetime` object of when the lesson ends in the day
        :name: `str` of the full name of the lesson's subject.
        :teacher: TAMO `Teacher` object of who teaches the subject.
    """

    def __init__(
            self,
            dnumber: int,
            lesson_start: datetime.datetime,
            lesson_end: datetime.datetime,
            name: str,
            teacher: Teacher
    ):
        """
        Create a lesson object

        Parameters:
            :dnumber: `int` of which lesson of the day it is.
            :lesson_start: `datetime.datetime` object of
            when the lesson starts in the day.
            :lesson_end: `datetime.datetime` object of when
            when the lesson ends in the day.
            :name: `str` of full name of the lesson's subject.
            :teacher: TAMO `Teacher` object of who Teaches the subject.
        """
        self.num_in_day = dnumber
        self.start = lesson_start
        self.end = lesson_end
        self.name = name
        self.teacher = teacher


class SchoolDay:
    """
    A school day, contains lessons

    Attributes:
        :lessons: list of TAMO `Lesson` objects.
        :empty: whether the SchoolDay has no lessons.

    """

    def __init__(self, lessons=[], empty=False):
        """
        Create a school day

        :lessons: can be a list of Lesson objects, if not given
        you must add lessons after thefact with `SchoolDay.append_lesson`.
        :empty: whether the schoolday has no lessons.
        """

        # We need to do this instead of simply assigning, because otherwise
        # every time we create such an object, it gets its previous values.
        # I don't know why is this
        self.lessons = lessons[:]

        self.empty = empty

        # If the passed list is empty an error here is expected
        try:
            self.lessons.sort(key=lambda x: x.num_in_day)
        except:
            pass

    def append_lesson(self, lesson: Lesson):
        """
        Add a lesson to the schoolday

        :lesson: should be a TAMO `Lesson` object,
        
        You do not need to worry about the order
        as they will be sorted automatically if they
        are valid Lesson objects
        """
        self.lessons.append(lesson)

        # We want the list to always be sorted by time
        self.lessons.sort(key=lambda x: x.num_in_day)

    def __getitem__(self, item) -> Lesson:
        return self.lessons[item]


class Schedule:
    """
    A schedule object for TAMO.

    Attributes:
        :days: list of TAMO `SchoolDay` objects representing the Scheduled week.
    """

    def __init__(self, sched_div: bs4.element.Tag):
        """
        Create a Schedule object

        :shed_div: `bs4.element.Tag` of the outer div
        containing all schedule content.
        """
        self._sched_div = sched_div
        self._days = None

        # The number map let's us find out the number based
        # on the Lithuanian full word
        with open(Path(__file__).parents[1] / "tamo-data" / "number-map.json", 'r') as f:
            self._number_map = json.load(f)
            print(type(self._number_map))

    def _get_days(self):
        self._parse()
        return self._days

    def _parse(self):
        self._days = []

        all_unparsed_days = self._sched_div.find_all("table", class_="c_main_table full_width padless borderless wrap_text")

        for unparsed_day in all_unparsed_days:
            tmp_day = SchoolDay()

            unparsed_lessons_of_day = unparsed_day.find("tbody").find_all(recursive=False)

            for unparsed_lesson in unparsed_lessons_of_day:
                unparsed_lesson_children = unparsed_lesson.find_all(recursive=False)

                # We need to check wether there aren't any lessons
                if "Nėra pamokų" in unparsed_lesson_children[0].get_text(strip=True):
                    tmp_day.empty = True
                    continue

                # Second element is the number of the unparsed_lesson in the day
                tmp_lesson_number = self._number_map[unparsed_lesson_children[1].get_text(strip=True)]

                # Third element is the length of the unparsed_lesson formated like this:
                # %h%m - %h%m
                tmp_unparsed_lesson_start = (
                                                unparsed_lesson_children[2].get_text(strip=True))[:5]
                tmp_unparsed_lesson_end = (
                                              unparsed_lesson_children[2].get_text(strip=True))[-5:]

                tmp_lesson_start = datetime.datetime.strptime(
                    tmp_unparsed_lesson_start, "%H:%M")
                tmp_lesson_end = datetime.datetime.strptime(
                    tmp_unparsed_lesson_end, "%H:%M")

                # Fourth element is the full name of theunparsed_lesson
                tmp_lesson_name = unparsed_lesson_children[3].get_text(strip=True)

                # Fifth element is the full name of the Teacher
                tmp_lesson_teacher_name = unparsed_lesson_children[4].get_text(strip=True)

                # We first create the lesson object beforehand because otherwise it
                # doesn't work
                tmp_day.append_lesson(
                    Lesson(
                        tmp_lesson_number,
                        tmp_lesson_start,
                        tmp_lesson_end,
                        tmp_lesson_name,
                        Teacher(tmp_lesson_teacher_name)
                    )
                )

            self._days.append(tmp_day)

    @property
    def days(self) -> list:
        """
        List of days of the schedule

        :return: a list of SchoolDay objects
        """
        if self._days is None:
            return self._get_days()
        return self._days

    def __getitem__(self, item):
        return self.days[item]
