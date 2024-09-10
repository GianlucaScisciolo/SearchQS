import sys
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
import src.test.utils.utils as utils
from src.main.view.app import *

class TestAuthenticationView(unittest.TestCase):
    app_test = app.test_client()
    app_test.testing = True

    """ Test registration """

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_A_SERVICE_REGISTRATION)
    def test_registration_success(self, mock_a_service_registration, mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'name_ru': "Mario", 
            'surname_ru': "Rossi", 
            'gender_ru': "M", 
            'birthdate_ru': "05-10-1980", 
            'city_birthplace_ru': "Torre del Greco", 
            'nation_birthplace_ru': "Italia", 
            'nationality_ru': "Italiana", 
            'profession_ru': "Computer Science", 
            'num_cellphone_ru': "3334445556", 
            'email_ru': "mr_80@test.test", 
            'password_ru': "mr_PassWord_80", 
            'confirm_password_ru': "mr_PassWord_80", 
            'name_ra': "Corso Mario Pagano", 
            'number_ra': 86, 
            'city_ra': "Roccapiemonte", 
            'province_ra': "SA", 
            'cap_ra': "84086"
        }
        mock_a_service_registration.return_value = {'success': True, 'errors': {}}
        result = self.app_test.post('/registration', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        self.assertIn(b"<title>Login</title>", result.data)
        self.assertEqual(mock_a_service_registration.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_A_SERVICE_REGISTRATION)
    def test_registration_success_failure(self, mock_a_service_registration, mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'name_ru': "Mario", 
            'surname_ru': "Rossi", 
            'gender_ru': "M", 
            'birthdate_ru': "05-10-1980", 
            'city_birthplace_ru': "Torre del Greco", 
            'nation_birthplace_ru': "Italia", 
            'nationality_ru': "Italiana", 
            'profession_ru': "Computer Science", 
            'num_cellphone_ru': "3334445556", 
            'email_ru': "mr_80#test.test", 
            'password_ru': "mr_PassWord_80", 
            'confirm_password_ru': "mr_PassWord_80", 
            'name_ra': "Corso Mario Pagano", 
            'number_ra': 86, 
            'city_ra': "Roccapiemonte", 
            'province_ra': "SA", 
            'cap_ra': "84086"
        }
        mock_a_service_registration.return_value = {'success': False, "errors": {'email_ru': "Email inserita non valida.\n"}}
        result = self.app_test.post('/registration', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        self.assertIn(b"<title>Registrazione</title>", result.data)
        self.assertEqual(mock_a_service_registration.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_A_SERVICE_REGISTRATION)
    def test_registration_success_none(self, mock_a_service_registration, mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'name_ru': "Mario", 
            'surname_ru': "Rossi", 
            'gender_ru': "M", 
            'birthdate_ru': "05-10-1980", 
            'city_birthplace_ru': "Torre del Greco", 
            'nation_birthplace_ru': "Italia", 
            'nationality_ru': "Italiana", 
            'profession_ru': "Computer Science", 
            'num_cellphone_ru': "3334445556", 
            'email_ru': "mr_80@test.test", 
            'password_ru': "mr_PassWord_80", 
            'confirm_password_ru': "mr_PassWord_80", 
            'name_ra': "Corso Mario Pagano", 
            'number_ra': 86, 
            'city_ra': "Roccapiemonte", 
            'province_ra': "SA", 
            'cap_ra': "84086"
        }
        mock_a_service_registration.return_value = {'success': None}
        result = self.app_test.post('/registration', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_a_service_registration.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    """ Test login """

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_A_SERVICE_LOGIN)
    def test_login_success(self, mock_a_service_login, mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            "email_ru": "mr_80@test.test",
            "password_ru": "mr_PassWord_80"
        }
        mock_a_service_login.return_value = {'success': True, 'errors': {}}
        result = self.app_test.post('/login', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        
        self.assertIn(b"<title>Home page</title>", result.data)
        self.assertEqual(mock_a_service_login.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_A_SERVICE_LOGIN)
    def test_login_failure(self, mock_a_service_login, mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            "email_ru": "mr_80#test.test",
            "password_ru": "mr_PassWord_80"
        }
        mock_a_service_login.return_value = {'success': False, 'errors': {'email_ru': "Email inserita non valida.\n"}}
        result = self.app_test.post('/login', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        
        self.assertIn(b"<title>Login</title>", result.data)
        self.assertEqual(mock_a_service_login.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_A_SERVICE_LOGIN)
    def test_login_none(self, mock_a_service_login, mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            "email_ru": "mr_80#test.test",
            "password_ru": "mr_PassWord_80"
        }
        mock_a_service_login.return_value = {'success': None}
        result = self.app_test.post('/login', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_a_service_login.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    def run_tests(self):
        self.test_registration_success()
        self.test_registration_success_failure()
        self.test_registration_success_none()
        self.test_login_success()
        self.test_login_failure()
        self.test_login_none()









