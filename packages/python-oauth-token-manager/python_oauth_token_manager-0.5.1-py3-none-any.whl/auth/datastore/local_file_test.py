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

from auth import local_file
from google.oauth2 import credentials as oauth

from copy import deepcopy
from typing import Any, Dict

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


class LocalFileTest(unittest.TestCase):
  def setUp(self):
    self.open = mock.mock_open(read_data=json.dumps(MASTER_CONFIG))

  def test_get_document_with_key(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()
      self.assertEqual({'api_key': 'api_key'},
                       datastore.get_document('auth', 'api_key'))

  def test_get_document_without_key(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()
      self.assertEqual(MASTER_CONFIG,
                       datastore.get_document('auth'))

  def test_get_document_missing_type(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()
      self.assertEqual(None, datastore.get_document('10011'))

  def test_get_document_missing_id(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()
      self.assertEqual(None, datastore.get_document('10011'))

  def test_get_document_missing_key(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()
      self.assertEqual(None, datastore.get_document('auth', 'foo'))

  def test_store_new_document(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()
      datastore.store_document(id='0000', document={'id': '0000'})

      expected = deepcopy(MASTER_CONFIG)
      expected.update({'0000': {'id': '0000'}})
      self.open.assert_called_with('datastore.json', 'w')
      self.open().write.assert_called_with(json.dumps(expected, indent=2))

  def test_store_new_document_new_name(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile(
          datastore_file='new_datastore.json')
      datastore.store_document(id='0000', document={'id': '0000'})

      expected = deepcopy(MASTER_CONFIG)
      expected.update({'0000': {'id': '0000'}})
      self.open.assert_called_with('new_datastore.json', 'w')
      self.open().write.assert_called_with(json.dumps(expected, indent=2))

  def test_list_documents_all(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      _docs = datastore.list_documents()
      expected = MASTER_CONFIG
      self.assertDictEqual(expected, _docs)

  def test_list_documents_auth(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      _docs = datastore.list_documents('auth')
      expected = MASTER_CONFIG.get('auth')
      self.assertEqual(expected.keys(), _docs)

  def test_list_documents_none(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      _docs = datastore.list_documents('foo')
      self.assertIsNone(_docs)

  def test_get_all_documents(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      _docs = datastore.get_all_documents()
      expected = MASTER_CONFIG
      self.assertEqual(expected, _docs)

  def test_delete_document_collection(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      datastore.delete_document(id='auth')
      self.assertEqual({}, datastore.datastore)

  def test_delete_document_key(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      datastore.delete_document(
          id='auth', key='api_key')
      self.assertEqual({
          'auth': {'bHVrZUBza3l3YWxrZXIuY29t': {
              '_key': 'luke@skywalker.com',
              'access_token': 'access_token',
                              'refresh_token': 'refresh_token'}}},
          datastore.datastore)

  def test_delete_document_key_missing(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      datastore.delete_document(
          id='auth', key='foo')
      self.assertEqual(MASTER_CONFIG,
                       datastore.datastore)

  def test_update_document_existing(self):
    with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
      datastore = local_file.LocalFile()

      expected = {'api_key': 'new api key'}
      datastore.update_document(id='auth',
                                new_data=expected)
      self.open().write.assert_called_once()
      self.assertEqual(expected.get('api_key'),
                       datastore.datastore.get('auth').get('api_key'))

  # def test_with_credentials(self):
  #   token = {"token": "ya29.a0AfB_byDtQjjFnbUKnk-DgZx4tGlaOLZZXEB3bMjL8P7_IZ5WKUHgCPSBUqjI7ACbCclA850_7dnh8AoMBlt87TKNW7bRgDv5V6Dmvb7KZYycssnjal9gwA9dQuwqLEf5fr9SJ12-NHp6x51C_gP468NOprEfv4Av75mxiG0aCgYKASsSARASFQGOcNnCduSFEVw2dKa6RINZTWqHQA0174", "refresh_token": "1//0dRuCPZqlcv2CCgYIARAAGA0SNwF-L9Ir4S8NZWlFevdDXYFUvrTlEshsld0DTezlei_uScReK29aZHNsVMhM6tSW_ZtWHBVpzXs", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "2688500325-2ihs0lfm6luj60dc6uc34quf3fj6annp.apps.googleusercontent.com", "client_secret": "LajIs2mA_GE8lkmX6El6hbok", "expiry": "2023-10-12T19:30:11.273524Z"}
  #   creds = oauth.Credentials.from_authorized_user_info(token)

  #   with mock.patch(f'{CLASS_UNDER_TEST}.open', self.open):
  #     datastore = local_file.LocalFile()

  #     expected = {'api_key': 'new api key'}
  #     datastore.update_document(id='auth',
  #                               new_data=creds)
  #     self.open().write.assert_called_once()
  #     self.assertEqual(expected.get('api_key'),
  #                      datastore.datastore.get('auth').get('api_key'))
