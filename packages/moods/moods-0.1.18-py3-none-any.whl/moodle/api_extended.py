"""
Moodle API Extended.

an extension of the Moodle REST API
"""

# Copyright (C) 2024, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

import logging
from typing import Any

from .moodle import MoodleCourse, MoodleSection
from .api import MoodleSession

logger = logging.getLogger(__name__)


class MoodleExtended(MoodleSession):
    """An extension of `MoodleSession` with QOL improvements.
    These extensions may be combining two or more steps into one when
    fetching data from the API, or filtering results.
    """

    def ex_fetch_courses(self, *,
                         result_filter: Any = None,
                         **kwargs: Any) -> list[MoodleCourse]:
        """Fetch all the user's courses and their details"""
        courses = self.core_enrol_get_users_courses(**kwargs)
        return courses

    def fetch_contents(self, **kwargs: str) -> list[MoodleSection]:
        return self.core_course_get_contents(**kwargs)
