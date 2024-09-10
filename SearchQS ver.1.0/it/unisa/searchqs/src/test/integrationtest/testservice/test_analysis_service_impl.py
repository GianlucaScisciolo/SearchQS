import sys

import mysql.connector
sys.path.append("../../../..")

import unittest
from unittest.mock import patch
from src.main.view.app import *
import mysql
import src.test.utils.utils as utils
from src.main.service.analysisservice.analysis_service_impl import AnalysisServiceImpl
from flask import session
from werkzeug.datastructures import FileStorage
import json
from src.main.model.entity.q_system import QSystem
from src.main.model.entity.analysis import Analysis
from src.main.model.entity.source_file import SourceFile
from src.main.model.entity.result_dynamic_analysis import ResultDynamicAnalysis

class TestITAnalysisServiceImpl(unittest.TestCase):
    def setUp(self):
        self.app_test = app.test_client()
        self.app_test.testing = True
        self.service = AnalysisServiceImpl()

    """ Test loading_q_system """
    
    def test_it_1_loading_q_system_success(self):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            with open('SistemaQuantistico.zip', 'rb') as f:
                file = FileStorage(f)
                attributes = {
                    'file': file,
                    'filename': 'SistemaQuantistico.zip'
                }
                result = self.service.loading_q_system(attributes)
                oracle = {
                    'success': True, 
                    'python_files': ['app_1\\SistemaQuantistico\\file1.py', 'app_1\\SistemaQuantistico\\files\\file2.py'], 
                    'files_json': '["app_1\\\\SistemaQuantistico\\\\file1.py", "app_1\\\\SistemaQuantistico\\\\files\\\\file2.py"]', 
                    'id_qs': 1, 
                    'name_qs': 'SistemaQuantistico.zip', 
                    'num_errors': 0  
                }
                self.assertEqual(result, oracle)
    def test_it_2_loading_q_system_failure(self):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            with open('SistemaQuantistico.rar', 'rb') as f:
                file = FileStorage(f)
                attributes = {
                    'file': file,
                    'filename': 'SistemaQuantistico.rar'
                }
                result = self.service.loading_q_system(attributes)
                oracle = {
                    'success': False, 
                    'errors': {'file': "Il sistema quantistico caricato non è del tipo .zip.\n"}, 
                    'num_errors': 1
                }
                self.assertEqual(result, oracle)

    @patch(utils.PATCH_QS_DAO_READ_BY_NAME_AND_EMAIL_REGISTERED_USER)
    def test_it_3_loading_q_system_error(self, mock_qs_dao_read_by_name_and_email_registered_user):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            
            mock_qs_dao_read_by_name_and_email_registered_user.side_effect = mysql.connector.Error
            with open('SistemaQuantistico.zip', 'rb') as f:
                file = FileStorage(f)
                attributes = {
                    'file': file,
                    'filename': 'SistemaQuantistico.zip'
                }
                result = self.service.loading_q_system(attributes)
                oracle = {
                    'success': None, 
                    'error': "Errore durante il caricamento del sistema quantistico. Riprova."
                }
                self.assertEqual(result, oracle)
                self.assertEqual(mock_qs_dao_read_by_name_and_email_registered_user.call_count, 1)

    """ Test execution_analyses """

    def test_it_4_execution_analyses_success(self):
        attributes = {
            "id_qs": 1, 
            "name_qs": "SistemaQuantistico.zip", 
            "optimization": 2, 
            "files_json": '["app_1\\\\SistemaQuantistico\\\\file1.py", "app_1\\\\SistemaQuantistico\\\\files\\\\file2.py"]', 
            "transpilations_json": '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]',
            "files_selected": ["app_1\\\\SistemaQuantistico\\\\file1.py"],
            "transpilations_selected": ["ibm_perth"]
        }
        result = self.service.execution_analyses(attributes)
        oracle = {
            'success': True, 
            'transpilations': ["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]
        }
        self.assertEqual(result, oracle)
    
    def test_it_5_execution_analyses_failure(self):
        attributes = {
            "id_qs": 1, 
            "name_qs": "SistemaQuantistico.zip", 
            "optimization": 2, 
            "files_json": '["app_1\\\\SistemaQuantistico\\\\file1.py"]', 
            "transpilations_json": '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]',
            "files_selected": [],
            "transpilations_selected": ["ibm_perth"]
        }
        result = self.service.execution_analyses(attributes)
        oracle = {
            'success': False,
            'id_qs': attributes['id_qs'],
            'name_qs': attributes['name_qs'],
            'errors': {'files_selected': 'Nessun file selezionato. Seleziona almeno un file.\n', 'transpilations_selected': '', 'optimization': ''}, 
            'num_errors': 1, 
            'files_json': attributes['files_json'],
            'transpilations_json': attributes['transpilations_json'],
            'python_files': json.loads(attributes['files_json']),
            'transpilations': json.loads(attributes['transpilations_json'])
        }
        
        self.assertEqual(result, oracle)

    @patch(utils.PATCH_SF_DAO_READ_BY_PARAMS)
    def test_it_6_execution_analyses_error(self, mock_sf_dao_read_by_params):
        mock_sf_dao_read_by_params.side_effect = mysql.connector.Error
        attributes = {
            "id_qs": 1, 
            "name_qs": "SistemaQuantistico.zip", 
            "optimization": 2, 
            "files_json": '["app_1\\\\SistemaQuantistico\\\\file1.py", "app_1\\\\SistemaQuantistico\\\\files\\\\file2.py"]', 
            "transpilations_json": '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]',
            "files_selected": ["app_1\\\\SistemaQuantistico\\\\file1.py"],
            "transpilations_selected": ["ibm_perth"]
        }
        result = self.service.execution_analyses(attributes)
        oracle = {'success': None, 'error': "Errore durante l\'esecuzone delle analisi. Riprova."}
        self.assertEqual(result, oracle)
        self.assertEqual(mock_sf_dao_read_by_params.call_count, 1)


    """ Test display_analysis """

    def test_it_7_display_analysis_success(self):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            attributes = {
                'id_qs': 1, 
                'name_qs': "SistemaQuantistico.zip", 
                'save_date': "2023-01-02", 
                'id_analysis': 1, 
                'name_transpilation': "ibm_perth", 
                'optimization': 2
            }
            result = self.service.display_analysis(attributes)
            test_qs = QSystem(1, "SistemaQuantistico.zip", "cc_90@test.test")
            test_analysis = Analysis(1, 'ibm_perth', 2, '2023-01-02', 1)
            test_code = ""
            test_code += "from qiskit import transpile\n"
            test_code += "from qiskit import *\n"
            test_code += "qc1 = QuantumCircuit(2,2)\n"
            test_code += "qc2 = QuantumCircuit(2,2)\n"
            test_code += "qc1.x(0)\n"
            test_code += "qc1.y(0)\n"
            test_code += "qc1.cx(0,1)\n"
            test_code += "qc2.h(0)\n"
            test_code += "qc2.h(0)\n"
            test_code += "qc2.h(1)\n"
            test_code += "qc2.cx(0,1)\n"
            test_code += "print(qc1)\n"
            test_code += "print(qc2)\n"
            test_code += "\n"
            test_code += "qc1 = transpile(qc1, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=2)\n"
            test_code += "qc2 = transpile(qc2, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=2)\n"
            test_sf = SourceFile(
                1, 
                'app_1\\\\SistemaQuantistico\\\\file1.py', 
                b"\nfrom qiskit import transpile\nfrom qiskit import *\nqc1 = QuantumCircuit(2,2)\nqc2 = QuantumCircuit(2,2)\nqc1.x(0)\nqc1.y(0)\nqc1.cx(0,1)\nqc2.h(0)\nqc2.h(0)\nqc2.h(1)\nqc2.cx(0,1)\nprint(qc1)\nprint(qc2)\n\n                    \nqc1 = transpile(qc1, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=2)\n                        \nqc2 = transpile(qc2, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=2)\n                        "
            )
            test_results = [
                {
                    'source_file': test_sf, 
                    'result_static_analysis': 'Risultato quantum smell LPQ: 0\nRisultato quantum smell NC: 0\n', 
                    'results_dynamic_analysis': [
                        ResultDynamicAnalysis(
                            1, 
                            'qc1', 
                            1, 
"""[[None  1     2    ]
 [qb-0  rz(float) cx() ]
 [qb-1  '' cx() ]
 [cb-0  '' '']
 [cb-1  '' '']]""",
"""Risultato quantum smell IdQ: 0
Risultato quantum smell IQ: 0
Risultato quantum smell IM: 0
Risultato quantum smell LC: 4
Risultato quantum smell ROC: 0
Risultato quantum smell CG: 0\n""", 
                            1
                        ), 
                        ResultDynamicAnalysis(
                            2, 
                            'qc2', 
                            2,
"""[[None  1     2     3     4    ]
 [qb-0  '' '' '' cx() ]
 [qb-1  rz(float) sx()  rz(float) cx() ]
 [cb-0  '' '' '' '']
 [cb-1  '' '' '' '']]""",  
"""Risultato quantum smell IdQ: 0
Risultato quantum smell IQ: 0
Risultato quantum smell IM: 0
Risultato quantum smell LC: 8
Risultato quantum smell ROC: 0
Risultato quantum smell CG: 0\n""", 
                            1
                        )
                    ]
                }
            ]
            test_success = True
            oracle = {
                "q_system": test_qs, 
                "analysis": test_analysis,
                "results": test_results, 
                "success": test_success
            }
            self.assertEqual(result, oracle)

    @patch(utils.PATCH_R_DAO_READ_BY_ID_ANALYSIS)
    def test_it_8_display_analysis_error(self, mock_r_dao_read_by_id_analysis):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            mock_r_dao_read_by_id_analysis.side_effect = mysql.connector.Error
            attributes = {
                'id_qs': 1, 
                'name_qs': "SistemaQuantistico.zip", 
                'save_date': "2023-01-02", 
                'id_analysis': 36, 
                'name_transpilation': "ibm_perth", 
                'optimization': 2
            }
            result = self.service.display_analysis(attributes)
            oracle = {'success': None, 'error': "Errore durante la visualizzazione dell\'analisi. Riprova."}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_r_dao_read_by_id_analysis.call_count, 1)

    """ Test deletion_analysis """

    def test_it_9_deletion_analysis_success(self):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            attributes = {
                'id_analysis': 1, 
                'name_transpilation': 'ibm_perth', 
                'id_qs': 1
            }
            result = self.service.deletion_analysis(attributes)
            oracle = {'success': True}
            self.assertEqual(result, oracle)
    
    @patch(utils.PATCH_A_DAO_DELETE_BY_ID)
    def test_it_10_deletion_analysis_error(self, mock_a_dao_delete_by_id):
        with app.test_request_context() as c:
            session['email'] = 'cc_90@test.test'
            session['actor'] = 'registered user'
            mock_a_dao_delete_by_id.side_effect = mysql.connector.Error
            attributes = {
                'id_analysis': 1, 
                'name_transpilation': 'ibm_perth', 
                'id_qs': 1
            }
            result = self.service.deletion_analysis(attributes)
            oracle = {'success': None, 'error': "Errore durante l'eliminazione dell'analisi selezionata. Riprova."}
            self.assertEqual(result, oracle)
            self.assertEqual(mock_a_dao_delete_by_id.call_count, 1)






