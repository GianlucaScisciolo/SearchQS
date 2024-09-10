import sys
sys.path.append("../../../..")

import unittest
from unittest.mock import patch, MagicMock
import src.test.utils.utils as utils
from src.main.view.app import *
import responses
from src.main.model.entity.q_system import QSystem
from src.main.model.entity.analysis import Analysis
from src.main.model.entity.result_dynamic_analysis import ResultDynamicAnalysis
from src.main.model.entity.source_file import SourceFile
from werkzeug.datastructures import FileStorage
import io

class TestAnalysisView(unittest.TestCase):
    app_test = app.test_client()
    app_test.testing = True

    """ Test loading_q_system """

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTE_REQUEST_FILE)
    @patch(utils.PATCH_ANALYSIS_SERVICE_LOADING_Q_SYSTEM)
    @patch(utils.PATCH_ANALYSIS_SERVICE_DISPLAY_NAMES_TRANSPILATION)
    def test_loading_q_system_success(self, mock_analysis_service_display_names_transpilation, 
                                      mock_analysis_service_loading_q_system, 
                                      mock_utils_get_attribute_request_file):
        mock_utils_get_attribute_request_file.return_value = FileStorage(stream=io.BytesIO(b"Test sistema"), filename='TestSistemaQuantistico.zip')
        mock_analysis_service_loading_q_system.return_value = {
            'success': True, 
            'python_files': [
                "TestSistemaquantistico/file_1.py", "TestSistemaquantistico/file_2.py", 
                "TestSistemaquantistico/file_3.py"
            ], 
            'files_json': '{"TestSistemaquantistico/file_1.py", "TestSistemaquantistico/file_2.py", "TestSistemaquantistico/file_3.py"}', 
            'id_qs': 12, 
            'name_qs': "TestSistemaQuantistico.zip", 
            'num_errors': 0
        }
        mock_analysis_service_display_names_transpilation.return_value = {
            'success': True, 
            'transpilations': ['original', 'simple', 'ibm_perth', 'ibm_sherbroke', 'rpcx']
        }
        result = self.app_test.post('/loading_q_system', data={'filename': "TestSistemaQuantistico.zip", 
                                                                 'file': mock_utils_get_attribute_request_file.return_value})
        self.assertIn(b"<title>Esecuzione analisi</title>", result.data)
        self.assertEqual(mock_analysis_service_display_names_transpilation.call_count, 1)
        self.assertEqual(mock_analysis_service_loading_q_system.call_count, 1)
        self.assertEqual(mock_utils_get_attribute_request_file.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTE_REQUEST_FILE)
    @patch(utils.PATCH_ANALYSIS_SERVICE_LOADING_Q_SYSTEM)
    def test_loading_q_system_failure(self, mock_analysis_service_loading_q_system,
                                      mock_utils_get_attribute_request_file):
        mock_utils_get_attribute_request_file.return_value = FileStorage(stream=io.BytesIO(b"Test sistema"), filename='TestSistemaQuantistico.rar')

        mock_analysis_service_loading_q_system.return_value = {
            'success': False, 
            'errors': {
                'file': "Il sistema quantistico caricato non è del tipo .zip.\n"
            }, 
            'num_errors': 1
        }
        result = self.app_test.post('/loading_q_system', data={'filename': "TestSistemaQuantistico.rar", 
                                                               'file': mock_utils_get_attribute_request_file.return_value})
        self.assertIn(b"<title>Caricamento sistema quantistico</title>", result.data)
        self.assertEqual(mock_analysis_service_loading_q_system.call_count, 1)
        self.assertEqual(mock_utils_get_attribute_request_file.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTE_REQUEST_FILE)
    @patch(utils.PATCH_ANALYSIS_SERVICE_LOADING_Q_SYSTEM)
    def test_loading_q_system_error(self, mock_analysis_service_loading_q_system,
                                      mock_utils_get_attribute_request_file):
        mock_utils_get_attribute_request_file.return_value = FileStorage(stream=io.BytesIO(b"Test sistema"), filename='TestSistemaQuantistico.zip')
        mock_analysis_service_loading_q_system.return_value = {
            'success': None, 
            'error': "Errore durante il caricamento del sistema quantistico. Riprova."
        }
        result = self.app_test.post('/loading_q_system', data={'filename': "TestSistemaQuantistico.zip", 
                                                               'file': mock_utils_get_attribute_request_file.return_value})
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_analysis_service_loading_q_system.call_count, 1)
        self.assertEqual(mock_utils_get_attribute_request_file.call_count, 1)

    """ Test execution_analyses """

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_ANALYSIS_SERVICE_EXECUTION_ANALYSES)
    def test_execution_analyses_success(self, mock_analysis_service_execution_analyses,  
                                        mock_utils_get_attributes_from_list_of_request):
        
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'id_qs': 12, 
            'name_qs': "TestSistemaQuantistico.zip", 
            'optimization': 2, 
            'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}', 
            'transpilations_json': '{"original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"}',
            'files_selected': ["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py"],
            'transpilations_selected': ["None", "simple", "ibm_perth"],
        } 
        mock_analysis_service_execution_analyses.return_value = {
            'success': True, 
            'transpilations': ["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]
        }
        result = self.app_test.post('/execution_analyses', data=mock_utils_get_attributes_from_list_of_request.return_value)
        self.assertIn(b"<title>Nomi transpilazioni</title>", result.data)
        self.assertEqual(mock_analysis_service_execution_analyses.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)
    
    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_ANALYSIS_SERVICE_EXECUTION_ANALYSES)
    def test_execution_analyses_failure(self, mock_analysis_service_execution_analyses,  
                                        mock_utils_get_attributes_from_list_of_request):
        
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'id_qs': 12, 
            'name_qs': "TestSistemaQuantistico.rar", 
            'optimization': 2, 
            'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}', 
            'transpilations_json': '{"original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"}',
            'files_selected': [],
            'transpilations_selected': ["None", "simple", "ibm_perth"]
        } 
        mock_analysis_service_execution_analyses.return_value = {
                    'success': False,
                    'id_qs': 12,
                    'name_qs':"TestSistemaQuantistico.rar",
                    'errors': {'files_selected': "Nessun file selezionato. Seleziona almeno un file.\n"}, 
                    'num_errors': 1, 
                    'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}',
                    'transpilations_json': '{"original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"}',
                    'python_files': [],
                    'transpilations': ["None", "simple", "ibm_perth"]
                }
        result = self.app_test.post('/execution_analyses', data=mock_utils_get_attributes_from_list_of_request.return_value)
        self.assertIn(b"<title>Esecuzione analisi</title>", result.data)
        self.assertEqual(mock_analysis_service_execution_analyses.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_ANALYSIS_SERVICE_EXECUTION_ANALYSES)
    def test_execution_analyses_error(self, mock_analysis_service_execution_analyses,  
                                        mock_utils_get_attributes_from_list_of_request):
        
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'id_qs': 12, 
            'name_qs': "TestSistemaQuantistico.rar", 
            'optimization': 2, 
            'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}', 
            'transpilations_json': '{"original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"}',
            'files_selected': ["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py"],
            'transpilations_selected': ["None", "simple", "ibm_perth"]
        } 
        mock_analysis_service_execution_analyses.return_value = {'success': None}
        result = self.app_test.post('/execution_analyses', data=mock_utils_get_attributes_from_list_of_request.return_value)
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_analysis_service_execution_analyses.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)
    
    """ Test display_analysis """

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_ANALYSIS_SERVICE_DISPLAY_ANALYSIS)    
    def test_display_analysis_success(self, mock_analysis_service_display_analysis, 
                                       mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'id_qs': 12, 
            'name_qs': "TestSistemaQuantistico.zip", 
            'save_date': "10-05-2023 10-30-20",
            'id_analysis': 6, 
            'name_transpilation': "ibm_perth", 
            'optimization': 2
        }
        test_source_files = [
            SourceFile(1, "TestSistemaQuantistico/file1.py", "", "Salt Hex"),
            SourceFile(2, "TestSistemaQuantistico/file2.py", "", "Salt Hex"),
            SourceFile(3, "TestSistemaQuantistico/file3.py", "", "Salt Hex")
        ]
        test_source_files[0].set_file_from_code('print("Contenuto file 1")')
        test_source_files[1].set_file_from_code('print("Contenuto file 2")')
        test_source_files[2].set_file_from_code('print("Contenuto file 3")')
        mock_analysis_service_display_analysis.return_value = {
            'success': True,
            'q_system': QSystem(6, "TestSistemaQuantistico.zip", "test@test.test"), 
            'analysis': Analysis(12, "ibm_perth", 2, "2023-10-12 10:30:20:", 6),
            'results': [
                {
                    'source_file': test_source_files[0], 
                    'result_static_analysis': "Risultato analisi statica transpilazione 2 file 1", 
                    'results_dynamic_analysis': [
                        ResultDynamicAnalysis(35, "circuit", 1, "Matrice circuit transpilazione 2", "Risultato circuit transpilazione 2", 24)
                    ]
                }, 
                {
                    'source_file': test_source_files[1], 
                    'result_static_analysis': "Risultato analisi statica transpilazione 2 file 2", 
                    'results_dynamic_analysis': [
                        ResultDynamicAnalysis(36, "qc_1", 1, "Matrice qc_1 transpilazione 2", "Risultato qc_1 transpilazione 2", 25), 
                        ResultDynamicAnalysis(37, "qc_2", 2, "Matrice qc_2 transpilazione 2", "Risultato qc_2 transpilazione 2", 25)
                    ]
                }, 
                {
                    'source_file': test_source_files[2], 
                    'result_static_analysis': "Risultato analisi statica transpilazione 2 file 3", 
                    'results_dynamic_analysis': [
                        ResultDynamicAnalysis(38, "circuito", 1, "Matrice circuito transpilazione 2", "Risultato circuito transpilazione 2", 26)
                    ]
                }
            ]
        }
        result = self.app_test.post('/display_analysis', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        self.assertIn(b"<title>Analisi</title>", result.data)
        self.assertEqual(mock_analysis_service_display_analysis.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)
    
    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_ANALYSIS_SERVICE_DISPLAY_ANALYSIS)    
    def test_display_analysis_failure(self, mock_analysis_service_display_analysis, 
                                       mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'id_qs': 12, 
            'name_qs': "TestSistemaQuantistico.zip", 
            'save_date': "10-05-2023 10-30-20",
            'id_analysis': 6, 
            'name_transpilation': "ibm_perth", 
            'optimization': 2
        }
        mock_analysis_service_display_analysis.return_value = {'success': False}
        result = self.app_test.post('/display_analysis', data=mock_utils_get_attributes_from_list_of_request.return_value) 
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_analysis_service_display_analysis.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    """ Test deletion_analysis """

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_ANALYSIS_SERVICE_DELETION_ANALYSIS)
    def test_deletion_analysis_success(self, mock_analysis_service_deletion_analysis, 
                                       mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'id_analysis': 6, 
            'name_transpilation': "ibm_perth", 
            'id_qs': 12
        }
        mock_analysis_service_deletion_analysis.return_value = {'success': True}
        result = self.app_test.post('/deletion_analysis', data=mock_utils_get_attributes_from_list_of_request.return_value)
        
        self.assertIn(b"<title>Analisi tipi di transpilazione</title>", result.data)
        self.assertEqual(mock_analysis_service_deletion_analysis.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    @patch(utils.PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST)
    @patch(utils.PATCH_ANALYSIS_SERVICE_DELETION_ANALYSIS)
    def test_deletion_analysis_error(self, mock_analysis_service_deletion_analysis, 
                                       mock_utils_get_attributes_from_list_of_request):
        mock_utils_get_attributes_from_list_of_request.return_value = {
            'id_analysis': 6, 
            'name_transpilation': "ibm_perth", 
            'id_qs': 12
        }
        mock_analysis_service_deletion_analysis.return_value = {'success': False}
        result = self.app_test.post('/deletion_analysis', data=mock_utils_get_attributes_from_list_of_request.return_value)
        
        self.assertIn(b"<title>Errore</title>", result.data)
        self.assertEqual(mock_analysis_service_deletion_analysis.call_count, 1)
        self.assertEqual(mock_utils_get_attributes_from_list_of_request.call_count, 1)

    def run_tests(self):
        self.test_loading_q_system_success()
        self.test_loading_q_system_failure()
        self.test_loading_q_system_error()
        self.test_execution_analyses_success()
        self.test_execution_analyses_failure()
        self.test_execution_analyses_error()   
        self.test_display_analysis_success()    
        self.test_display_analysis_failure()
        self.test_deletion_analysis_success()
        self.test_deletion_analysis_error()

    








