
from io import BytesIO, StringIO

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import pandas as pd


CALCULATE_EXCEL_URL = reverse('calculate-excel')


class CalculateExcelAPITests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        test_data = {
            'Unnamed: 1': ['', '', 1, 2, 3, 4, 5, 6],
            'Unnamed: 2': ['', 'Test', 'test', 't', 't', '', 't', ''],
            'name': ['Anna', 'Tom', 'Mark', 'Alice', 'Michelle', 'George', 'Sophia', 'Alex'],
            'age': [26, 27, 42, 34, 39, 60, 42, 28],
            'Unnamed: 3': ['', '', '', '', '', '', '', ''],
            'Unnamed: 4': [None, 'product', 'qwerty', 'asdf', 'zxcv', 'zz1', 'zz2', 'zz3'],
            'Unnamed: 5': ['', 'price', 29.99, 10, 5.49, 5, 100, 3.21],
            'Unnamed: 6': ['', '', 'aaa bbb c', '', '', 'Dd', '', '']
        }
        test_df = pd.DataFrame(test_data)
        self.excel_file_io = BytesIO()
        with pd.ExcelWriter(self.excel_file_io) as writer:
            test_df.to_excel(writer, engine='xlsxwriter')
        self.excel_file_io.name = 'test_excel_file.xlsx'
        self.excel_file_io.size = self.excel_file_io.getbuffer().nbytes
        self.excel_file_io.seek(0)

    def test_calculate_excel_file(self):
        payload = {
            "file": (self.excel_file_io.name, self.excel_file_io),
            "columns": ['["age", "price"]']
        }
        response = self.client.post(CALCULATE_EXCEL_URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file'], self.excel_file_io.name)
        self.assertEqual(len(response.data['summary']), 2)
        self.assertEqual(response.data['summary'][0]['column'], 'age')
        self.assertEqual(response.data['summary'][0]['sum'], 298)
        self.assertEqual(response.data['summary'][0]['avg'], 37.25)
        self.assertEqual(response.data['summary'][1]['column'], 'price')
        self.assertEqual(response.data['summary'][1]['sum'], 153.69)
        self.assertEqual(response.data['summary'][1]['avg'], 25.62)

    def test_calculate_excel_file_wrong_column_list(self):
        payload = {
            "file": (self.excel_file_io.name, self.excel_file_io),
            "columns": ['["test1", "test2"]']
        }
        response = self.client.post(CALCULATE_EXCEL_URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file'], self.excel_file_io.name)
        self.assertEqual(len(response.data['summary']), 0)

    def test_calculate_excel_file_no_column_list(self):
        payload = {
            "file": (self.excel_file_io.name, self.excel_file_io)
        }
        response = self.client.post(CALCULATE_EXCEL_URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data.keys())

    def test_calculate_excel_file_no_excel_file(self):
        payload = {
            "columns": ['["age", "price"]']
        }
        response = self.client.post(CALCULATE_EXCEL_URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data.keys())

    def test_calculate_excel_file_with_wrong_file_type(self):
        test_wrong_file = StringIO("Lorem ipsum, test test test. ")
        test_wrong_file.name = "Testing.txt"
        test_wrong_file.seek(0)
        payload = {
            "file": (test_wrong_file.name, test_wrong_file),
            "columns": ['["age", "price"]']
        }
        response = self.client.post(CALCULATE_EXCEL_URL, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data.keys())
