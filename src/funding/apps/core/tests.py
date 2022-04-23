from django.test import TestCase
from funding.apps.core.views.response import HttpStatus, GenericResponse


class CoreViewTests(TestCase):
    def test_response_HttpStatus(self):
        http = HttpStatus(200, 'SUCCESS')
        self.assertEqual(http.code, 200)
        self.assertEqual(http.message, 'SUCCESS')
        self.assertRaises(ValueError, HttpStatus, code='invalid code', message="fail")

    def test_response_InheritedResponse(self):
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
