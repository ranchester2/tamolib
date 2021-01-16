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

import bs4
from pathlib import Path

from .tamo_users import Teacher


class Lesson:
    """
    A lesson of a day.

    Attributes:
        :num_in_day: `int` of which lesson in the day is it/
            NOTE: uses IRL naming scheme.
        :start: `datetime.datetime` of when the lesson starts in the day
        :end: `datetime.datetime` of when the lesson ends in the day
        :name: `str` of the full name of the lesson's subject.
        :teacher: `tamo.models.Teacher` of who teaches the subject.
    """

    def __init__(
            self,
            num_in_day: int,
            lesson_start: datetime.datetime,
            lesson_end: datetime.datetime,
            name: str,
            teacher: Teacher
    ):
        """
        Create a lesson object.

        Parameters:
            :num_in_day: `int` of which lesson of the day it is.
                NOTE: uses IRL naming scheme.
            :lesson_start: `datetime.datetime` of
            when the lesson starts in the day.
            :lesson_end: `datetime.datetime` of when
            when the lesson ends in the day.
            :name: `str` of full name of the lesson's subject.
            :teacher: `tamo.models.Teacher` of who Teaches the subject.
        """
        self.num_in_day = num_in_day
        self.start = lesson_start
        self.end = lesson_end
        self.name = name
        self.teacher = teacher


class SchoolDay:
    """
    A school day, contains lessons.

    Attributes:
        :empty: whether the SchoolDay has no lessons.

    Iterate:
        Iterate through the lessons of the day, type `tamo.models.Lesson`,
        does not exist if attribute :emtpy: is `True`

    """

    def __init__(self, lessons=None, empty=False):
        """
        Create a school day.

        :lessons: can be a list of `tamo.models.Lesson` objects, if not given
        you must add lessons after the fact with `SchoolDay.append_lesson`.
        :empty: whether the schoolday has no lessons.
        """

        # We need to do this instead of simply assigning, because otherwise
        # every time we create such an object, it gets its previous values.
        # ~~I don't know why is this~~

        # Update: the reason is https://www.reddit.com/r/learnpython/comments/apsplq/what_are_some_bad_habits_to_avoid/egbgqnf/
        # (last point). This was soooo frustrating for me. See commit
        # history for what was the issue before
        if lessons is None:
            self._lessons = []
        else:
        # I don't know if I actually need this line, and according to
        # the above linked reddit comment its not super clear,
        # however I will still leave it in.
            self._lessons = lessons[:]

        self.empty = empty

        # If the passed list is empty an error here is expected
        try:
            self._lessons.sort(key=lambda x: x.num_in_day)
        except:
            pass

    def append_lesson(self, lesson: Lesson):
        """
        Add a lesson to the schoolday.

        Arguments:
            :lesson:`tamo.models.Lesson` of the lesson that you want to add.

        NOTE:
            You do not need to worry about the order
            as they will be sorted automatically if they
            are valid Lesson objects
        """
        self._lessons.append(lesson)

        # We want the list to always be sorted
        self._lessons.sort(key=lambda x: x.num_in_day)

    def __getitem__(self, item) -> Lesson:
        return self._lessons[item]

    def __len__(self):
        return len(self._lessons)


class Schedule:
    """
    A schedule object for TAMO.

    Iterate:
        Iterate through the lessons of the day, behaves like list.
        All are `tamo.models.SchoolDay` objects.
    """

    def __init__(self, sched_div: bs4.element.Tag):
        """
        Create a Schedule object

        :shed_div: `bs4.element.Tag` of the outer div
        containing all schedule content.
        """
        self._sched_div = sched_div
        self.__days = None

        # The number map let's us find out the number based
        # on the Lithuanian full word
        with open(Path(__file__).parents[1] / "tamo-data" / "number-map.json", 'r') as f:
            self._number_map = json.load(f)

    def _get_days(self):
        self._parse()
        return self.__days

    # This could probably be integrated directly
    # into _get_days() instead.
    def _parse(self):
        self.__days = []

        all_unparsed_days = self._sched_div.find_all("table",
                                                     class_="c_main_table full_width padless borderless wrap_text")

        for unparsed_day in all_unparsed_days:
            tmp_day = SchoolDay()

            unparsed_lessons_of_day = unparsed_day.find("tbody").find_all(recursive=False)

            for unparsed_lesson in unparsed_lessons_of_day:
                unparsed_lesson_children = unparsed_lesson.find_all(recursive=False)

                # "Nera pamoku" means the day has no lessons
                if "Nėra pamokų" in unparsed_lesson_children[0].get_text(strip=True):
                    tmp_day.empty = True
                    continue

                # Second element is the number of the unparsed_lesson in the day
                tmp_lesson_number = self._number_map[unparsed_lesson_children[1].get_text(strip=True)]

                # Third element is the length of the unparsed_lesson formatted like this:
                # %h%m - %h%m
                tmp_unparsed_lesson_start = (unparsed_lesson_children[2].get_text(strip=True))[:5]
                tmp_unparsed_lesson_end = (unparsed_lesson_children[2].get_text(strip=True))[-5:]

                tmp_lesson_start = datetime.datetime.strptime(
                    tmp_unparsed_lesson_start, "%H:%M")
                tmp_lesson_end = datetime.datetime.strptime(
                    tmp_unparsed_lesson_end, "%H:%M")

                # Fourth element is the full name of the unparsed_lesson
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

            self.__days.append(tmp_day)

    # Private because we don't need that as we
    # use special methods instead, however we still
    # want this as a dynamically loaded property
    # for caching and performance.
    @property
    def _days(self) -> list:
        """
        List of days of the schedule

        :return: a list of SchoolDay objects
        """

        # Double underscore seams weird, however I don't know
        # how to handle this any better, since we want to use a cached
        # property, however _days is already the name of the property
        if self.__days is None:
            return self._get_days()
        return self.__days

    def __len__(self):
        return len(self._days)

    def __getitem__(self, item):
        return self._days[item]
