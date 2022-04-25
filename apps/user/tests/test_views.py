import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from datetime import datetime, timedelta

from apps.utils.tests.mixins import BaseAPITestCase
from apps.utils.tests.validators.auth_schemas import otp_schema


class AuthenticationTest(BaseAPITestCase):

    def test_get_otp_201(self):
        """
                Ensure we can get a new otp for authentication
        """

        url = reverse('get-otp')
        data = {'phone': '09380502542'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_otp_400(self):
        """
                Test get 400 on wrong number
        """

        url = reverse('get-otp')
        data = {'phone': '0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_otp_response_schema(self):
        """
               Test get otp response schema
        """

        url = reverse('get-otp')
        data = {'phone': '09380502542'}
        response = self.client.post(url, data, format='json')

        response = json.loads(response.content)
        self.check_response_schema(otp_schema, response)

