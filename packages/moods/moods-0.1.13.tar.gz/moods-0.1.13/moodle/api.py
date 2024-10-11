"""
Moodle API

an interface to make Moodle REST API calls on a session basis.
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

from tiny_api_client import api_client, get

from .moodle import (
    MoodleToken,
    MoodleSiteInfo,
    MoodleCourse,
    MoodlePrivateFilesInfo,
    MoodleUserPreferences,
    MoodleResource,
    MoodleSection
)

from .exceptions import status_handler

_logger = logging.getLogger(__name__)


@api_client(timeout=15, status_handler=status_handler, status_key='errorcode')
class MoodleLogin:
    def __init__(self, url: str, *, username: str, password: str):
        endpoint = "/login/token.php?"
        query = f"username={username}&password={password}&service="
        self._url = url.rstrip("/") + endpoint + query

    @get("moodle_mobile_app")
    def login(self, response: Any) -> str:
        return MoodleToken(**response).token


@api_client(timeout=12, status_handler=status_handler, status_key='errorcode')
class MoodleSession:
    """Represents a user session in Moodle."""

    def __init__(self, url: str, *, token: str):
        """
        :param url: The URL of the Moodle API to use
        :param token: A valid API token
        """

        endpoint = "/webservice/rest/server.php?"
        query = f"wstoken={token}&moodlewsrestformat=json&wsfunction="

        self._instance_url = url
        self._url = url.rstrip("/") + endpoint + query
        self._token = token
        self._user_id: str | None = None

    @property
    def user_id(self) -> str:
        """User id field used for API requests."""
        if self._user_id is None:
            self._user_id = str(self.core_webservice_get_site_info().userid)
        return self._user_id

    @property
    def url(self) -> str:
        """API URL."""
        return self._url

    @property
    def instance_url(self) -> str:
        """Base URL of instance as provided."""
        return self._instance_url

    # API CALLS
    # https://docs.moodle.org/dev/Web_service_API_functions

    # core_webservice #

    @get("core_webservice_get_site_info")
    def core_webservice_get_site_info(self, response: Any
                                      ) -> MoodleSiteInfo:
        """Return some site info / user info / list web service functions."""
        return MoodleSiteInfo(**response)

    # core_course #

    @get("core_course_get_contents&courseid={course_id}")
    def core_course_get_contents(self, response: Any) -> list[MoodleSection]:
        return [MoodleSection(**section) for section in response]

    @get("core_course_get_courses")
    def core_course_get_courses(self, response: Any) -> list[MoodleCourse]:
        """Return course details."""
        return [MoodleCourse(**course) for course in response]

    # core_enrol #

    @get("core_enrol_get_users_courses&userid={user_id}")
    def core_enrol_get_users_courses(self, response: Any
                                     ) -> list[MoodleCourse]:
        """Get list of course ids that a user is enrolled in."""
        return [MoodleCourse(**course) for course in response]

    # core_files #

    @get("core_files_get_files")
    def core_files_get_files(self, response: Any) -> Any:
        """Browse moodle files."""
        return response

    # core_user #

    @get("core_user_get_private_files_info")
    def core_user_get_private_files_info(self, response: Any
                                         ) -> MoodlePrivateFilesInfo:
        """Information about files in the user private files area."""
        return MoodlePrivateFilesInfo(**response)

    @get("core_user_get_user_preferences")
    def core_user_get_user_preferences(self, response: Any
                                       ) -> MoodleUserPreferences:
        """Return user preferences."""
        return MoodleUserPreferences(**response)

    # mod_resource #

    @get("mod_resource_get_resources_by_courses")
    def mod_resource_get_resources_by_courses(self, response: Any
                                              ) -> list[MoodleResource]:
        return [MoodleResource(**res) for res in response['resources']]

    # download #

    def download(self, **kwargs: str) -> Any:
        """Download content from a given url (attachment_id)."""

        @get("{attachment_id}", json=False,
             stream=True, use_api=False)
        def _download(self: Any, response: Any) -> Any:
            return response

        return _download(self,
                         params={'token': self._token},
                         **kwargs)  # type: ignore
