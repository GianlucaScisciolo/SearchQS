import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import patch, MagicMock
from src.main.view.app import *
from src.main.service.authenticationservice.authentication_service_impl import AuthenticationServiceImpl
from src.main.model.entity.registered_user import RegisteredUser
import src.test.utils.utils as utils

class TestAuthenticationServiceImpl(unittest.TestCase):
    service = AuthenticationServiceImpl()
                          
    """ Test registration """

    @patch(utils.PATCH_CONNECTION_OPEN, return_value = True)
    @patch(utils.PATCH_CONNECTION_CLOSE, return_value = True)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_COMMIT, return_value = MagicMock())
    @patch(utils.PATCH_CF_CHECK_REGISTRATION, return_value = [{}, 0])
    @patch(utils.PATCH_CF_CHECK_REGISTRATION_REGISTERED_USER_IS_PRESENT, return_value = [{}, 0])
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL, return_value = [])
    @patch(utils.PATCH_RU_DAO_CREATE, return_value = True)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS, side_effect = [[], 10])
    @patch(utils.PATCH_RA_DAO_CREATE, return_value = True)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING, return_value = "B330tClS7rNVZIUq")
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD, return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7")
    def test_1_registration_with_create_ra_success(self, mock_security_encrypt_password, 
                                                 mock_security_generation_random_string, mock_ra_dao_create, 
                                                 mock_ra_dao_read_id_by_params, mock_ru_dao_create, 
                                                 mock_ru_dao_read_by_email, 
                                                 mock_cf_check_registration_registered_user_is_present, 
                                                 mock_cf_check_registration, 
                                                 mock_connection_commit, mock_connection_start_transaction, 
                                                 mock_connection_close, mock_connection_open):
        with app.test_request_context():
            attributes = {
                "name_ru": "Mario",
                "surname_ru": "Rossi",
                "gender_ru": 'M',
                "birthdate_ru": "1980-10-05",
                "city_birthplace_ru": "Torre del greco",
                "nation_birthplace_ru": "Italia", 
                "nationality_ru": "Italiana",
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": "86",
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "confirm_password_ru": "mr_PassWord_80"    
            }
            result = self.service.registration(attributes)
            oracle = {'success': True, 'errors': {}}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_encrypt_password.call_count, 1)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            self.assertEqual(mock_ra_dao_create.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 2)
            self.assertEqual(mock_ru_dao_create.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_registration_registered_user_is_present.call_count, 1)
            self.assertEqual(mock_cf_check_registration.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)
    
    
            

    @patch(utils.PATCH_CONNECTION_OPEN, return_value = True)
    @patch(utils.PATCH_CONNECTION_CLOSE, return_value = True)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_COMMIT, return_value = MagicMock())
    @patch(utils.PATCH_CF_CHECK_REGISTRATION, return_value = [{}, 0])
    @patch(utils.PATCH_CF_CHECK_REGISTRATION_REGISTERED_USER_IS_PRESENT, return_value = [{}, 0])
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL, return_value = [])
    @patch(utils.PATCH_RU_DAO_CREATE, return_value = True)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS, return_value = 10)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING, return_value = "B330tClS7rNVZIUq")
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD, return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7")
    def test_2_registration_without_create_ra_success(self, mock_security_encrypt_password, 
                                                 mock_security_generation_random_string, mock_ra_dao_read_id_by_params, 
                                                 mock_ru_dao_create, mock_ru_dao_read_by_email, 
                                                 mock_cf_check_registration_registered_user_is_present, 
                                                 mock_cf_check_registration, mock_connection_commit, 
                                                 mock_connection_start_transaction, mock_connection_close, 
                                                 mock_connection_open):
        with app.test_request_context():
            attributes = {
                "name_ru": "Mario",
                "surname_ru": "Rossi",
                "gender_ru": 'M',
                "birthdate_ru": "1980-10-05",
                "city_birthplace_ru": "Torre del greco",
                "nation_birthplace_ru": "Italia", 
                "nationality_ru": "Italia",
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": "86",
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "confirm_password_ru": "mr_PassWord_80"    
            }
            result = self.service.registration(attributes)
            oracle = {'success': True, 'errors': {}}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_encrypt_password.call_count, 1)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 1)
            self.assertEqual(mock_ru_dao_create.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_registration_registered_user_is_present.call_count, 1)
            self.assertEqual(mock_cf_check_registration.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN, return_value = True)
    @patch(utils.PATCH_CONNECTION_CLOSE, return_value = True)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_COMMIT, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_ROLLBACK, return_value = MagicMock())
    @patch(utils.PATCH_CF_CHECK_REGISTRATION, return_value = [{}, 0])
    @patch(utils.PATCH_CF_CHECK_REGISTRATION_REGISTERED_USER_IS_PRESENT, return_value = [{}, 0])
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL, return_value = [])
    @patch(utils.PATCH_RU_DAO_CREATE, return_value = True)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS, return_value = [])
    @patch(utils.PATCH_RA_DAO_CREATE, side_effect = Exception)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING, return_value = "B330tClS7rNVZIUq")
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD, return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7")
    def test_3_registration_with_create_ra_error(self, mock_security_encrypt_password, 
                                                 mock_security_generation_random_string, mock_ra_dao_create, 
                                                 mock_ra_dao_read_id_by_params, mock_ru_dao_create, 
                                                 mock_ru_dao_read_by_email, 
                                                 mock_cf_check_registration_registered_user_is_present, 
                                                 mock_cf_check_registration, mock_connection_rollback, 
                                                 mock_connection_commit, mock_connection_start_transaction, 
                                                 mock_connection_close, mock_connection_open):
        with app.test_request_context():
            attributes = {
                "name_ru": "Mario",
                "surname_ru": "Rossi",
                "gender_ru": 'M',
                "birthdate_ru": "1980-10-05",
                "city_birthplace_ru": "Torre del greco",
                "nation_birthplace_ru": "Italia", 
                "nationality_ru": "Italia",
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": "86",
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "confirm_password_ru": "mr_PassWord_80"    
            }
            result = self.service.registration(attributes)
            oracle = {'success': None, 'error': 'La registrazione e\' fallita. Riprova.'}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_ra_dao_create.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_registration_registered_user_is_present.call_count, 1)
            self.assertEqual(mock_cf_check_registration.call_count, 1)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN, return_value = True)
    @patch(utils.PATCH_CONNECTION_CLOSE, return_value = True)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_COMMIT, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_ROLLBACK, return_value = MagicMock())
    @patch(utils.PATCH_CF_CHECK_REGISTRATION, return_value = [{}, 0])
    @patch(utils.PATCH_CF_CHECK_REGISTRATION_REGISTERED_USER_IS_PRESENT, return_value = [{}, 0])
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL, return_value = [])
    @patch(utils.PATCH_RU_DAO_CREATE, side_effect = Exception)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS, return_value = 10)
    @patch(utils.PATCH_RA_DAO_CREATE, side_effect = Exception)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING, return_value = "B330tClS7rNVZIUq")
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD, return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7")
    def test_4_registration_without_create_ra_error(self, mock_security_encrypt_password, 
                                                 mock_security_generation_random_string, mock_ra_dao_create, 
                                                 mock_ra_dao_read_id_by_params, mock_ru_dao_create, 
                                                 mock_ru_dao_read_by_email, 
                                                 mock_cf_check_registration_registered_user_is_present, 
                                                 mock_cf_check_registration, mock_connection_rollback, 
                                                 mock_connection_commit, mock_connection_start_transaction, 
                                                 mock_connection_close, mock_connection_open):
        with app.test_request_context():
            attributes = {
                "name_ru": "Mario",
                "surname_ru": "Rossi",
                "gender_ru": 'M',
                "birthdate_ru": "1980-10-05",
                "city_birthplace_ru": "Torre del greco",
                "nation_birthplace_ru": "Italia", 
                "nationality_ru": "Italia",
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": "86",
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "confirm_password_ru": "mr_PassWord_80"    
            }
            result = self.service.registration(attributes)
            oracle = {'success': None, 'error': 'La registrazione e\' fallita. Riprova.'}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_encrypt_password.call_count, 1)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 1)
            self.assertEqual(mock_ru_dao_create.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_registration_registered_user_is_present.call_count, 1)
            self.assertEqual(mock_cf_check_registration.call_count, 1)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN, return_value = True)
    @patch(utils.PATCH_CONNECTION_CLOSE, return_value = True)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_COMMIT, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_ROLLBACK, return_value = MagicMock())
    @patch(utils.PATCH_CF_CHECK_REGISTRATION, return_value = [{}, 0])
    @patch(utils.PATCH_CF_CHECK_REGISTRATION_REGISTERED_USER_IS_PRESENT, return_value = [{'email_ru': "Utente con la stessa e-mail gia\' presente.\n"}, 1])
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_CREATE, side_effect = Exception)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS, return_value = 10)
    @patch(utils.PATCH_RA_DAO_CREATE, side_effect = Exception)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING, return_value = "B330tClS7rNVZIUq")
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD, return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7")
    def test_5_registration_ru_failure_1(self, mock_security_encrypt_password, 
                                                 mock_security_generation_random_string, mock_ra_dao_create, 
                                                 mock_ra_dao_read_id_by_params, mock_ru_dao_create, 
                                                 mock_ru_dao_read_by_email, 
                                                 mock_cf_check_registration_registered_user_is_present, 
                                                 mock_cf_check_registration, mock_connection_rollback, 
                                                 mock_connection_commit, mock_connection_start_transaction, 
                                                 mock_connection_close, mock_connection_open):
        with app.test_request_context():
            test_ru = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del greco", "Italia", 
                             "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                             "B330tClS7rNVZIUq", 10)
            mock_ru_dao_read_by_email.return_value = test_ru
            attributes = {
                "name_ru": "Mario",
                "surname_ru": "Rossi",
                "gender_ru": 'M',
                "birthdate_ru": "1980-10-05",
                "city_birthplace_ru": "Torre del greco",
                "nation_birthplace_ru": "Italia", 
                "nationality_ru": "Italia",
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": "86",
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "confirm_password_ru": "mr_PassWord_80"    
            }
            result = self.service.registration(attributes)
            oracle = {
                'success': False, 
                'errors': {'email_ru': "Utente con la stessa e-mail gia\' presente.\n"}, 
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
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_registration_registered_user_is_present.call_count, 1)
            self.assertEqual(mock_cf_check_registration.call_count, 1)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN, return_value = True)
    @patch(utils.PATCH_CONNECTION_CLOSE, return_value = True)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_COMMIT, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_ROLLBACK, return_value = MagicMock())
    @patch(utils.PATCH_CF_CHECK_REGISTRATION, return_value = [{'email_ru': "Il formato dell\'e-mail non e\' valido.\n"}, 1])
    @patch(utils.PATCH_CF_CHECK_REGISTRATION_REGISTERED_USER_IS_PRESENT, return_value = [{'email_ru': "Utente con la stessa e-mail gia\' presente.\n"}, 1])
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_CREATE, side_effect = Exception)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS, return_value = 10)
    @patch(utils.PATCH_RA_DAO_CREATE, side_effect = Exception)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING, return_value = "B330tClS7rNVZIUq")
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD, return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7")
    def test_6_registration_failure_2(self, mock_security_encrypt_password, 
                                                 mock_security_generation_random_string, mock_ra_dao_create, 
                                                 mock_ra_dao_read_id_by_params, mock_ru_dao_create, 
                                                 mock_ru_dao_read_by_email, 
                                                 mock_cf_check_registration_registered_user_is_present, 
                                                 mock_cf_check_registration, mock_connection_rollback, 
                                                 mock_connection_commit, mock_connection_start_transaction, 
                                                 mock_connection_close, mock_connection_open):
        with app.test_request_context():
            test_ru = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del greco", "Italia", 
                             "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                             "B330tClS7rNVZIUq", 10)
            mock_ru_dao_read_by_email.return_value = test_ru
            attributes = {
                "name_ru": "Mario",
                "surname_ru": "Rossi",
                "gender_ru": 'M',
                "birthdate_ru": "1980-10-05",
                "city_birthplace_ru": "Torre del greco",
                "nation_birthplace_ru": "Italia", 
                "nationality_ru": "Italia",
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80#test.test",
                "password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": "86",
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "confirm_password_ru": "mr_PassWord_80"    
            }
            result = self.service.registration(attributes)
            oracle = {
                'success': False, 
                "errors": {'email_ru': "Il formato dell\'e-mail non e\' valido.\n"}, 
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
            self.assertEqual(mock_cf_check_registration.call_count, 1)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    """ Test login """

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CF_CHECK_LOGIN)
    @patch(utils.PATCH_CF_CHECK_LOGIN_AUTHENTICATION)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_7_login_success(self, mock_ru_dao_read_by_email, mock_cf_check_login_authentication, 
                           mock_cf_check_login, mock_connection_close, mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_cf_check_login.return_value = [{}, 0]
            mock_ru_dao_read_by_email.read_by_email.return_value = RegisteredUser(
                "mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", "Italiana", 
                "Computer Science", "3334445556", "mr_PassWord_80", "Salt Hex", 2
            )
            mock_cf_check_login_authentication.return_value = [{}, 0]
            mock_connection_close.return_value = True
            attributes = {
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80"
            }
            result = self.service.login(attributes)
            oracle = {'success': True, "errors": {}}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_login_authentication.call_count, 1)
            self.assertEqual(mock_cf_check_login.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

            
            
    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CF_CHECK_LOGIN)
    def test_8_login_failure_1(self, mock_cf_check_login, mock_connection_close, mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_cf_check_login.return_value = [
                {"email_ru": "Il formato dell\'e-mail non e\' valido.\n", 'password_ru': ""}, 1
            ]
            mock_connection_close.return_value = True
            attributes = {
                'email_ru': "mr_80#test.test",
                'password_ru': "mr_PassWord_80"
            }
            result = self.service.login(attributes)
            oracle = {
                "success": False, 
                "errors": {"email_ru": "Il formato dell\'e-mail non e\' valido.\n", 'password_ru': ""}, 
                'email_ru': "mr_80#test.test",
                'password_ru': "mr_PassWord_80"
            }
            self.assertEqual(result, oracle)
            self.assertEqual(mock_cf_check_login.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CF_CHECK_LOGIN)
    @patch(utils.PATCH_CF_CHECK_LOGIN_AUTHENTICATION)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_9_login_failure_2(self, mock_ru_dao_read_by_email, mock_cf_check_login_authentication, 
                           mock_cf_check_login, mock_connection_close, mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_cf_check_login.return_value = [{}, 0]
            mock_ru_dao_read_by_email.return_value = []
            mock_cf_check_login_authentication.return_value = [
                {'form_login': "Password e/o e-mail non corretta.\n"}, 1
            ]
            mock_connection_close.return_value = True
            attributes = {
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_90"
            }
            result = self.service.login(attributes)
            oracle = {
                "success": False, 
                "errors": {"form_login": "Password e/o e-mail non corretta.\n"}, 
                'email_ru': "mr_80@test.test", 
                'password_ru': "mr_PassWord_90"
            }
            self.assertEqual(result, oracle)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_login_authentication.call_count, 1)
            self.assertEqual(mock_cf_check_login.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CF_CHECK_LOGIN)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_10_login_error(self, mock_ru_dao_read_by_email, mock_cf_check_login, mock_connection_close, 
                          mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_cf_check_login.return_value = [{}, 0]
            mock_ru_dao_read_by_email.side_effect = Exception
            mock_connection_close.return_value = True
            attributes = {
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80"
            }
            result = self.service.login(attributes)
            oracle = {'success': None, 'error': "Il login e\' fallito. Riprova."}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_cf_check_login.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)







