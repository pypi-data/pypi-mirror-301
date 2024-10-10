"""Moodle REST API exceptions."""

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

from typing import Any, NoReturn


class MoodleAPIError(Exception):
    pass


class MoodleParameterError(MoodleAPIError):
    """Invalid parameter value detected."""
    pass


class MoodleTokenError(MoodleAPIError):
    """Invalid token - token not found."""
    pass


class MoodleContextError(MoodleAPIError):
    """You cannot execute functions in the course context."""
    pass


class MoodlePermissionsError(MoodleAPIError):
    """Sorry, but you do not currently have permissions to do that."""
    pass


def status_handler(client: Any, status_code: Any, response: Any) -> NoReturn:
    match status_code:
        case "invalidparameter":
            raise MoodleParameterError(response)
        case "invalidtoken":
            raise MoodleTokenError(response)
        case "errorcoursecontextnotvalid":
            raise MoodleContextError(response)
        case "nopermissions":
            raise MoodlePermissionsError(response)
        case _:
            raise MoodleAPIError(response)
