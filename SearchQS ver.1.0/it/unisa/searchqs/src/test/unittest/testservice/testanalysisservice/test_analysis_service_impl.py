import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import patch, MagicMock
from src.main.service.analysisservice.analysis_service_impl import AnalysisServiceImpl
import src.test.utils.utils as utils
from werkzeug.datastructures import FileStorage
from src.main.view.app import *
from src.main.model.entity.source_file import SourceFile
from src.main.model.entity.result_dynamic_analysis import ResultDynamicAnalysis
from src.main.model.entity.result import Result
from src.main.model.entity.q_system import QSystem
from src.main.model.entity.analysis import Analysis

class TestAnalysisServiceImpl(unittest.TestCase):
    service = AnalysisServiceImpl()

    """ Test loading_q_system """

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CF_CHECK_LOADING_Q_SYSTEM)
    @patch(utils.PATCH_QS_DAO_READ_BY_NAME_AND_EMAIL_REGISTERED_USER)
    @patch(utils.PATCH_QS_DAO_CREATE)
    @patch(utils.PATCH_QS_DAO_READ_ID_BY_ATTRIBUTES)
    @patch(utils.PATCH_OS_MAKEDIRS)
    @patch(utils.PATCH_OS_PATH_JOIN)
    @patch(utils.PATCH_ZIPFILE)
    @patch(utils.PATCH_SUBPROCESS_RUN)
    @patch(utils.PATCH_GLOB)
    @patch(utils.PATCH_JSON_DUMPS)
    def test_1_loading_q_system_with_create_qs_success(self, mock_json_dumps, mock_glob, mock_subprocess_run, 
                                                     mock_zipfile, mock_os_path_join, 
                                                     mock_os_makedirs, mock_qs_dao_read_id_by_attributes, 
                                                     mock_qs_dao_create, 
                                                     mock_qs_dao_read_by_name_and_email_registered_user, 
                                                     mock_cf_check_loading_q_system,
                                                     mock_connection_commit, mock_connection_start_transaction, 
                                                     mock_connection_close, mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_cf_check_loading_q_system.return_value = [{}, 0]
            mock_qs_dao_read_by_name_and_email_registered_user.return_value = []
            mock_qs_dao_create.return_value = True
            mock_qs_dao_read_id_by_attributes.return_value = 10
            mock_os_makedirs.return_value = None
            mock_os_path_join.side_effect = ["join1", "join2", "join3", "join4"]
            mock_zipfile.return_value = MagicMock()
            mock_subprocess_run.side_effect = [None, None, None]
            mock_glob.return_value = ["app_10/TestSistemaQuantistico/file1.py", "app_10/TestSistemaQuantistico/file2.py", "app_10/TestSistemaQuantistico/file3.py"]
            mock_json_dumps.return_value = '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}'
            mock_connection_commit.return_value = MagicMock()
            mock_connection_close.return_value = True

            session['email'] = "test@test.test"
            mock_zipfile.extractall.return_value = None
            attributes = {
                'file': MagicMock(),
                'filename': "TestSistemaQuantistico.zip", 
            }
            oracle = {
                'success': True,
                'python_files': ["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"], 
                'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}', 
                'id_qs': 10, 
                'name_qs': "TestSistemaQuantistico.zip", 
                'num_errors': 0
            }
            result = self.service.loading_q_system(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_json_dumps.call_count, 2)
            self.assertEqual(mock_glob.call_count, 1)
            self.assertEqual(mock_subprocess_run.call_count, 3)
            self.assertEqual(mock_zipfile.call_count, 1)
            self.assertEqual(mock_os_path_join.call_count, 4)
            self.assertEqual(mock_os_makedirs.call_count, 1)
            self.assertEqual(mock_qs_dao_read_id_by_attributes.call_count, 1)
            self.assertEqual(mock_qs_dao_create.call_count, 1)
            self.assertEqual(mock_qs_dao_read_by_name_and_email_registered_user.call_count, 1)
            self.assertEqual(mock_cf_check_loading_q_system.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CF_CHECK_LOADING_Q_SYSTEM)
    @patch(utils.PATCH_QS_DAO_READ_BY_NAME_AND_EMAIL_REGISTERED_USER)
    @patch(utils.PATCH_QS_DAO_CREATE)
    @patch(utils.PATCH_QS_DAO_READ_ID_BY_ATTRIBUTES)
    @patch(utils.PATCH_OS_MAKEDIRS)
    @patch(utils.PATCH_OS_PATH_JOIN)
    @patch(utils.PATCH_ZIPFILE)
    @patch(utils.PATCH_SUBPROCESS_RUN)
    @patch(utils.PATCH_GLOB)
    @patch(utils.PATCH_JSON_DUMPS)
    def test_2_loading_q_system_without_create_qs_success(self, mock_json_dumps, mock_glob, mock_subprocess_run, 
                                                     mock_zipfile, mock_os_path_join, 
                                                     mock_os_makedirs, mock_qs_dao_read_id_by_attributes, 
                                                     mock_qs_dao_create, 
                                                     mock_qs_dao_read_by_name_and_email_registered_user, 
                                                     mock_cf_check_loading_q_system,
                                                     mock_connection_commit, mock_connection_start_transaction, 
                                                     mock_connection_close, mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_cf_check_loading_q_system.return_value = [{}, 0]
            mock_qs_dao_read_by_name_and_email_registered_user.return_value = QSystem(10, "TestSistemaQuantistico.zip", 
                                                                                      "test@test.test")
            mock_os_makedirs.return_value = None
            mock_os_path_join.side_effect = ["join1", "join2", "join3", "join4"]
            mock_zipfile.return_value = MagicMock()
            mock_subprocess_run.side_effect = [None, None, None]
            mock_glob.return_value = ["app_10/TestSistemaQuantistico/file1.py", "app_10/TestSistemaQuantistico/file2.py", "app_10/TestSistemaQuantistico/file3.py"]
            mock_json_dumps.return_value = '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}'
            mock_connection_commit.return_value = MagicMock()
            mock_connection_close.return_value = True

            session['email'] = "test@test.test"
            mock_zipfile.extractall.return_value = None
            attributes = {
                'file': MagicMock(),
                'filename': "TestSistemaQuantistico.zip", 
            }
            oracle = {
                'success': True,
                'python_files': ["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"], 
                'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}', 
                'id_qs': 10, 
                'name_qs': "TestSistemaQuantistico.zip", 
                'num_errors': 0
            }
            result = self.service.loading_q_system(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_json_dumps.call_count, 2)
            self.assertEqual(mock_glob.call_count, 1)
            self.assertEqual(mock_subprocess_run.call_count, 3)
            self.assertEqual(mock_zipfile.call_count, 1)
            self.assertEqual(mock_os_path_join.call_count, 4)
            self.assertEqual(mock_os_makedirs.call_count, 1)
            self.assertEqual(mock_qs_dao_read_id_by_attributes.call_count, 0)
            self.assertEqual(mock_qs_dao_create.call_count, 0)
            self.assertEqual(mock_qs_dao_read_by_name_and_email_registered_user.call_count, 1)
            self.assertEqual(mock_cf_check_loading_q_system.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK)
    @patch(utils.PATCH_CF_CHECK_LOADING_Q_SYSTEM)
    @patch(utils.PATCH_QS_DAO_READ_BY_NAME_AND_EMAIL_REGISTERED_USER)
    @patch(utils.PATCH_QS_DAO_CREATE)
    @patch(utils.PATCH_QS_DAO_READ_ID_BY_ATTRIBUTES)
    @patch(utils.PATCH_OS_MAKEDIRS)
    @patch(utils.PATCH_OS_PATH_JOIN)
    @patch(utils.PATCH_ZIPFILE)
    @patch(utils.PATCH_SUBPROCESS_RUN)
    @patch(utils.PATCH_GLOB)
    @patch(utils.PATCH_JSON_DUMPS)
    def test_3_loading_q_system_failure(self, mock_json_dumps, mock_glob, mock_subprocess_run, 
                                                        mock_zipfile, mock_os_path_join, 
                                                        mock_os_makedirs, mock_qs_dao_read_id_by_attributes, 
                                                        mock_qs_dao_create, 
                                                        mock_qs_dao_read_by_name_and_email_registered_user, 
                                                        mock_cf_check_loading_q_system, mock_connection_rollback, 
                                                        mock_connection_commit, mock_connection_start_transaction, 
                                                        mock_connection_close, mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_cf_check_loading_q_system.return_value = [
                {'file': "Il sistema quantistico caricato non è del tipo .zip.\n"}, 1
            ]
            mock_connection_rollback.return_value = MagicMock()
            mock_connection_close.return_value = True

            session['email'] = "test@test.test"
            mock_zipfile.extractall.return_value = None
            attributes = {
                'file': MagicMock(),
                'filename': "TestSistemaQuantistico.zip", 
            }
            oracle = {
                'success': False, 
                'errors': {'file': "Il sistema quantistico caricato non è del tipo .zip.\n"}, 
                'num_errors': 1
            }
            result = self.service.loading_q_system(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_json_dumps.call_count, 1)
            self.assertEqual(mock_glob.call_count, 0)
            self.assertEqual(mock_subprocess_run.call_count, 0)
            self.assertEqual(mock_zipfile.call_count, 0)
            self.assertEqual(mock_os_path_join.call_count, 0)
            self.assertEqual(mock_os_makedirs.call_count, 0)
            self.assertEqual(mock_qs_dao_read_id_by_attributes.call_count, 0)
            self.assertEqual(mock_qs_dao_create.call_count, 0)
            self.assertEqual(mock_qs_dao_read_by_name_and_email_registered_user.call_count, 0)
            self.assertEqual(mock_cf_check_loading_q_system.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 0)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK, return_value = MagicMock())
    @patch(utils.PATCH_CF_CHECK_LOADING_Q_SYSTEM)
    @patch(utils.PATCH_QS_DAO_READ_BY_NAME_AND_EMAIL_REGISTERED_USER)
    @patch(utils.PATCH_QS_DAO_CREATE)
    @patch(utils.PATCH_QS_DAO_READ_ID_BY_ATTRIBUTES)
    @patch(utils.PATCH_OS_MAKEDIRS)
    @patch(utils.PATCH_OS_PATH_JOIN)
    @patch(utils.PATCH_ZIPFILE)
    @patch(utils.PATCH_SUBPROCESS_RUN)
    @patch(utils.PATCH_GLOB)
    @patch(utils.PATCH_JSON_DUMPS)
    def test_4_loading_q_system_with_create_qs_error(self, mock_json_dumps, mock_glob, mock_subprocess_run, 
                                                     mock_zipfile, mock_os_path_join, 
                                                     mock_os_makedirs, mock_qs_dao_read_id_by_attributes, 
                                                     mock_qs_dao_create, 
                                                     mock_qs_dao_read_by_name_and_email_registered_user, 
                                                     mock_cf_check_loading_q_system, mock_connection_rollback, 
                                                     mock_connection_commit, mock_connection_start_transaction, 
                                                     mock_connection_close, mock_connection_open):
        with app.test_request_context():
            mock_connection_open.return_value = True
            mock_connection_start_transaction.return_value = MagicMock()
            mock_cf_check_loading_q_system.return_value = [{}, 0]
            mock_qs_dao_read_by_name_and_email_registered_user.return_value = []
            mock_qs_dao_create.side_effect = Exception
            mock_connection_rollback.return_value = MagicMock()
            mock_connection_close.return_value = True

            session['email'] = "test@test.test"
            mock_zipfile.extractall.return_value = None
            attributes = {
                'file': MagicMock(),
                'filename': "TestSistemaQuantistico.zip", 
            }
            oracle = {'success': None, 'error': "Errore durante il caricamento del sistema quantistico. Riprova."}
            result = self.service.loading_q_system(attributes)
            self.assertEqual(result, oracle)
            self.assertEqual(mock_json_dumps.call_count, 1)
            self.assertEqual(mock_glob.call_count, 0)
            self.assertEqual(mock_subprocess_run.call_count, 0)
            self.assertEqual(mock_zipfile.call_count, 0)
            self.assertEqual(mock_os_path_join.call_count, 0)
            self.assertEqual(mock_os_makedirs.call_count, 0)
            self.assertEqual(mock_qs_dao_read_id_by_attributes.call_count, 0)
            self.assertEqual(mock_qs_dao_create.call_count, 1)
            self.assertEqual(mock_qs_dao_read_by_name_and_email_registered_user.call_count, 1)
            self.assertEqual(mock_cf_check_loading_q_system.call_count, 1)
            self.assertEqual(mock_connection_commit.call_count, 0)
            self.assertEqual(mock_connection_rollback.call_count, 1)
            self.assertEqual(mock_connection_start_transaction.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    """ Test execution_analyses """

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK)
    @patch(utils.PATCH_CF_CHECK_EXECUTION_ANALYSES)
    @patch(utils.PATCH_FILE_OPEN)
    @patch(utils.PATCH_SF_DAO_READ_BY_PARAMS)
    @patch(utils.PATCH_SF_DAO_CREATE)
    @patch(utils.PATCH_A_OP_GET_NAMES_Q_CIRCUITS_FROM_FILE)
    @patch(utils.PATCH_A_DAO_CREATE)
    @patch(utils.PATCH_A_DAO_READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE)
    @patch(utils.PATCH_A_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_A_OP_GET_RESULT_STATIC_ANALYSIS)
    @patch(utils.PATCH_R_DAO_CREATE)
    @patch(utils.PATCH_R_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_A_OP_GET_RESULTS_DYNAMIC_ANALYSIS)
    @patch(utils.PATCH_RDA_DAO_CREATE)
    def test_5_execution_analyses_success(self, mock_rda_dao_create, mock_a_op_get_results_dynamic_analysis, 
                                        mock_r_dao_read_id_by_params, mock_r_dao_create, 
                                        mock_a_op_get_result_static_analysis, mock_a_dao_read_id_by_params, 
                                        mock_a_dao_read_id_by_params_with_name_transpilation_none, mock_a_dao_create, 
                                        mock_a_op_get_names_q_circuits_from_file, mock_sf_dao_create, 
                                        mock_sf_dao_read_by_params, mock_file_open, 
                                        mock_cf_check_execution_analyses, mock_connection_rollback, 
                                        mock_connection_commit, mock_connection_start_transaction, 
                                        mock_connection_close, mock_connection_open):
        
        mock_connection_open.return_value = True
        mock_connection_start_transaction.return_value = MagicMock()
        mock_cf_check_execution_analyses.return_value = [{}, 0]
        mock_file_open.side_effect = [
            MagicMock(read_data='print("Contenuto file 1")')(),
            MagicMock(read_data='print("Contenuto file 2")')(),
            MagicMock(read_data='print("Contenuto file 3")')()
        ]
        test_source_files = [
            SourceFile(1, "TestSistemaQuantistico/file1.py", ""),
            SourceFile(2, "TestSistemaQuantistico/file2.py", ""),
            SourceFile(3, "TestSistemaQuantistico/file3.py", "")
        ]
        test_source_files[0].set_file_from_code('print("Contenuto file 1")')
        test_source_files[1].set_file_from_code('print("Contenuto file 2")')
        test_source_files[2].set_file_from_code('print("Contenuto file 3")')
        mock_sf_dao_read_by_params.side_effect = [
            test_source_files[0],
            [],
            test_source_files[1],
            [],
            test_source_files[2]
        ]
        mock_sf_dao_create.side_effect = [True, True]
        mock_a_op_get_names_q_circuits_from_file.side_effect = [['circuit'], ['qc_1', 'qc_2'], ['circuito']]
        mock_a_dao_create.side_effect = [True, True, True]
        mock_a_dao_read_id_by_params_with_name_transpilation_none.return_value = 11
        mock_a_dao_read_id_by_params.side_effect = [12, 13]
        mock_a_op_get_result_static_analysis.side_effect = [
            "Risultato analisi statica transpilazione 1 file 1", "Risultato analisi statica transpilazione 1 file 2", 
            "Risultato analisi statica transpilazione 1 file 3", "Risultato analisi statica transpilazione 2 file 1", 
            "Risultato analisi statica transpilazione 2 file 2", "Risultato analisi statica transpilazione 2 file 3", 
            "Risultato analisi statica transpilazione 3 file 1", "Risultato analisi statica transpilazione 3 file 2", 
            "Risultato analisi statica transpilazione 3 file 3"
        ]
        mock_r_dao_create.side_effect = [True, True, True, True, True, True, True, True, True]
        mock_r_dao_read_id_by_params.return_value = [21, 22, 23, 24, 25, 26, 27, 28, 29]
        mock_a_op_get_results_dynamic_analysis.side_effect = [
            [
                ResultDynamicAnalysis(31, "circuit", 1, "Matrice circuit transpilazione 1", "Risultato circuit transpilazione 1", 21)
            ],
            [
                ResultDynamicAnalysis(32, "qc_1", 1, "Matrice qc_1 transpilazione 1", "Risultato qc_1 transpilazione 1", 22), 
                ResultDynamicAnalysis(33, "qc_2", 2, "Matrice qc_2 transpilazione 1", "Risultato qc_2 transpilazione 1", 22)
            ],
            [
                ResultDynamicAnalysis(34, "circuito", 1, "Matrice circuito transpilazione 1", "Risultato circuito transpilazione 1", 23)
            ],
            
            [
                ResultDynamicAnalysis(35, "circuit", 1, "Matrice circuit transpilazione 2", "Risultato circuit transpilazione 2", 24)
            ],
            [
                ResultDynamicAnalysis(36, "qc_1", 1, "Matrice qc_1 transpilazione 2", "Risultato qc_1 transpilazione 2", 25), 
                ResultDynamicAnalysis(37, "qc_2", 2, "Matrice qc_2 transpilazione 2", "Risultato qc_2 transpilazione 2", 25)
            ],
            [
                ResultDynamicAnalysis(38, "circuito", 1, "Matrice circuito transpilazione 2", "Risultato circuito transpilazione 2", 26)
            ],

            [
                ResultDynamicAnalysis(39, "circuit", 1, "Matrice circuit transpilazione 3", "Risultato circuit transpilazione 3", 27)
            ],
            [
                ResultDynamicAnalysis(40, "qc1", 1, "Matrice qc_1 transpilazione 3", "Risultato qc_1 transpilazione 3", 28), 
                ResultDynamicAnalysis(41, "qc_2", 2, "Matrice qc_2 transpilazione 3", "Risultato qc_2 transpilazione 3", 28)
            ],
            [
                ResultDynamicAnalysis(42, "circuito", 1, "Matrice circuito transpilazione 3", "Risultato circuito transpilazione 3", 29)
            ],
        ]
        mock_rda_dao_create.side_effect = [True, True, True, True, True, True, True, True, True, True, True, True]
        mock_connection_commit.return_value = MagicMock()
        mock_connection_close.return_value = True

        attributes = {
            'id_qs': 6, 
            'name_qs': "TestSistemaQuantistico.zip",
            'optimization': 2,
            'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}',
            'transpilations_json': '{"None", "ibm_perth", "simple"}',
            'files_selected': ["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"],
            'transpilations_selected': ["None", "ibm_perth", "simple"],
        }
        result = self.service.execution_analyses(attributes)
        oracle = {
            'success': True, 
            'transpilations': ['original', 'simple', 'ibm_perth', 'ibm_sherbroke', 'rpcx']
        }
        self.assertEqual(result, oracle)
        self.assertEqual(mock_rda_dao_create.call_count, 12)
        self.assertEqual(mock_a_op_get_results_dynamic_analysis.call_count, 9)
        self.assertEqual(mock_r_dao_read_id_by_params.call_count, 9)
        self.assertEqual(mock_r_dao_create.call_count, 9)
        self.assertEqual(mock_a_op_get_result_static_analysis.call_count, 9)
        self.assertEqual(mock_a_dao_read_id_by_params.call_count, 2)
        self.assertEqual(mock_a_dao_read_id_by_params_with_name_transpilation_none.call_count, 1)
        self.assertEqual(mock_a_dao_create.call_count, 3)
        self.assertEqual(mock_a_op_get_names_q_circuits_from_file.call_count, 3)
        self.assertEqual(mock_sf_dao_create.call_count, 2)
        self.assertEqual(mock_sf_dao_read_by_params.call_count, 5)
        self.assertEqual(mock_file_open.call_count, 3)
        self.assertEqual(mock_cf_check_execution_analyses.call_count, 1)
        self.assertEqual(mock_connection_rollback.call_count, 0)
        self.assertEqual(mock_connection_commit.call_count, 1)
        self.assertEqual(mock_connection_start_transaction.call_count, 1)
        self.assertEqual(mock_connection_close.call_count, 1)
        self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK)
    @patch(utils.PATCH_CF_CHECK_EXECUTION_ANALYSES)
    @patch(utils.PATCH_FILE_OPEN)
    @patch(utils.PATCH_SF_DAO_READ_BY_PARAMS)
    @patch(utils.PATCH_SF_DAO_CREATE)
    @patch(utils.PATCH_A_OP_GET_NAMES_Q_CIRCUITS_FROM_FILE)
    @patch(utils.PATCH_A_DAO_CREATE)
    @patch(utils.PATCH_A_DAO_READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE)
    @patch(utils.PATCH_A_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_A_OP_GET_RESULT_STATIC_ANALYSIS)
    @patch(utils.PATCH_R_DAO_CREATE)
    @patch(utils.PATCH_R_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_A_OP_GET_RESULTS_DYNAMIC_ANALYSIS)
    @patch(utils.PATCH_RDA_DAO_CREATE)
    def test_6_execution_analyses_error(self, mock_rda_dao_create, mock_a_op_get_results_dynamic_analysis, 
                                        mock_r_dao_read_id_by_params, mock_r_dao_create, 
                                        mock_a_op_get_result_static_analysis, mock_a_dao_read_id_by_params, 
                                        mock_a_dao_read_id_by_params_with_name_transpilation_none, mock_a_dao_create, 
                                        mock_a_op_get_names_q_circuits_from_file, mock_sf_dao_create, 
                                        mock_sf_dao_read_by_params, mock_file_open, 
                                        mock_cf_check_execution_analyses, mock_connection_rollback, 
                                        mock_connection_commit, mock_connection_start_transaction, 
                                        mock_connection_close, mock_connection_open):
        
        mock_connection_open.return_value = True
        mock_connection_start_transaction.return_value = MagicMock()
        mock_cf_check_execution_analyses.return_value = [{}, 0]
        mock_file_open.side_effect = [
            MagicMock(read_data='print("Contenuto file 1")')(),
            MagicMock(read_data='print("Contenuto file 2")')(),
            MagicMock(read_data='print("Contenuto file 3")')()
        ]
        test_source_files = [
            SourceFile(1, "TestSistemaQuantistico/file1.py", ""),
            SourceFile(2, "TestSistemaQuantistico/file2.py", ""),
            SourceFile(3, "TestSistemaQuantistico/file3.py", "")
        ]
        test_source_files[0].set_file_from_code('print("Contenuto file 1")')
        test_source_files[1].set_file_from_code('print("Contenuto file 2")')
        test_source_files[2].set_file_from_code('print("Contenuto file 3")')
        mock_sf_dao_read_by_params.side_effect = [test_source_files[0], []]
        mock_sf_dao_create.side_effect = Exception
        mock_a_op_get_names_q_circuits_from_file.return_value = ['circuit']
        mock_connection_rollback.return_value = MagicMock()
        mock_connection_close.return_value = True

        attributes = {
            'id_qs': 6, 
            'name_qs': "TestSistemaQuantistico.zip",
            'optimization': 2,
            'files_json': '{"TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"}',
            'transpilations_json': '{"None", "ibm_perth", "simple"}',
            'files_selected': ["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"],
            'transpilations_selected': ["None", "ibm_perth", "simple"],
        }
        result = self.service.execution_analyses(attributes)
        oracle = {'success': None, 'error': "Errore durante l\'esecuzone delle analisi. Riprova."}
        self.assertEqual(result, oracle)
        self.assertEqual(mock_rda_dao_create.call_count, 0)
        self.assertEqual(mock_a_op_get_results_dynamic_analysis.call_count, 0)
        self.assertEqual(mock_r_dao_read_id_by_params.call_count, 0)
        self.assertEqual(mock_r_dao_create.call_count, 0)
        self.assertEqual(mock_a_op_get_result_static_analysis.call_count, 0)
        self.assertEqual(mock_a_dao_read_id_by_params.call_count, 0)
        self.assertEqual(mock_a_dao_read_id_by_params_with_name_transpilation_none.call_count, 0)
        self.assertEqual(mock_a_dao_create.call_count, 0)
        self.assertEqual(mock_a_op_get_names_q_circuits_from_file.call_count, 1)
        self.assertEqual(mock_sf_dao_create.call_count, 1)
        self.assertEqual(mock_sf_dao_read_by_params.call_count, 2)
        self.assertEqual(mock_file_open.call_count, 3)
        self.assertEqual(mock_cf_check_execution_analyses.call_count, 1)
        self.assertEqual(mock_connection_rollback.call_count, 1)
        self.assertEqual(mock_connection_commit.call_count, 0)
        self.assertEqual(mock_connection_start_transaction.call_count, 1)
        self.assertEqual(mock_connection_close.call_count, 1)
        self.assertEqual(mock_connection_open.call_count, 1)
    
    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK)
    @patch(utils.PATCH_CF_CHECK_EXECUTION_ANALYSES)
    @patch(utils.PATCH_FILE_OPEN)
    @patch(utils.PATCH_SF_DAO_READ_BY_PARAMS)
    @patch(utils.PATCH_SF_DAO_CREATE)
    @patch(utils.PATCH_A_OP_GET_NAMES_Q_CIRCUITS_FROM_FILE)
    @patch(utils.PATCH_A_DAO_CREATE)
    @patch(utils.PATCH_A_DAO_READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE)
    @patch(utils.PATCH_A_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_A_OP_GET_RESULT_STATIC_ANALYSIS)
    @patch(utils.PATCH_R_DAO_CREATE)
    @patch(utils.PATCH_R_DAO_READ_ID_BY_PARAMS)
    @patch(utils.PATCH_A_OP_GET_RESULTS_DYNAMIC_ANALYSIS)
    @patch(utils.PATCH_RDA_DAO_CREATE)
    def test_7_execution_analyses_failure(self, mock_rda_dao_create, mock_a_op_get_results_dynamic_analysis, 
                                        mock_r_dao_read_id_by_params, mock_r_dao_create, 
                                        mock_a_op_get_result_static_analysis, mock_a_dao_read_id_by_params, 
                                        mock_a_dao_read_id_by_params_with_name_transpilation_none, mock_a_dao_create, 
                                        mock_a_op_get_names_q_circuits_from_file, mock_sf_dao_create, 
                                        mock_sf_dao_read_by_params, mock_file_open, 
                                        mock_cf_check_execution_analyses, mock_connection_rollback, 
                                        mock_connection_commit, mock_connection_start_transaction, 
                                        mock_connection_close, mock_connection_open):
        
        mock_connection_open.return_value = True
        mock_connection_start_transaction.return_value = MagicMock()
        mock_cf_check_execution_analyses.return_value = [
            {'files_selected': "Nessun file selezionato. Seleziona almeno un file.\n"}, 1
        ]

        attributes = {
            'id_qs': 6, 
            'name_qs': "TestSistemaQuantistico.zip",
            'optimization': 2,
            'files_json': '["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"]',
            'transpilations_json': '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]',
            'files_selected': [],
            'transpilations_selected': ["None", "ibm_perth", "simple"]
        }
        result = self.service.execution_analyses(attributes)
        oracle = {
            'success': False,
            'id_qs': 6,
            'name_qs':"TestSistemaQuantistico.zip",
            'errors': {'files_selected': "Nessun file selezionato. Seleziona almeno un file.\n"}, 
            'num_errors': 1, 
            'files_json': '["TestSistemaQuantistico/file1.py", "TestSistemaQuantistico/file2.py", "TestSistemaQuantistico/file3.py"]',
            'transpilations_json': '["original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"]',
            'python_files': ['TestSistemaQuantistico/file1.py', 'TestSistemaQuantistico/file2.py', 'TestSistemaQuantistico/file3.py'],
            'transpilations': ['original', 'simple', 'ibm_perth', 'ibm_sherbroke', 'rpcx']
        }
        self.assertEqual(result, oracle)
        self.assertEqual(mock_rda_dao_create.call_count, 0)
        self.assertEqual(mock_a_op_get_results_dynamic_analysis.call_count, 0)
        self.assertEqual(mock_r_dao_read_id_by_params.call_count, 0)
        self.assertEqual(mock_r_dao_create.call_count, 0)
        self.assertEqual(mock_a_op_get_result_static_analysis.call_count, 0)
        self.assertEqual(mock_a_dao_read_id_by_params.call_count, 0)
        self.assertEqual(mock_a_dao_read_id_by_params_with_name_transpilation_none.call_count, 0)
        self.assertEqual(mock_a_dao_create.call_count, 0)
        self.assertEqual(mock_a_op_get_names_q_circuits_from_file.call_count, 0)
        self.assertEqual(mock_sf_dao_create.call_count, 0)
        self.assertEqual(mock_sf_dao_read_by_params.call_count, 0)
        self.assertEqual(mock_file_open.call_count, 0)
        self.assertEqual(mock_cf_check_execution_analyses.call_count, 1)
        self.assertEqual(mock_connection_rollback.call_count, 1)
        self.assertEqual(mock_connection_commit.call_count, 0)
        self.assertEqual(mock_connection_start_transaction.call_count, 1)
        self.assertEqual(mock_connection_close.call_count, 1)
        self.assertEqual(mock_connection_open.call_count, 1)
    


    """ Test display_analysis """

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_R_DAO_READ_BY_ID_ANALYSIS)
    @patch(utils.PATCH_SF_DAO_READ_BY_ID)
    @patch(utils.PATCH_RDA_DAO_READ_BY_ID_RESULT)
    def test_8_display_analysis_success(self, mock_rda_dao_read_by_id_result, mock_sf_dao_read_by_id, 
                                      mock_r_dao_read_by_id_analysis, mock_connection_close, mock_connection_open):
        with app.test_request_context():
            session['email'] = "test@test.test"
            mock_connection_open.return_value = True
            mock_r_dao_read_by_id_analysis.return_value = [
                Result(24, "Risultato analisi statica transpilazione 2 file 1", 12, 1),
                Result(25, "Risultato analisi statica transpilazione 2 file 2", 12, 2),
                Result(26, "Risultato analisi statica transpilazione 2 file 3", 12, 3),
            ]
            test_source_files = [
                SourceFile(1, "TestSistemaQuantistico/file1.py", ""),
                SourceFile(2, "TestSistemaQuantistico/file2.py", ""),
                SourceFile(3, "TestSistemaQuantistico/file3.py", "")
            ]
            test_source_files[0].set_file_from_code('print("Contenuto file 1")')
            test_source_files[1].set_file_from_code('print("Contenuto file 2")')
            test_source_files[2].set_file_from_code('print("Contenuto file 3")')
            mock_sf_dao_read_by_id.side_effect = [test_source_files[0], test_source_files[1], test_source_files[2]]
            mock_rda_dao_read_by_id_result.side_effect = [
                [
                    ResultDynamicAnalysis(35, "circuit", 1, "Matrice circuit transpilazione 2", "Risultato circuit transpilazione 2", 24)
                ],
                [
                    ResultDynamicAnalysis(36, "qc_1", 1, "Matrice qc_1 transpilazione 2", "Risultato qc_1 transpilazione 2", 25), 
                    ResultDynamicAnalysis(37, "qc_2", 2, "Matrice qc_2 transpilazione 2", "Risultato qc_2 transpilazione 2", 25)
                ],
                [
                    ResultDynamicAnalysis(38, "circuito", 1, "Matrice circuito transpilazione 2", "Risultato circuito transpilazione 2", 26)
                ],
            ]
            mock_connection_close.return_value = True

            attributes = {
                'id_qs': 6, 
                'name_qs': "TestSistemaQuantistico.zip", 
                'save_date': "2023-10-12 10:30:20:", 
                'id_analysis': 12, 
                'name_transpilation': "ibm_perth", 
                'optimization': 2
            }

            oracle = {
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
            result = self.service.display_analysis(attributes)

            self.assertEqual(result, oracle)
            self.assertEqual(mock_rda_dao_read_by_id_result.call_count, 3)
            self.assertEqual(mock_sf_dao_read_by_id.call_count, 3)
            self.assertEqual(mock_r_dao_read_by_id_analysis.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_R_DAO_READ_BY_ID_ANALYSIS)
    @patch(utils.PATCH_SF_DAO_READ_BY_ID)
    @patch(utils.PATCH_RDA_DAO_READ_BY_ID_RESULT)
    def test_9_display_analysis_error(self, mock_rda_dao_read_by_id_result, mock_sf_dao_read_by_id, 
                                      mock_r_dao_read_by_id_analysis, mock_connection_close, mock_connection_open):
        with app.test_request_context():
            session['email'] = "test@test.test"
            mock_connection_open.return_value = True
            mock_r_dao_read_by_id_analysis.side_effect = Exception
            mock_connection_close.return_value = True

            attributes = {
                'id_qs': 6, 
                'name_qs': "TestSistemaQuantistico.zip", 
                'save_date': "2023-10-12 10:30:20:", 
                'id_analysis': 12, 
                'name_transpilation': "ibm_perth", 
                'optimization': 2
            }

            oracle = {'success': None, 'error': "Errore durante la visualizzazione dell\'analisi. Riprova."}
            result = self.service.display_analysis(attributes)

            self.assertEqual(result, oracle)
            self.assertEqual(mock_rda_dao_read_by_id_result.call_count, 0)
            self.assertEqual(mock_sf_dao_read_by_id.call_count, 0)
            self.assertEqual(mock_r_dao_read_by_id_analysis.call_count, 1)
            self.assertEqual(mock_connection_close.call_count, 1)
            self.assertEqual(mock_connection_open.call_count, 1)


    """ Test deletion_analysis """

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_R_DAO_READ_ID_SOURCE_FILES_BY_ID_ANALYSIS)
    @patch(utils.PATCH_R_DAO_READ_NUM_RESULTS_BY_ID_SOURCE_FILE)
    @patch(utils.PATCH_A_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_A_DAO_READ_NUM_ANALYSES_BY_ID_Q_SYSTEM)
    @patch(utils.PATCH_SF_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_QS_DAO_DELETE_BY_ID)
    def test_10_deletion_analysis_with_deletion_q_system_success(self, mock_qs_dao_delete_by_id, mock_sf_dao_delete_by_id, 
                                                              mock_a_dao_read_num_analyses_by_id_q_system, 
                                                              mock_a_dao_delete_by_id, 
                                                              mock_r_dao_read_num_results_by_id_source_file, 
                                                              mock_r_dao_read_id_source_files_by_id_analysis, 
                                                              mock_connection_commit, mock_connection_start_transaction, 
                                                              mock_connection_close, mock_connection_open):
        mock_connection_open.return_value = True
        mock_connection_start_transaction.return_value = MagicMock()
        mock_r_dao_read_id_source_files_by_id_analysis.return_value = [1, 2, 3]
        mock_a_dao_delete_by_id.return_value = True
        mock_r_dao_read_num_results_by_id_source_file.side_effect = [0, 1, 0]
        mock_sf_dao_delete_by_id.side_effect = [True, True]
        mock_a_dao_read_num_analyses_by_id_q_system.return_value = 0
        mock_qs_dao_delete_by_id.return_value = True
        mock_connection_commit.return_value = MagicMock()
        mock_connection_close.return_value = True

        attributes = {
            'id_analysis': 12, 
            'name_transpilation': "ibm_perth", 
            'id_qs': 6
        }
        result = self.service.deletion_analysis(attributes)
        oracle = {'success': True}
        self.assertEqual(result, oracle)
        self.assertEqual(mock_qs_dao_delete_by_id.call_count, 1)
        self.assertEqual(mock_sf_dao_delete_by_id.call_count, 2)
        self.assertEqual(mock_a_dao_read_num_analyses_by_id_q_system.call_count, 1)
        self.assertEqual(mock_a_dao_delete_by_id.call_count, 1)
        self.assertEqual(mock_r_dao_read_num_results_by_id_source_file.call_count, 3)
        self.assertEqual(mock_r_dao_read_id_source_files_by_id_analysis.call_count, 1)
        self.assertEqual(mock_connection_commit.call_count, 1)
        self.assertEqual(mock_connection_start_transaction.call_count, 1)
        self.assertEqual(mock_connection_close.call_count, 1)
        self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_R_DAO_READ_ID_SOURCE_FILES_BY_ID_ANALYSIS)
    @patch(utils.PATCH_R_DAO_READ_NUM_RESULTS_BY_ID_SOURCE_FILE)
    @patch(utils.PATCH_A_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_A_DAO_READ_NUM_ANALYSES_BY_ID_Q_SYSTEM)
    @patch(utils.PATCH_SF_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_QS_DAO_DELETE_BY_ID)
    def test_11_deletion_analysis_without_deletion_q_system_success(self, mock_qs_dao_delete_by_id, mock_sf_dao_delete_by_id, 
                                                              mock_a_dao_read_num_analyses_by_id_q_system, 
                                                              mock_a_dao_delete_by_id, 
                                                              mock_r_dao_read_num_results_by_id_source_file, 
                                                              mock_r_dao_read_id_source_files_by_id_analysis, 
                                                              mock_connection_commit, mock_connection_start_transaction, 
                                                              mock_connection_close, mock_connection_open):
        mock_connection_open.return_value = True
        mock_connection_start_transaction.return_value = MagicMock()
        mock_r_dao_read_id_source_files_by_id_analysis.return_value = [1, 2, 3]
        mock_a_dao_delete_by_id.return_value = True
        mock_r_dao_read_num_results_by_id_source_file.side_effect = [0, 1, 0]
        mock_sf_dao_delete_by_id.side_effect = [True, True]
        mock_a_dao_read_num_analyses_by_id_q_system.return_value = 2
        mock_connection_commit.return_value = MagicMock()
        mock_connection_close.return_value = True

        attributes = {
            'id_analysis': 12, 
            'name_transpilation': "ibm_perth", 
            'id_qs': 6
        }
        result = self.service.deletion_analysis(attributes)
        oracle = {'success': True}
        self.assertEqual(result, oracle)
        self.assertEqual(mock_qs_dao_delete_by_id.call_count, 0)
        self.assertEqual(mock_sf_dao_delete_by_id.call_count, 2)
        self.assertEqual(mock_a_dao_read_num_analyses_by_id_q_system.call_count, 1)
        self.assertEqual(mock_a_dao_delete_by_id.call_count, 1)
        self.assertEqual(mock_r_dao_read_num_results_by_id_source_file.call_count, 3)
        self.assertEqual(mock_r_dao_read_id_source_files_by_id_analysis.call_count, 1)
        self.assertEqual(mock_connection_commit.call_count, 1)
        self.assertEqual(mock_connection_start_transaction.call_count, 1)
        self.assertEqual(mock_connection_close.call_count, 1)
        self.assertEqual(mock_connection_open.call_count, 1)

    @patch(utils.PATCH_CONNECTION_OPEN)
    @patch(utils.PATCH_CONNECTION_CLOSE)
    @patch(utils.PATCH_CONNECTION_START_TRANSACTION)
    @patch(utils.PATCH_CONNECTION_COMMIT)
    @patch(utils.PATCH_CONNECTION_ROLLBACK)
    @patch(utils.PATCH_R_DAO_READ_ID_SOURCE_FILES_BY_ID_ANALYSIS)
    @patch(utils.PATCH_R_DAO_READ_NUM_RESULTS_BY_ID_SOURCE_FILE)
    @patch(utils.PATCH_A_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_A_DAO_READ_NUM_ANALYSES_BY_ID_Q_SYSTEM)
    @patch(utils.PATCH_SF_DAO_DELETE_BY_ID)
    @patch(utils.PATCH_QS_DAO_DELETE_BY_ID)
    def test_12_deletion_analysis_error(self, mock_qs_dao_delete_by_id, mock_sf_dao_delete_by_id, 
                                                              mock_a_dao_read_num_analyses_by_id_q_system, 
                                                              mock_a_dao_delete_by_id, 
                                                              mock_r_dao_read_num_results_by_id_source_file, 
                                                              mock_r_dao_read_id_source_files_by_id_analysis, 
                                                              mock_connection_rollback, 
                                                              mock_connection_commit, mock_connection_start_transaction, 
                                                              mock_connection_close, mock_connection_open):
        mock_connection_open.return_value = True
        mock_connection_start_transaction.return_value = MagicMock()
        mock_r_dao_read_id_source_files_by_id_analysis.side_effect = Exception
        mock_connection_rollback.return_value = MagicMock()
        mock_connection_close.return_value = True

        attributes = {
            'id_analysis': 12, 
            'name_transpilation': "ibm_perth", 
            'id_qs': 6
        }
        result = self.service.deletion_analysis(attributes)
        oracle = {'success': None, 'error': "Errore durante l'eliminazione dell'analisi selezionata. Riprova."}
        self.assertEqual(result, oracle)
        self.assertEqual(mock_qs_dao_delete_by_id.call_count, 0)
        self.assertEqual(mock_sf_dao_delete_by_id.call_count, 0)
        self.assertEqual(mock_a_dao_read_num_analyses_by_id_q_system.call_count, 0)
        self.assertEqual(mock_a_dao_delete_by_id.call_count, 0)
        self.assertEqual(mock_r_dao_read_num_results_by_id_source_file.call_count, 0)
        self.assertEqual(mock_r_dao_read_id_source_files_by_id_analysis.call_count, 1)
        self.assertEqual(mock_connection_commit.call_count, 0)
        self.assertEqual(mock_connection_rollback.call_count, 1)
        self.assertEqual(mock_connection_start_transaction.call_count, 1)
        self.assertEqual(mock_connection_close.call_count, 1)
        self.assertEqual(mock_connection_open.call_count, 1)


        
        


    
    
    
        
        
    
    
    
    
        





        
        
        
        
        
        
    







