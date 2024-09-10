import sys

import mysql.connector
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
from src.main.view.app import *
import mysql
import src.test.utils.utils as utils
from flask import session

class TestITUserAreaView(unittest.TestCase):
    def setUp(self):
        self.app_test = app.test_client()
        self.app_test.testing = True

    """ Test modification_personal_data """

    def test_it_1_modification_personal_data_success(self):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'

            data = {
                "profession_ru": "",
                "num_cellphone_ru": "",
                "email_ru": "av_70@test.test",
                "password_ru": "PassWord_70av",
                "confirm_password_ru": "PassWord_70av",    
                "name_ra": "Via Giuseppe Verdi",
                "number_ra": 40,
                "city_ra": "Napoli",
                "province_ra": "NA",
                "cap_ra": "80013",
                "id_ra": 1
            }
            
            result = c.post('/modification_personal_data', data=data)
            assert b"<title>Dati personali</title>" in result.data
    
    def test_it_2_modification_personal_data_failure(self):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'

            data = {
                "profession_ru": "",
                "num_cellphone_ru": "",
                "email_ru": "av_70#test.test",
                "password_ru": "PassWord_70av",
                "confirm_password_ru": "PassWord_70av",    
                "name_ra": "Via Giuseppe Verdi",
                "number_ra": 40,
                "city_ra": "Napoli",
                "province_ra": "NA",
                "cap_ra": "80013",
                "id_ra": 1
            }
            
            result = c.post('/modification_personal_data', data=data)
            assert b"<title>Dati personali</title>" in result.data

    @patch(utils.PATCH_RU_DAO_READ_BY_EMAIL)
    def test_it_3_modification_personal_data_error(self, mock_ru_dao_read_by_email):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'

            mock_ru_dao_read_by_email.side_effect = mysql.connector.Error
            data = {
                "profession_ru": "",
                "num_cellphone_ru": "",
                "email_ru": "av_70@test.test",
                "password_ru": "PassWord_70av",
                "confirm_password_ru": "PassWord_70av",    
                "name_ra": "Via Giuseppe Verdi",
                "number_ra": 40,
                "city_ra": "Napoli",
                "province_ra": "NA",
                "cap_ra": "80013",
                "id_ra": 1
            }
            
            result = c.post('/modification_personal_data', data=data)
            assert b"<title>Errore</title>" in result.data
            self.assertEqual(mock_ru_dao_read_by_email.call_count, 1)

