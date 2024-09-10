import sys
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
import src.test.utils.utils as utils
from src.main.view.app import *
from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress

class TestUserAreaView(unittest.TestCase):
    app_test = app.test_client()
    app_test.testing = True

    """ Test modification_personal_data """

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_UA_SERVICE_MODIFICATION_PERSONAL_DATA)
    def test_modification_personal_data_success(self, mock_ua_service_modification_personal_data, 
                                                mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'profession_ru': "Data Science", 
            'num_cellphone_ru': "3344556677", 
            'email_ru': "new_email_80@test.test", 
            'password_ru': "new_PassWord_80", 
            'confirm_password_ru': "new_PassWord_80", 
            'name_ra': "Corso Mario Pagano", 
            'number_ra': 10, 
            'city_ra': "Roccapiemonte", 
            'province_ra': "SA", 
            'cap_ra': "84086",
            'id_ra': 10
        }
        mock_ua_service_modification_personal_data.return_value = {
            'success': True,
            'errors': {}, 
            'registered_user': RegisteredUser("new_email_80@test.test", "Mario", "Rossi", 'M', "05-10-1980", 
                                              "Torre del Greco", "Italia", "Italiana", "Data Science", "3344556677", 
                                              "new_PassWord_80", "new_PassWord_80", 20), 
            'residential_address': ResidentialAddress(20, "Corso Mario Pagano", 10, "Roccapiemonte", "SA", "84086"), 
            'id_ra': 20
        }
        result = self.app_test.post('/modification_personal_data', data=mock_utils_get_attributes_from_list_of_request.return_value)
        self.assertIn(b"<title>Dati personali</title>", result.data)
        self.assertEqual(mock_ua_service_modification_personal_data.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_UA_SERVICE_MODIFICATION_PERSONAL_DATA)
    def test_modification_personal_data_failure(self, mock_ua_service_modification_personal_data, 
                                                mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'profession_ru': "Data Science", 
            'num_cellphone_ru': "3344556677", 
            'email_ru': "new_email_80#test.test", 
            'password_ru': "new_PassWord_80", 
            'confirm_password_ru': "new_PassWord_80", 
            'name_ra': "Corso Mario Pagano", 
            'number_ra': 10, 
            'city_ra': "Roccapiemonte", 
            'province_ra': "SA", 
            'cap_ra': "84086",
            'id_ra': 10
        }
        mock_ua_service_modification_personal_data.return_value = {
            'success': False,
            'errors': {'email_ru': "L\'email inserita non è valida.\n"}, 
            'registered_user': RegisteredUser("new_email_80#test.test", "Mario", "Rossi", 'M', "05-10-1980", 
                                              "Torre del Greco", "Italia", "Italiana", "Data Science", "3344556677", 
                                              "new_PassWord_80", "new_PassWord_80", 20), 
            'residential_address': ResidentialAddress(20, "Corso Mario Pagano", 10, "Roccapiemonte", "SA", "84086"), 
            'password': "new_PassWord_80", 
            'confirm_password': "new_PassWord_80", 
            'id_ra': 10
        }
        result = self.app_test.post('/modification_personal_data', data=mock_utils_get_attributes_from_list_of_request.return_value)
        self.assertIn(b"<title>Dati personali</title>", result.data)
        self.assertEqual(mock_ua_service_modification_personal_data.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_UA_SERVICE_MODIFICATION_PERSONAL_DATA)
    def test_modification_personal_data_none(self, mock_ua_service_modification_personal_data, 
                                                mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'profession_ru': "Data Science", 
            'num_cellphone_ru': "3344556677", 
            'email_ru': "new_email_80#test.test", 
            'password_ru': "new_PassWord_80", 
            'confirm_password_ru': "new_PassWord_80", 
            'name_ra': "Corso Mario Pagano", 
            'number_ra': 10, 
            'city_ra': "Roccapiemonte", 
            'province_ra': "SA", 
            'cap_ra': "84086",
            'id_ra': 10
        }
        mock_ua_service_modification_personal_data.return_value = {
            'success': None, 'error': "Errore durante la modifica dei dati personali."
        }
        result = self.app_test.post('/modification_personal_data', data=mock_utils_get_attributes_from_list_of_request.return_value)
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_ua_service_modification_personal_data.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    def run_tests(self):
        self.test_modification_personal_data_success()
        self.test_modification_personal_data_failure()
        self.test_modification_personal_data_none()





