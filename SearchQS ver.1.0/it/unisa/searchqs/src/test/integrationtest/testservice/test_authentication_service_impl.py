import sys

import mysql.connector
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
from src.main.view.app import *
import mysql
import src.test.utils.utils as utils
from src.main.service.authenticationservice.authentication_service_impl import AuthenticationServiceImpl
from flask import session

class TestITAuthenticationServiceImpl(unittest.TestCase):
    app_test = app.test_client()
    app_test.testing = True
    service = AuthenticationServiceImpl()

    """ Test registration """

    def test_it_1_registration_success(self):
        attributes = {
            "name_ru": "Carla",
            "surname_ru": "Celeste",
            "gender_ru": 'F',
            "birthdate_ru": "1990-05-03",
            "city_birthplace_ru": "Milano",
            "nation_birthplace_ru": "Italia", 
            "nationality_ru": "Italiana",
            "profession_ru": "",
            "num_cellphone_ru": "",
            "email_ru": "cc_90@test.test",
            "password_ru": "cc_PassWord_90",
            "name_ra": "Via Giuseppe Verdi",
            "number_ra": "40",
            "city_ra": "Napoli",
            "province_ra": "NA",
            "cap_ra": "80013",
            "confirm_password_ru": "cc_PassWord_90"    
        }
        result = self.service.registration(attributes)
        oracle = {'success': True, 'errors': {}}
        self.assertEqual(result, oracle)
    
    def test_it_2_registration_failure(self):
        attributes = {
            "name_ru": "Carla",
            "surname_ru": "Celeste",
            "gender_ru": 'F',
            "birthdate_ru": "1990-05-03",
            "city_birthplace_ru": "Milano",
            "nation_birthplace_ru": "Italia", 
            "nationality_ru": "Italiana",
            "profession_ru": "",
            "num_cellphone_ru": "",
            "email_ru": "cc_90#test.test",
            "password_ru": "cc_PassWord_90",
            "name_ra": "Via Giuseppe Verdi",
            "number_ra": "40",
            "city_ra": "Napoli",
            "province_ra": "NA",
            "cap_ra": "80013",
            "confirm_password_ru": "cc_PassWord_90"    
        }
        result = self.service.registration(attributes)
        oracle = {
            'success': False, 
            "errors": {
                'name_ru': '', 'surname_ru': '', 'gender_ru': '', 'birthdate_ru': '', 
                'birthplace_ru': '', 'nationality_ru': '', 'profession_ru': '', 
                'num_cellphone_ru': '', 'email_ru': "Il formato dell'email non e' valido.\n", 
                'password_ru': '', 'confirm_password_ru': '', 'residential_address_ru': ''
            }, 
            'name_ru': attributes['name_ru'],
            'surname_ru': attributes['surname_ru'],
            'gender_ru': attributes['gender_ru'],
            'birthdate_ru': attributes['birthdate_ru'],
            'city_birthplace_ru': attributes['city_birthplace_ru'],
            'nation_birthplace_ru': attributes['nation_birthplace_ru'], 
            'nationality_ru': attributes['nationality_ru'],
            'profession_ru': attributes['profession_ru'],
            'num_cellphone_ru': attributes['num_cellphone_ru'],
            'email_ru': attributes['email_ru'],
            'password_ru': attributes['password_ru'], 
            'confirm_password_ru': attributes['confirm_password_ru'],
            'name_ra': attributes['name_ra'],
            'number_ra': attributes['number_ra'], 
            'city_ra': attributes['city_ra'],
            'province_ra': attributes['province_ra'],
            'cap_ra': attributes['cap_ra']
        }
        self.assertEqual(result, oracle)

    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_it_3_registration_error(self, mock_ru_dao_read_by_email):
        mock_ru_dao_read_by_email.side_effect = mysql.connector.Error
        attributes = {
            "name_ru": "Carla",
            "surname_ru": "Celeste",
            "gender_ru": 'F',
            "birthdate_ru": "1990-05-03",
            "city_birthplace_ru": "Milano",
            "nation_birthplace_ru": "Italia", 
            "nationality_ru": "Italiana",
            "profession_ru": "",
            "num_cellphone_ru": "",
            "email_ru": "cc_90@test.test",
            "password_ru": "cc_PassWord_90",
            "name_ra": "Via Giuseppe Verdi",
            "number_ra": "40",
            "city_ra": "Napoli",
            "province_ra": "NA",
            "cap_ra": "80013",
            "confirm_password_ru": "cc_PassWord_90"    
        }
        result = self.service.registration(attributes)
        oracle = {
            'success': None, 
            'error': 'La registrazione e\' fallita. Riprova.', 
        }
        self.assertEqual(result, oracle)
        self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)

    """ Test login """
    
    def test_it_4_login_success(self):
        with app.test_request_context():
            attributes = {
                'email_ru': "cc_90@test.test",
                'password_ru': "cc_PassWord_90"
            }
            result = self.service.login(attributes)
            oracle = {'success': True, "errors": {}}
            self.assertEqual(result, oracle)

    def test_it_5_login_failure(self):
        with app.test_request_context():
            attributes = {
                'email_ru': "cc_90@test.test",
                'password_ru': "90_PassWord_cc"
            }
            result = self.service.login(attributes)
            oracle = {
                'success': False, 
                'errors': {'form_login': 'Password e/o e-mail non corretta.\n'}, 
                'email_ru': attributes['email_ru'], 
                'password_ru': attributes['password_ru']}
            self.assertEqual(result, oracle)
    
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_it_6_login_error(self, mock_ru_dao_read_by_email):
        with app.test_request_context():
            mock_ru_dao_read_by_email.side_effect = mysql.connector.Error
            attributes = {
                'email_ru': "cc_90@test.test",
                'password_ru': "cc_PassWord_90"
            }
            result = self.service.login(attributes)
            oracle = {'success': None, 'error': "Il login e\' fallito. Riprova."}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
    








