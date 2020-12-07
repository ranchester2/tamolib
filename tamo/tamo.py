# This file is part of tamolib
# Copyright (C) 2020
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from bs4 import BeautifulSoup, SoupStrainer

from tamo.models import Schedule


class Tamo():
    """
    Interact with TAMO.

    Class designed for creating a Tamo session
    and using it to communicate with the online
    education platform.

    Attributes:
        :logged_in: `bool` of whether you have successfully authenticated and are logged in.
    """

    def __init__(self, username, password):
        """
        Create a Tamo session.

        :username: the username of your account.
        :password: the password of your account.
        """
        self._session = requests.Session()
        self.username = username
        self.password = password
        self._login()

        self._schedule = None
        self._real_name = None
        self._logged_in = None

    def _login(self):
        result = self._session.get(
            "https://dienynas.tamo.lt/Prisijungimas/Login")
        soup = BeautifulSoup(result.content, 'lxml')
        SToken = soup.find(attrs={"name": "SToken"})['value']
        timestamp = soup.find(attrs={"name": "Timestamp"})['value']
        payload = {
            'UserName': self.username,
            'Password': self.password,
            'IsMobileUser': 'false',
            'ReturnUrl': '',
            'RequireCaptcha': 'false',
            'Timestamp': timestamp,
            'SToken': SToken
        }

        self._session.post("https://dienynas.tamo.lt/", data=payload)

    @property
    def logged_in(self) -> bool:
        """Whether or not the session is logged in."""
        if self._logged_in is None:
            return self._check_logged_in()
        return self._logged_in

    def _check_logged_in(self):
        r = self._session.get("http://dienynas.tamo.lt/?clickMode=True")

        # We are redirected if we failed to login
        self._logged_in = (302 not in [response.status_code for response in r.history])
        return self._logged_in

    def close(self):
        """Close the connection with Tamo"""
        self._session.close()

    @property
    def schedule(self) -> Schedule:
        """
        Your account's lesson schedule.

        :type: `tamo.models.Schedule`
        """
        if self._schedule is None:
            return self._get_schedule()
        return self._schedule

    def _get_schedule(self):
        r = self._session.post(
            "https://dienynas.tamo.lt/TvarkarascioIrasas/MokinioTvarkarastis")

        soup = BeautifulSoup(r.text, "lxml")

        # c_main is the id that the schedule div uses
        schedule_div = soup.find("div", {"id": "c_main"})
        schedule = Schedule(schedule_div)

        self._schedule = schedule
        return self._schedule
