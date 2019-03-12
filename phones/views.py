'''
Implements the API for the phone book.

Contact data is retrieved from http://www.mocky.io/v2/581335f71000004204abaf83 on each request.

[From the problem setting, it was not fully clear to me, if this is a requirement or the idea was rather to save the
data to the database and to use the database for generating responses, but it seemed to me rather that calling the API
on each request is required.]

Repeated queries are handled as OR (e.g. ?name=name1&name=name2 returns contacts such that name1 OR name2 are parts
of their names). Empty queries are handled as missing.
'''

import json

import requests

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

QUERY_PARAM_MAP = {
    'name': 'name',
    'phone': 'phone_number',
    'address': 'address',
}


def check_query(contact, name, values_list):
    return any([value.lower() in contact[QUERY_PARAM_MAP[name]].lower() for value in values_list])


def filter_contacts(contacts, query_params):
    result = list()

    for contact in contacts:
        should_be_included = True

        for name, values_list in query_params.lists():
            if values_list:
                should_be_included = should_be_included and check_query(contact, name, values_list)

        if should_be_included:
            result.append(contact)

    return result


def get_data_from_api():
    response = requests.get(settings.EXTERNAL_PHONES_API_URL)
    return json.loads(response.text)['contacts']


class Phones(APIView):
    def get(self, request, format=None):
        contacts = get_data_from_api()
        data = filter_contacts(contacts, request.query_params)
        return Response(status=status.HTTP_200_OK, data=data)
