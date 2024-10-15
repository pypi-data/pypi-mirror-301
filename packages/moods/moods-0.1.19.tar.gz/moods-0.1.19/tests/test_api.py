"""
Test the Moodle API
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

from unittest import mock
from hypothesis import given, strategies as st

from moodle.api import MoodleSession
from moodle.moodle import (
    MoodleSiteInfo,
    MoodleUserPreferences,
    MoodlePrivateFilesInfo
)


API_URL = "https://moodle.example.org/api/v{version}"


@given(model=st.from_type(MoodleSiteInfo))
def test_core_webservice_get_site_info(model):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = model.model_dump()
        s = MoodleSession(API_URL, token='')
        assert s.core_webservice_get_site_info() == model

@given(model=st.from_type(MoodlePrivateFilesInfo))
def test_core_user_get_private_files_info(model):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = model.model_dump()
        s = MoodleSession(API_URL, token='')
        assert s.core_user_get_private_files_info() == model

@given(model=st.from_type(MoodleUserPreferences))
def test_core_user_get_user_preferences(model):
    with mock.patch('pytest_tiny_api_client._api_call') as api_call:
        api_call.return_value = model.model_dump()
        s = MoodleSession(API_URL, token='')
        assert s.core_user_get_user_preferences() == model
