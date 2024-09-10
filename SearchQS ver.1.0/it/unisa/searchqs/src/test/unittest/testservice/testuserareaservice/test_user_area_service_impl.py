import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import patch, MagicMock
from src.main.service.userareaservice.user_area_service_impl import UserAreaServiceImpl
from src.main.view.app import *
import src.test.utils.utils as utils
from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress

class TestUserAreaServiceImpl(unittest.TestCase):
    service = UserAreaServiceImpl()

    """ Test modification_personal_data """
    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_UA_SERVICE_DISPLAY_PERSONAL_DATA)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_UPDATE_BY_PARAMS)
    @patch(utils.PATCH_RU_DAO_READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS)
    @patch(utils.PATCH_CF_CHECK_MODIFICATION_PERSONAL_DATA)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_RA_DAO_CREATE)
    @patch(utils.PATCH_RA_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING)
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD)
    def test_1_modification_personal_data_with_create_ra_and_with_delete_ra_success(
                    self, mock_security_encrypt_password, mock_security_generation_random_string, 
                    mock_ra_dao_delete_by_id, mock_ra_dao_create, mock_ra_dao_read_id_by_params, 
                    mock_cf_check_modification_personal_data, 
                    mock_ru_dao_read_num_registered_user_by_id_residential_address, mock_ru_dao_update_by_params, 
                    mock_ru_dao_read_by_email, mock_ua_service_display_personal_data,
                    mock_connection_commit, mock_connection_start_transaction, mock_connection_close, 
                    mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_ua_service_display_personal_data.return_value = {
                "registered_user": RegisteredUser("old_email@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                            "Italiana", "Old professione", "3333333333", "6095bf0a42541c3732324456a4a138516e7afc1d56e434b2c9be3d8690c4814f36d0a49e1523d81bc0902d859a94c24625553b803e6494a04a7ed32edccaf613", 
                                            "EmPXS0J7wjbqOO5p", 20), 
                "residential_address": ResidentialAddress(10, "old name", 42, "old city", "old province", "00000")
            }
            mock_ru_dao_read_by_email.return_value = []
            mock_cf_check_modification_personal_data.return_value = [{}, 0]
            mock_ra_dao_read_id_by_params.side_effect = [[], 20]
            mock_ra_dao_create.return_value = True
            mock_security_generation_random_string.return_value = "B330tClS7rNVZIUq"
            mock_security_encrypt_password.return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7"
            mock_ru_dao_update_by_params.return_value = True
            mock_ru_dao_read_num_registered_user_by_id_residential_address.return_value = 0
            mock_ra_dao_delete_by_id.return_value = True
            mock_connection_commit.return_value = MagicMock()
            mock_connection_close.return_value = True


            session['email'] = "old_email@test.test"
            attributes = {
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "confirm_password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": 86,
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "id_ra": 10    
            }
            ru_test = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                     "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                                     "B330tClS7rNVZIUq", 20)
            ra_test = ResidentialAddress(20, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            id_ra_test = 20
            oracle = {
                'success': True,
                'errors': {}, 
                'registered_user': ru_test, 
                'residential_address': ra_test, 
                'id_ra': id_ra_test
            }

            result = self.service.modification_personal_data(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_encrypt_password.call_count, 1)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            self.assertEqual(mock_ra_dao_delete_by_id.call_count, 1)
            self.assertEqual(mock_ra_dao_create.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 2)
            self.assertEqual(mock_cf_check_modification_personal_data.call_count, 1)
            self.assertEqual(mock_ru_dao_read_num_registered_user_by_id_residential_address.call_count, 1)
            self.assertEqual(mock_ru_dao_update_by_params.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_ua_service_display_personal_data.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_UA_SERVICE_DISPLAY_PERSONAL_DATA)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_UPDATE_BY_PARAMS)
    @patch(utils.PATCH_RU_DAO_READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS)
    @patch(utils.PATCH_CF_CHECK_MODIFICATION_PERSONAL_DATA)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_RA_DAO_CREATE)
    @patch(utils.PATCH_RA_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING)
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD)
    def test_2_modification_personal_data_with_create_ra_and_without_delete_ra_success(
                    self, mock_security_encrypt_password, mock_security_generation_random_string, 
                    mock_ra_dao_delete_by_id, mock_ra_dao_create, mock_ra_dao_read_id_by_params, 
                    mock_cf_check_modification_personal_data, 
                    mock_ru_dao_read_num_registered_user_by_id_residential_address, mock_ru_dao_update_by_params, 
                    mock_ru_dao_read_by_email, mock_ua_service_display_personal_data,
                    mock_connection_commit, mock_connection_start_transaction, mock_connection_close, 
                    mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_ua_service_display_personal_data.return_value = {
                "registered_user": RegisteredUser("old_email@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                            "Italiana", "Old professione", "3333333333", "6095bf0a42541c3732324456a4a138516e7afc1d56e434b2c9be3d8690c4814f36d0a49e1523d81bc0902d859a94c24625553b803e6494a04a7ed32edccaf613", 
                                            "EmPXS0J7wjbqOO5p", 20), 
                "residential_address": ResidentialAddress(10, "old name", 42, "old city", "old province", "00000")
            }
            mock_ru_dao_read_by_email.return_value = []
            mock_cf_check_modification_personal_data.return_value = [{}, 0]
            mock_ra_dao_read_id_by_params.side_effect = [[], 20]
            mock_ra_dao_create.return_value = True
            mock_security_generation_random_string.return_value = "B330tClS7rNVZIUq"
            mock_security_encrypt_password.return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7"
            mock_ru_dao_update_by_params.return_value = True
            mock_ru_dao_read_num_registered_user_by_id_residential_address.return_value = 1
            mock_connection_commit.return_value = MagicMock()
            mock_connection_close.return_value = True
            session['email'] = "old_email@test.test"
            attributes = {
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "confirm_password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": 86,
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "id_ra": 10    
            }
            ru_test = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                     "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                                     "B330tClS7rNVZIUq", 20)
            ra_test = ResidentialAddress(20, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            id_ra_test = 20
            oracle = {
                'success': True,
                'errors': {}, 
                'registered_user': ru_test, 
                'residential_address': ra_test, 
                'id_ra': id_ra_test
            }            
            result = self.service.modification_personal_data(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_encrypt_password.call_count, 1)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            self.assertEqual(mock_ra_dao_create.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 2)
            self.assertEqual(mock_cf_check_modification_personal_data.call_count, 1)
            self.assertEqual(mock_ru_dao_read_num_registered_user_by_id_residential_address.call_count, 1)
            self.assertEqual(mock_ru_dao_update_by_params.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_ua_service_display_personal_data.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)
            
    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_UA_SERVICE_DISPLAY_PERSONAL_DATA)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_UPDATE_BY_PARAMS)
    @patch(utils.PATCH_RU_DAO_READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS)
    @patch(utils.PATCH_CF_CHECK_MODIFICATION_PERSONAL_DATA)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_RA_DAO_CREATE)
    @patch(utils.PATCH_RA_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING)
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD)
    def test_3_modification_personal_data_without_create_ra_and_without_delete_ra_success(
                    self, mock_security_encrypt_password, mock_security_generation_random_string, 
                    mock_ra_dao_delete_by_id, mock_ra_dao_create, mock_ra_dao_read_id_by_params, 
                    mock_cf_check_modification_personal_data, 
                    mock_ru_dao_read_num_registered_user_by_id_residential_address, mock_ru_dao_update_by_params, 
                    mock_ru_dao_read_by_email, mock_ua_service_display_personal_data, 
                    mock_connection_commit, mock_connection_start_transaction, mock_connection_close, 
                    mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_ua_service_display_personal_data.return_value = {
                "registered_user": RegisteredUser("old_email@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                            "Italiana", "Old professione", "3333333333", "6095bf0a42541c3732324456a4a138516e7afc1d56e434b2c9be3d8690c4814f36d0a49e1523d81bc0902d859a94c24625553b803e6494a04a7ed32edccaf613", 
                                            "EmPXS0J7wjbqOO5p", 20), 
                "residential_address": ResidentialAddress(10, "old name", 42, "old city", "old province", "00000")
            }
            mock_ru_dao_read_by_email.return_value = []
            mock_cf_check_modification_personal_data.return_value = [{}, 0]
            mock_ra_dao_read_id_by_params.return_value = 10
            mock_security_generation_random_string.return_value = "B330tClS7rNVZIUq"
            mock_security_encrypt_password.return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7"
            mock_ru_dao_update_by_params.return_value = True
            mock_ru_dao_read_num_registered_user_by_id_residential_address.return_value = 2
            mock_connection_commit.return_value = MagicMock()
            mock_connection_close.return_value = True
            

            session['email'] = "old_email@test.test"
            attributes = {
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "confirm_password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": 86,
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "id_ra": 10    
            }
            ru_test = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                     "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                                     "B330tClS7rNVZIUq", 10)
            ra_test = ResidentialAddress(10, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            id_ra_test = 10
            oracle = {
                'success': True,
                'errors': {}, 
                'registered_user': ru_test, 
                'residential_address': ra_test, 
                'id_ra': id_ra_test
            }            
            result = self.service.modification_personal_data(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_encrypt_password.call_count, 1)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 1)
            self.assertEqual(mock_cf_check_modification_personal_data.call_count, 1)
            self.assertEqual(mock_ru_dao_read_num_registered_user_by_id_residential_address.call_count, 1)
            self.assertEqual(mock_ru_dao_update_by_params.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_ua_service_display_personal_data.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)
            
    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK)
    @patch(utils.PATCH_UA_SERVICE_DISPLAY_PERSONAL_DATA)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_UPDATE_BY_PARAMS)
    @patch(utils.PATCH_RU_DAO_READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS)
    @patch(utils.PATCH_CF_CHECK_MODIFICATION_PERSONAL_DATA)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_RA_DAO_CREATE)
    @patch(utils.PATCH_RA_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING)
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD)
    def test_4_modification_personal_data_with_create_ra_error(
                    self, mock_security_encrypt_password, mock_security_generation_random_string, 
                    mock_ra_dao_delete_by_id, mock_ra_dao_create, mock_ra_dao_read_id_by_params, 
                    mock_cf_check_modification_personal_data, 
                    mock_ru_dao_read_num_registered_user_by_id_residential_address, mock_ru_dao_update_by_params, 
                    mock_ru_dao_read_by_email, mock_ua_service_display_personal_data, mock_connection_rollback, 
                    mock_connection_commit, mock_connection_start_transaction, mock_connection_close, 
                    mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_ua_service_display_personal_data.return_value = {
                "registered_user": RegisteredUser("old_email@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                            "Italiana", "Old professione", "3333333333", "6095bf0a42541c3732324456a4a138516e7afc1d56e434b2c9be3d8690c4814f36d0a49e1523d81bc0902d859a94c24625553b803e6494a04a7ed32edccaf613", 
                                            "EmPXS0J7wjbqOO5p", 20), 
                "residential_address": ResidentialAddress(10, "old name", 42, "old city", "old province", "00000")
            }
            mock_ru_dao_read_by_email.return_value = []
            mock_cf_check_modification_personal_data.return_value = [{}, 0]
            mock_ra_dao_read_id_by_params.return_value = []
            mock_ra_dao_create.side_effect = Exception
            mock_connection_rollback.return_value = MagicMock()
            mock_connection_close.return_value = True
            session['email'] = "old_email@test.test"
            attributes = {
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "confirm_password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": 86,
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "id_ra": 10    
            }
            ru_test = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                     "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                                     "B330tClS7rNVZIUq", 20)
            ra_test = ResidentialAddress(20, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            id_ra_test = 20
            oracle = {'success': None, 'error': "Errore durante la modifica dei dati personali. Riprova."}
            result = self.service.modification_personal_data(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_ra_dao_create.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 1)
            self.assertEqual(mock_cf_check_modification_personal_data.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_ua_service_display_personal_data.call_count, 1)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)
            
    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK)
    @patch(utils.PATCH_UA_SERVICE_DISPLAY_PERSONAL_DATA)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_UPDATE_BY_PARAMS)
    @patch(utils.PATCH_RU_DAO_READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS)
    @patch(utils.PATCH_CF_CHECK_MODIFICATION_PERSONAL_DATA)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_RA_DAO_CREATE)
    @patch(utils.PATCH_RA_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING)
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD)
    def test_5_modification_personal_data_with_create_ra_and_with_delete_ra_error(
                    self, mock_security_encrypt_password, mock_security_generation_random_string, 
                    mock_ra_dao_delete_by_id, mock_ra_dao_create, mock_ra_dao_read_id_by_params, 
                    mock_cf_check_modification_personal_data, 
                    mock_ru_dao_read_num_registered_user_by_id_residential_address, mock_ru_dao_update_by_params, 
                    mock_ru_dao_read_by_email, mock_ua_service_display_personal_data, mock_connection_rollback, 
                    mock_connection_commit, mock_connection_start_transaction, mock_connection_close, 
                    mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_ua_service_display_personal_data.return_value = {
                "registered_user": RegisteredUser("old_email@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                            "Italiana", "Old professione", "3333333333", "6095bf0a42541c3732324456a4a138516e7afc1d56e434b2c9be3d8690c4814f36d0a49e1523d81bc0902d859a94c24625553b803e6494a04a7ed32edccaf613", 
                                            "EmPXS0J7wjbqOO5p", 20), 
                "residential_address": ResidentialAddress(10, "old name", 42, "old city", "old province", "00000")
            }
            mock_ru_dao_read_by_email.return_value = []
            mock_cf_check_modification_personal_data.return_value = [{}, 0]
            mock_ra_dao_read_id_by_params.side_effect = [[], 20]
            mock_ra_dao_create.return_value = True
            mock_security_generation_random_string.return_value = "B330tClS7rNVZIUq"
            mock_security_encrypt_password.return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7"
            mock_ru_dao_update_by_params.return_value = True
            mock_ru_dao_read_num_registered_user_by_id_residential_address.return_value = 0
            mock_ra_dao_delete_by_id.side_effect = Exception
            mock_connection_rollback.return_value = MagicMock()
            mock_connection_close.return_value = True
            

            session['email'] = "old_email@test.test"
            attributes = {
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80@test.test",
                "password_ru": "mr_PassWord_80",
                "confirm_password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": 86,
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "id_ra": 10    
            }
            ru_test = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                     "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                                     "B330tClS7rNVZIUq", 20)
            ra_test = ResidentialAddress(20, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            id_ra_test = 20
            result = self.service.modification_personal_data(attributes)
            oracle = {'success': None, 'error': "Errore durante la modifica dei dati personali. Riprova."}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_encrypt_password.call_count, 1)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            self.assertEqual(mock_ra_dao_delete_by_id.call_count, 1)
            self.assertEqual(mock_ra_dao_create.call_count, 1)
            self.assertEqual(mock_ra_dao_read_id_by_params.call_count, 2)
            self.assertEqual(mock_cf_check_modification_personal_data.call_count, 1)
            self.assertEqual(mock_ru_dao_read_num_registered_user_by_id_residential_address.call_count, 1)
            self.assertEqual(mock_ru_dao_update_by_params.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_ua_service_display_personal_data.call_count, 1)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)
            
    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE, return_value = True)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT, return_value = MagicMock())
    @patch(utils.PATCH_CONNECTION_ROLLBACK, return_value = MagicMock())
    @patch(utils.PATCH_UA_SERVICE_DISPLAY_PERSONAL_DATA)
    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    @patch(utils.PATCH_RU_DAO_UPDATE_BY_PARAMS, return_value = True)
    @patch(utils.PATCH_RU_DAO_READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS, return_value = 0)
    @patch(utils.PATCH_CF_CHECK_MODIFICATION_PERSONAL_DATA)
    @patch(utils.PATCH_RA_DAO_READ_ID_BY_PARAMS, side_effect = [[], 20])
    @patch(utils.PATCH_RA_DAO_CREATE, return_value = True)
    @patch(utils.PATCH_RA_DAO_DELETE_BY_ID, return_value = True)
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING, return_value = "B330tClS7rNVZIUq")
    @patch(utils.PATCH_SECURITY_ENCRYPT_PASSWORD, return_value = "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7")
    def test_6_modification_personal_data_failure(
                    self, mock_security_encrypt_password, mock_security_generation_random_string, 
                    mock_ra_dao_delete_by_id, mock_ra_dao_create, mock_ra_dao_read_id_by_params, 
                    mock_cf_check_modification_personal_data, 
                    mock_ru_dao_read_num_registered_user_by_id_residential_address, mock_ru_dao_update_by_params, 
                    mock_ru_dao_read_by_email, mock_ua_service_display_personal_data, mock_connection_rollback, 
                    mock_connection_commit, mock_connection_start_transaction, mock_connection_close, 
                    mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_ua_service_display_personal_data.return_value = {
                "registered_user": RegisteredUser("old_email@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                            "Italiana", "Old professione", "3333333333", "6095bf0a42541c3732324456a4a138516e7afc1d56e434b2c9be3d8690c4814f36d0a49e1523d81bc0902d859a94c24625553b803e6494a04a7ed32edccaf613", 
                                            "EmPXS0J7wjbqOO5p", 20), 
                "residential_address": ResidentialAddress(10, "old name", 42, "old city", "old province", "00000")
            }
            mock_ru_dao_read_by_email.return_value = []
            mock_cf_check_modification_personal_data.return_value = [{'email_ru': "Il formato dell\'email non e\' valido.\n"}, 1]
            mock_connection_rollback.return_value = MagicMock()
            mock_connection_close.return_value = True

            session['email'] = "old_email@test.test"
            attributes = {
                "profession_ru": "Computer Science",
                "num_cellphone_ru": "3334445556",
                "email_ru": "mr_80#test.test",
                "password_ru": "mr_PassWord_80",
                "confirm_password_ru": "mr_PassWord_80",
                "name_ra": "Corso Mario Pagano",
                "number_ra": 86,
                "city_ra": "Roccapiemonte",
                "province_ra": "SA",
                "cap_ra": "84086",
                "id_ra": 10    
            }
            ru_test = RegisteredUser("mr_80#test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", "Italia", 
                                     "Italiana", "Computer Science", "3334445556", "6095bf0a42541c3732324456a4a138516e7afc1d56e434b2c9be3d8690c4814f36d0a49e1523d81bc0902d859a94c24625553b803e6494a04a7ed32edccaf613", 
                                     "EmPXS0J7wjbqOO5p", 20)
            ra_test = ResidentialAddress(10, "Corso Mario Pagano", 86, "Roccapiemonte", "SA", "84086")
            oracle = {
                'success': False,
                'errors': {'email_ru': "Il formato dell\'email non e\' valido.\n"},
                'registered_user': ru_test, 
                'residential_address': ra_test, 
                'password': "mr_PassWord_80",
                'confirm_password': "mr_PassWord_80",
                'id_ra': 10
            }
            result = self.service.modification_personal_data(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_cf_check_modification_personal_data.call_count, 1)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            self.assertEqual(mock_ua_service_display_personal_data.call_count, 1)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)


            










    
    
    
    
    
    
    
    
    