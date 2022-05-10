from django.test import TestCase
from funding.apps.core.views.response import HttpStatus, GenericResponse
from .utils import date, money


class CoreViewTests(TestCase):
    def test_response_HttpStatus(self):
        http = HttpStatus(200, 'SUCCESS')
        self.assertEqual(http.code, 200)
        self.assertEqual(http.message, 'SUCCESS')
        self.assertEqual(HttpStatus(800, message="fail").status, None)

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
    

class CoreComponentsTests(TestCase):
    def test_DateComponent_str_validation(self):
        str_date = "2023-04-05"
        self.assertEqual(str(date.DateComponent(str_date)), str_date)
        str_date = "1997-01-20"
        self.assertEqual(date.DateComponent(str_date).compare_of(date.get_today()), -1)
        str_date = "3340,01,03"
        self.assertRaises(ValueError, date.DateComponent, value=str_date)
    
    def test_DateComponent_get_d_day(self):
        now_date = "2022-05-02"
        str_date = "2022-05-05"
        
        target = date.DateComponent(str_date)
        now = date.DateComponent(now_date)

        self.assertEqual((target.as_date()-now.as_date()).days, 3)
    
    def test_Money(self):
        self.assertRaises(ValueError, money.money, value=9)
        self.assertEqual(str(money.money(19500)), '19,500')
