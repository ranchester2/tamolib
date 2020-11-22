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

class User:
    """
    A base TAMO user, currently mostly useless

    Attributes:
        :name: full `str` name of the user
    """

    def __init__(self, name: str):
        """
        Create a TAMO user

        Arguments:
            :name: full `str` name of the user
        """
        self.name = name

class Teacher(User):
    """
    A Teacher in TAMO, currently mostly useless

    Attributes:
        :name: full `str` name of the teacher
    """

    def __init__(self, name):
        """
        Create a TAMO teacher

        Arguments:
            :name: full `str` name of the teacher
        """
        super().__init__(name)