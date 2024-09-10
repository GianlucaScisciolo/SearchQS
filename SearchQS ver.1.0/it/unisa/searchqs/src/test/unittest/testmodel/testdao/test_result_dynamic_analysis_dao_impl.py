import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock, patch
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.resultdynamicanalysisdao.result_dynamic_analysis_dao_impl import ResultDynamicAnalysisDAOImpl
from src.main.model.entity.result_dynamic_analysis import ResultDynamicAnalysis

class TestResultDynamicAnalysisDAOImpl(unittest.TestCase):
    patch_execute_action = "src.main.model.dao.resultdynamicanalysisdao.result_dynamic_analysis_dao_impl.ResultDynamicAnalysisDAOImpl.execute_action"
    patch_execute_select = "src.main.model.dao.resultdynamicanalysisdao.result_dynamic_analysis_dao_impl.ResultDynamicAnalysisDAOImpl.execute_select"

    """ Test __init__ """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)
        connection.close()

    """ Test create """

    def test_2_create_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            rda_test = ResultDynamicAnalysis(0, "qc", 1, "Matrice circuito quantistico", 
                                           "Risultato analisi dinamica", 2)
            result = dao.create(rda_test)
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.CREATE, ("qc", 1, "Matrice circuito quantistico", 
                                                                          "Risultato analisi dinamica", 2), 1)
            connection.close()

    def test_3_create_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            rda_test = ResultDynamicAnalysis(0, "qc", 1, "Matrice circuito quantistico", 
                                           "Risultato analisi dinamica", 2)
            try:
                dao.create(rda_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.CREATE, ("qc", 1, "Matrice circuito quantistico", 
                                                                              "Risultato analisi dinamica", 2), 1)
                connection.close()

    """ Test read_by_id_result """

    def test_4_read_by_id_result_three_results(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [
                (2, "qc_1", 1, "Matrice qc_1", "Risultato analisi dinamica qc_1", 10),
                (4, "qc_2", 2, "Matrice qc_2", "Risultato analisi dinamica qc_2", 10),
                (6, "circuit", 3, "Matrice circuit", "Risultato analisi dinamica circuit", 10)
            ]
            oracle = [
                ResultDynamicAnalysis(2, "qc_1", 1, "Matrice qc_1", "Risultato analisi dinamica qc_1", 10),
                ResultDynamicAnalysis(4, "qc_2", 2, "Matrice qc_2", "Risultato analisi dinamica qc_2", 10),
                ResultDynamicAnalysis(6, "circuit", 3, "Matrice circuit", "Risultato analisi dinamica circuit", 10)
            ]
            result = dao.read_by_id_result(10)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID_RESULT, (10,))

    def test_5_read_by_id_result_not_results(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            oracle = []
            result = dao.read_by_id_result(10)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_ID_RESULT, (10,))

    def test_6_read_by_id_result_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_by_id_result(10)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_ID_RESULT, (10,))
                connection.close()











