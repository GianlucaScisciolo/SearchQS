import sys

import mysql.connector
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
from src.main.view.app import *
import mysql
import src.test.utils.utils as utils
from src.main.service.userareaservice.user_area_service_impl import UserAreaServiceImpl
from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress
from flask import session
import src.main.service.utils.security as security
from datetime import datetime

class TestITUserAreaServiceImpl(unittest.TestCase):
    def setUp(self):
        self.app_test = app.test_client()
        self.app_test.testing = True
        self.service = UserAreaServiceImpl()

    """ Test modification_personal_data """
    
    @patch(utils.PATCH_SECURITY_GENERATION_RANDOM_STRING)
    def test_it_1_modification_personal_data_success(self, mock_security_generation_random_string):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            
            mock_security_generation_random_string.return_value = 'Bj9m4ldLIFcKm67Q'
            attributes = {
                "profession_ru": "Studente",
                "num_cellphone_ru": "3323456789",
                "email_ru": "cc_90@test.test",
                "password_ru": "PassWord_cc90",
                "confirm_password_ru": "PassWord_cc90",    
                "name_ra": "Via Giuseppe Verdi",
                "number_ra": "40",
                "city_ra": "Napoli",
                "province_ra": "NA",
                "cap_ra": "80013",
                "id_ra": 1
            }
            result = self.service.modification_personal_data(attributes)
            data_str = "1990-05-03"
            data_date = datetime.strptime(data_str, "%Y-%m-%d").date()
            oracle = {
                'success': True, 
                'errors': {}, 
                'registered_user': RegisteredUser('cc_90@test.test', 'Carla', 'Celeste', 'F', data_date, 'Milano', 'Italia', 
                                                  'Italiana', 'Studente', '3323456789', '0eb73e727b95e4a70b70f4936a3b08541da8bfbf0f1f3d48cb354878793c87740260cda84ddd3a1ff5c6dedf89d00b031c5f239797b87875af2dd218391af01b', 
                                                  'Bj9m4ldLIFcKm67Q', 1), 
                'residential_address': ResidentialAddress(1, 'Via Giuseppe Verdi', '40', 'Napoli', 'NA', '80013'), 
                'id_ra': 1
            }
            self.assertEqual(result, oracle)
            self.assertEqual(mock_security_generation_random_string.call_count, 1)
            
    def test_it_2_modification_personal_data_failure(self):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            
            attributes = {
                "profession_ru": "Studente",
                "num_cellphone_ru": "3323456789",
                "email_ru": "cc_90#test.test",
                "password_ru": "PassWord_cc90",
                "confirm_password_ru": "PassWord_cc90",    
                "name_ra": "Via Giuseppe Verdi",
                "number_ra": "40",
                "city_ra": "Napoli",
                "province_ra": "NA",
                "cap_ra": "80013",
                "id_ra": 1
            }
            result = self.service.modification_personal_data(attributes)
            result['registered_user'].birthdate = str(result['registered_user'].birthdate)
            oracle = {
                'success': False, 
                'errors': {
                    'profession_ru': '', 
                    'num_cellphone_ru': '', 
                    'email_ru': "Il formato dell'email non e' valido.\n", 
                    'password_ru': '', 
                    'confirm_password_ru': '', 
                    'residential_address_ru': ''
                }, 
                'registered_user': RegisteredUser(
                    'cc_90#test.test', 'Carla', 'Celeste', 'F', "1990-05-03", 'Milano', 'Italia', 'Italiana', 
                    'Studente', '3323456789', '0eb73e727b95e4a70b70f4936a3b08541da8bfbf0f1f3d48cb354878793c87740260cda84ddd3a1ff5c6dedf89d00b031c5f239797b87875af2dd218391af01b', 
                    'Bj9m4ldLIFcKm67Q', 1), 
                'residential_address': ResidentialAddress(1, 'Via Giuseppe Verdi', '40', 'Napoli', 'NA', '80013'), 
                'password': 'PassWord_cc90', 
                'confirm_password': 'PassWord_cc90',
                'id_ra': 1
            }
            self.assertEqual(result, oracle)

    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_it_3_modification_personal_data_error(self, mock_ru_dao_read_by_email):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            
            mock_ru_dao_read_by_email.side_effect = mysql.connector.Error
            attributes = {
                "profession_ru": "Studente",
                "num_cellphone_ru": "3323456789",
                "email_ru": "cc_90@test.test",
                "password_ru": "PassWord_cc90",
                "confirm_password_ru": "PassWord_cc90",    
                "name_ra": "Via Giuseppe Verdi",
                "number_ra": "40",
                "city_ra": "Napoli",
                "province_ra": "NA",
                "cap_ra": "80013",
                "id_ra": 1
            }
            result = self.service.modification_personal_data(attributes)
            oracle = {'success': None, 'error': "Errore durante la modifica dei dati personali. Riprova."}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)
            
if __name__ == '__main__':
    unittest.main()







