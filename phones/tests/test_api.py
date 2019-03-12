import json

from unittest.mock import patch, Mock

from django.conf import settings

from rest_framework.reverse import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class FakeResponse:
    def __init__(self, text):
        self.text = text


fake_data = [
    {
        'name': 'Test One',
        'phone_number': '1',
        'address': 'first address',
    },
    {
        'name': 'Test Two',
        'phone_number': '2',
        'address': 'second address',
    },
    {
        'name': 'Test Three',
        'phone_number': '3',
        'address': 'first address',
    },
]

fake_data_str = json.dumps(
    {
        "contacts": [
            {
                'name': 'Test One',
                'phone_number': '1',
                'address': 'first address',
            },
            {
                'name': 'Test Two',
                'phone_number': '2',
                'address': 'second address',
            },
            {
                'name': 'Test Three',
                'phone_number': '3',
                'address': 'first address',
            },
        ]
    }
)

mock_get_data_from_api = Mock()
mock_get_data_from_api.side_effect = lambda url: FakeResponse(fake_data_str)


class APITest(APITestCase):
    url = reverse('phones-api')

    def setUp(self) -> None:
        mock_get_data_from_api.reset_mock()

    @patch('requests.get', mock_get_data_from_api)
    def test_external_phones_api_is_called(self):
        self.client.get(self.url)
        mock_get_data_from_api.assert_called_once_with(settings.EXTERNAL_PHONES_API_URL)

    @patch('requests.get', mock_get_data_from_api)
    def test_api_returns_all_contacts_without_filters(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(fake_data, response.data)

    @patch('requests.get', mock_get_data_from_api)
    def test_api_returns_correct_filtered_results(self):
        url = f'{self.url}?name=Test One'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual('Test One', response.data[0]['name'])

        url = f'{self.url}?phone=2'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual('Test Two', response.data[0]['name'])

        url = f'{self.url}?address=first address'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

        for data in response.data:
            self.assertIn(data['name'], ['Test One', 'Test Three'])

    @patch('requests.get', mock_get_data_from_api)
    def test_api_returns_correct_filtered_results_with_multiple_values_for_same_query_parameter(self):
        url = f'{self.url}?name=Test One&name=Test Two'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

        for data in response.data:
            self.assertIn(data['name'], ['Test One', 'Test Two'])

    @patch('requests.get', mock_get_data_from_api)
    def test_api_works_with_empty_query_params(self):
        url = f'{self.url}?name='
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))
