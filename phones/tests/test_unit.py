from django.http.request import QueryDict

from django.test import TestCase

from phones.views import check_query, filter_contacts

test_data = [
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


class UnitTest(TestCase):
    def test_check_query(self):
        contact_1 = {
            'name': 'Name',
            'phone_number': '4444',
            'address': 'some address',
        }

        contact_2 = {
            'name': 'name',
            'phone_number': '4444',
            'address': 'some address',
        }

        self.assertTrue(check_query(contact_1, 'name', 'nam'))
        self.assertTrue(check_query(contact_2, 'name', 'Nam'))
        self.assertFalse(check_query(contact_2, 'name', 'smth'))
        self.assertTrue(check_query(contact_1, 'phone', '44'))
        self.assertFalse(check_query(contact_1, 'phone', '3333'))
        self.assertTrue(check_query(contact_1, 'address', 'OMe'))
        self.assertFalse(check_query(contact_1, 'address', 'someaddress'))

    def test_filter_contacts(self):
        query_params = QueryDict('name=Test One')
        self.assertEqual([
            {
                'name': 'Test One',
                'phone_number': '1',
                'address': 'first address',
            }], filter_contacts(test_data, query_params))

        query_params = QueryDict('name=')
        self.assertEqual(test_data, filter_contacts(test_data, query_params))

        query_params = QueryDict('phone=2')
        self.assertEqual([
            {
                'name': 'Test Two',
                'phone_number': '2',
                'address': 'second address',
            }], filter_contacts(test_data, query_params))

        query_params = QueryDict('address=first address')
        self.assertEqual([
            {
                'name': 'Test One',
                'phone_number': '1',
                'address': 'first address',
            },
            {
                'name': 'Test Three',
                'phone_number': '3',
                'address': 'first address',
            }], filter_contacts(test_data, query_params))

        query_params = QueryDict('phone=2&address=first address')
        self.assertEqual([], filter_contacts(test_data, query_params))
