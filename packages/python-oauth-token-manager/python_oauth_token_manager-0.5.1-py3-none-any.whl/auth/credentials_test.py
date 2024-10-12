# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import unittest
from unittest import mock

from auth.credentials_helpers import encode_key
from auth.exceptions import KeyEncodingError
from google.oauth2 import credentials as oauth
from auth.credentials import Credentials
from auth import local_file

MASTER_CONFIG = {
    "auth": {
        "api_key": "api_key",
        "bHVrZUBza3l3YWxrZXIuY29t": {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "_key": "luke@skywalker.com"
        },
    },
}

CLASS_UNDER_TEST = 'auth.local_file'


class CredentialsTest(unittest.TestCase):
  def setUp(self):
    self.open = mock.mock_open(read_data=json.dumps(MASTER_CONFIG))

  # def test_encode_valid(self) -> None:
  #   self.assertEqual('YnV0dGVyY3VwQGFzeW91d2lzaC5jb20',
  #                    encode_key('buttercup@asyouwish.com'))

  # def test_encode_none(self) -> None:
  #   with self.assertRaisesRegex(KeyEncodingError, 'Cannot encode None'):
  #     encode_key(None)

  def test_store_credentials_with_creds(self) -> None:
    token = {"token": "ya29.a0AfB_byDtQjjFnbUKnk-DgZx4tGlaOLZZXEB3bMjL8P7_IZ5WKUHgCPSBUqjI7ACbCclA850_7dnh8AoMBlt87TKNW7bRgDv5V6Dmvb7KZYycssnjal9gwA9dQuwqLEf5fr9SJ12-NHp6x51C_gP468NOprEfv4Av75mxiG0aCgYKASsSARASFQGOcNnCduSFEVw2dKa6RINZTWqHQA0174",
             "refresh_token": "1//0dRuCPZqlcv2CCgYIARAAGA0SNwF-L9Ir4S8NZWlFevdDXYFUvrTlEshsld0DTezlei_uScReK29aZHNsVMhM6tSW_ZtWHBVpzXs", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "2688500325-2ihs0lfm6luj60dc6uc34quf3fj6annp.apps.googleusercontent.com", "client_secret": "LajIs2mA_GE8lkmX6El6hbok", "expiry": "2023-10-12T19:30:11.273524Z"}
    creds = oauth.Credentials.from_authorized_user_info(token)

    c = Credentials(datastore=local_file.LocalFile,
                    email='inigo@princessbride.com')
    c.store_credentials(creds)

    print(c.datastore.list_documents())
