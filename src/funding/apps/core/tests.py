from django.test import TestCase
from funding.apps.core.views.response import HttpStatus, GenericResponse
from .components import date


class CoreViewTests(TestCase):
    def test_response_HttpStatus(self):
        http = HttpStatus(200, 'SUCCESS')
        self.assertEqual(http.code, 200)
        self.assertEqual(http.message, 'SUCCESS')
        self.assertRaises(ValueError, HttpStatus, code='invalid code', message="fail")

    def test_response_GenericResponse(self):
        color_data = {
            "color": "red"
        }
        response = GenericResponse(color_data, HttpStatus(
            200, "SUCCESS"
        ))
        self.assertEqual(
            response.data,
            {
                "code": 200,
                "status": "HTTP_200_OK",
                "message": "SUCCESS",
                "data": color_data
            }
        )
    
    def test_FinalDateComponent_str_validation(self):
        str_date = "2023-04-05"
        self.assertEqual(str(date.FinalDateComponent(str_date)), str_date)
        str_date = "1997-01-20"
        self.assertRaises(ValueError, date.FinalDateComponent, str_date=str_date)
        str_date = "3340,01,03"
        self.assertRaises(ValueError, date.FinalDateComponent, str_date=str_date)
