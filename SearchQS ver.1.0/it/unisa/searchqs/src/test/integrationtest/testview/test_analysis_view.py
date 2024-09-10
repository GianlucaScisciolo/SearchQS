import sys

import mysql.connector
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
from src.main.view.app import *
import mysql
import src.test.utils.utils as utils
from flask import session
import os
from werkzeug.datastructures import FileStorage

class TestITAnalysisView(unittest.TestCase):
    def setUp(self):
        self.app_test = app.test_client()
        self.app_test.testing = True
    
    """ Test loading_q_system """

    def test_it_1_loading_q_system_success(self):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'
            with open('SistemaQuantistico.zip', 'rb') as f:
                file = FileStorage(f)
                data = {
                    'file': file
                }
                result = c.post('/loading_q_system', data=data, content_type='multipart/form-data')

                assert b"<title>Esecuzione analisi</title>" in result.data

    def test_it_2_loading_q_system_failure(self):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'
            with open('SistemaQuantistico.rar', 'rb') as f:
                file = FileStorage(f)
                data = {
                    'file': file
                }
                result = c.post('/loading_q_system', data=data, content_type='multipart/form-data')

                assert b"<title>Caricamento sistema quantistico</title>" in result.data

    @patch(utils.PATCH_QS_DAO_READ_BY_NAME_AND_EMAIL_REGISTERED_USER)
    def test_it_3_loading_q_system_error(self, mock_qs_dao_read_by_name_and_email_registered_user):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'
            mock_qs_dao_read_by_name_and_email_registered_user.side_effect = mysql.connector.Error
            with open('SistemaQuantistico.zip', 'rb') as f:
                file = FileStorage(f)
                data = {
                    'file': file
                }
                result = c.post('/loading_q_system', data=data, content_type='multipart/form-data')

                assert b"<title>Errore</title>" in result.data
                self.assertEqual(mock_qs_dao_read_by_name_and_email_registered_user.call_count, 1)
    
    """ Test execution_analyses """
    
    def test_it_4_execution_analyses_success(self):
        data = {
            "id_qs": 2, 
            "name_qs": "SistemaQuantistico.zip", 
            "optimization": 2, 
            "files_json": '["app_1\\\\SistemaQuantistico\\\\ile1.py", "app_1\\\\SistemaQuantistico\\\\files\\\\file2.py"]', 
            "transpilations_json": '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]', 
            "files_selected": ["app_1\\SistemaQuantistico\\file1.py", "app_1\\SistemaQuantistico\\files\\file2.py"], 
            "transpilations_selected": ["None", "simple", "ibm_perth"]
        }

        result = self.app_test.post('/execution_analyses', data=data)
        assert b"<title>Nomi transpilazioni</title>" in result.data
    
    def test_it_5_execution_analyses_failure(self):
        data = {
            "id_qs": 2, 
            "name_qs": "SistemaQuantistico.zip", 
            "optimization": 2, 
            "files_json": '["app_1\\\\SistemaQuantistico\\\\file1.py", "app_1\\\\SistemaQuantistico\\\\files\\\\file2.py"]', 
            "transpilations_json": '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]', 
            "files_selected": [], 
            "transpilations_selected": ["None", "simple", "ibm_perth"]
        }

        result = self.app_test.post('/execution_analyses', data=data)
        assert b"<title>Esecuzione analisi</title>" in result.data

    @patch(utils.PATCH_A_DAO_CREATE)
    def test_it_6_execution_analyses_error(self, mock_a_dao_create):
        mock_a_dao_create.side_effect = mysql.connector.Error
        data = {
            "id_qs": 2, 
            "name_qs": "SistemaQuantistico.zip", 
            "optimization": 2, 
            "files_json": '["app_1\\\\SistemaQuantistico\\\\file1.py", "app_1\\\\SistemaQuantistico\\\\files\\\\file2.py"]', 
            "transpilations_json": '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]', 
            "files_selected": ["app_1\\SistemaQuantistico\\file1.py", "app_1\\SistemaQuantistico\\files\\file2.py"], 
            "transpilations_selected": ["None", "simple", "ibm_perth"]
        }

        result = self.app_test.post('/execution_analyses', data=data)
        assert b"<title>Errore</title>" in result.data
        self.assertEqual(mock_a_dao_create.call_count, 1)

    """ Test display_analysis """
    
    def test_it_7_display_analysis_success(self):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'
        data = {
            'id_qs': 1, 
            'name_qs': "SistemaQuantistico.zip", 
            'save_date': '2023-10-10', 
            'id_analysis': 1, 
            'name_transpilation': 'ibm_perth', 
            'optimization': 2
        }
        result = self.app_test.post('/display_analysis', data=data)
        assert b"<title>Analisi</title>" in result.data
    
    @patch(utils.PATCH_R_DAO_READ_BY_ID_ANALYSIS)
    def test_it_8_display_analysis_error(self, mock_r_dao_read_by_id_analysis):
        with self.app_test as c:
            with c.session_transaction() as sess:
                sess['email'] = 'av_70@test.test'
                sess['actor'] = 'registered user'
        mock_r_dao_read_by_id_analysis.side_effect = mysql.connector.Error
        data = {
            'id_qs': 1, 
            'name_qs': "SistemaQuantistico.zip", 
            'save_date': '2023-10-10', 
            'id_analysis': 1, 
            'name_transpilation': 'ibm_perth', 
            'optimization': 2
        }
        result = self.app_test.post('/display_analysis', data=data)
        assert b"<title>Errore</title>" in result.data    
        self.assertEqual(mock_r_dao_read_by_id_analysis.call_count, 1)

    """ Test deletion_analysis """

    def test_it_9_deletion_analysis_success(self):
        data = {
            "id_analysis": 4, 
            "id_qs": 2, 
            "name_transpilation": 'ibm_perth', 
            "route": 'analysis.display_analysis', 
            "save_date_qs": '2023-10-10', 
            "name_qs": 'SistemaQuantistico.zip'
        }
        result = self.app_test.post('/deletion_analysis', data=data)
        assert b"<title>Analisi tipi di transpilazione</title>" in result.data
    
    @patch(utils.PATCH_A_DAO_DELETE_BY_ID)
    def test_it_10_deletion_analysis_error(self, mock_a_dao_delete_by_id):
        mock_a_dao_delete_by_id.side_effect = mysql.connector.Error
        data = {
            "id_analysis": 4, 
            "id_qs": 2, 
            "name_transpilation": 'ibm_perth', 
            "route": 'analysis.display_analysis', 
            "save_date_qs": '2023-10-10', 
            "name_qs": 'SistemaQuantistico.zip'
        }
        result = self.app_test.post('/deletion_analysis', data=data)
        assert b"<title>Errore</title>" in result.data
        self.assertEqual(mock_a_dao_delete_by_id.call_count, 1)
    





