from django.test import TestCase
from funding.apps.core.views.response import HttpStatus, GenericResponse
from .utils import date, money, sorted_by


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
        self.assertRaises(ValueError, money.money, value=-1)
        self.assertEqual(money.money(19500).value_of(str), '19,500')
        self.assertEqual(money.money(20000).times(3).value_of(str), '60,000')
        self.assertRaises(ValueError, money.money(999999999).times, num=100)

        self.assertRaises(ValueError, money.money, value='4342.13')
        self.assertEqual(money.money('3,431,215').value_of(int), 3431215)
        self.assertRaises(ValueError, money.money, value='33,5678,345,333')
    
    def test_sort_func(self):
        # test cmp=compare test
        data = []
        for i in range(100):
            year = 1990+i%3
            if i==0:
                year = 2020
            element = {
                "name": f"name{i}",
                "age": 20+i,
                "birth": f'{year}-05-07'
            }
            data.append(element)

        from functools import cmp_to_key
        key = 'birth'
        cmp_key = cmp_to_key(lambda x, y: date.compare_date_from_data(x[key], y[key]))
        sorted_data = sorted(data, key=cmp_key)
        self.assertEqual(sorted_data[0]['name'], 'name3')
