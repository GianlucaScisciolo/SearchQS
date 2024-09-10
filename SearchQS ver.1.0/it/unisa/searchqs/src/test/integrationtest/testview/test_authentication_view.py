import sys

import mysql.connector
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
from src.main.view.app import *
import mysql
import src.test.utils.utils as utils

class TestITAuthenticationView(unittest.TestCase):
    def setUp(self):
        self.app_test = app.test_client()
        self.app_test.testing = True

    """ Test registration """
    def test_it_1_registration_success(self):
        data = {
            "name_ru": "Andrea",
            "surname_ru": "Verdi",
            "gender_ru": 'M',
            "birthdate_ru": "1970-05-03",
            "city_birthplace_ru": "Torre annunziata",
            "nation_birthplace_ru": "Italia", 
            "nationality_ru": "Italiana",
            "profession_ru": "",
            "num_cellphone_ru": "",
            "email_ru": "av_70@test.test",
            "password_ru": "av_PassWord_70",
            "name_ra": "Via Giuseppe Verdi",
            "number_ra": 40,
            "city_ra": "Napoli",
            "province_ra": "NA",
            "cap_ra": "80013",
            "confirm_password_ru": "av_PassWord_70"    
        }
        result = self.app_test.post('/registration', data=data)
        self.assertIn(b"<title>Login</title>", result.data) 

    def test_it_2_registration_failure(self):
        data = {
            "name_ru": "Andrea",
            "surname_ru": "Verdi",
            "gender_ru": 'M',
            "birthdate_ru": "1970-05-03",
            "city_birthplace_ru": "Torre annunziata",
            "nation_birthplace_ru": "Italia", 
            "nationality_ru": "Italiana",
            "profession_ru": "",
            "num_cellphone_ru": "",
            "email_ru": "av_70#test.test",
            "password_ru": "av_PassWord_70",
            "name_ra": "Via Giuseppe Verdi",
            "number_ra": 40,
            "city_ra": "Napoli",
            "province_ra": "NA",
            "cap_ra": "80013",
            "confirm_password_ru": "va_PassWord_70"    
        }
        result = self.app_test.post('/registration', data=data)
        self.assertIn(b"<title>Registrazione</title>", result.data) 

    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_it_3_regitration_error(self, mock_ru_dao_read_by_email):
        mock_ru_dao_read_by_email.side_effect = mysql.connector.Error
        data = {
            "name_ru": "Andrea",
            "surname_ru": "Verdi",
            "gender_ru": 'M',
            "birthdate_ru": "1970-05-03",
            "city_birthplace_ru": "Torre annunziata",
            "nation_birthplace_ru": "Italia", 
            "nationality_ru": "Italiana",
            "profession_ru": "",
            "num_cellphone_ru": "",
            "email_ru": "av_70@test.test",
            "password_ru": "av_PassWord_70",
            "name_ra": "Via Giuseppe Verdi",
            "number_ra": 40,
            "city_ra": "Napoli",
            "province_ra": "NA",
            "cap_ra": "80013",
            "confirm_password_ru": "av_PassWord_70"    
        }
        result = self.app_test.post('/registration', data=data)
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)

        
    """ Test login """
    def test_it_4_login_success(self):
        data = {
            'email_ru': "av_70@test.test",
            'password_ru': "av_PassWord_70"
        }
        result = self.app_test.post('/login', data=data)
        self.assertIn(b"<title>Home page</title>", result.data) 
    def test_it_5_login_failure(self):
        data = {
            'email_ru': "av_70#test.test",
            'password_ru': "av_PassWord_70"
        }
        result = self.app_test.post('/login', data=data)
        self.assertIn(b"<title>Login</title>", result.data) 

    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_it_6_login_error(self, mock_ru_dao_read_by_email):
        mock_ru_dao_read_by_email.side_effect = mysql.connector.Error
        data = {
            'email_ru': "av_70@test.test",
            'password_ru': "av_PassWord_70"
        }
        result = self.app_test.post('/login', data=data)
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)









