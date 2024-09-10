import sys
sys.path.append("../..")

""" unit test"""

# Test model.connection
from src.test.unittest.testmodel.testconnection.test_mysql_connection import TestMySQLConnection

# Test model.dao

from src.test.unittest.testmodel.testdao.test_dao_impl import TestDAOImpl
from src.test.unittest.testmodel.testdao.test_analysis_dao_impl import TestAnalysisDAOImpl
from src.test.unittest.testmodel.testdao.test_q_system_dao_impl import TestQSystemDAOImpl
from src.test.unittest.testmodel.testdao.test_registered_user_dao_impl import TestRegisteredUserDAOImpl
from src.test.unittest.testmodel.testdao.test_residential_address_dao_impl import TestResidentialAddressDAOImpl
from src.test.unittest.testmodel.testdao.test_result_dao_impl import TestResultDAOImpl
from src.test.unittest.testmodel.testdao.test_result_dynamic_analysis_dao_impl import TestResultDynamicAnalysisDAOImpl
from src.test.unittest.testmodel.testdao.test_source_file_dao_impl import TestSourceFileDAOImpl

# Test service.authentication_service

from src.test.unittest.testservice.testauthenticationservice.test_authentication_service_impl import TestAuthenticationServiceImpl

# Test service.user_area_service

from src.test.unittest.testservice.testuserareaservice.test_user_area_service_impl import TestUserAreaServiceImpl

# Test service.analysis_service.q_smell

from src.test.unittest.testservice.testanalysisservice.testqcsmell.test_cg import TestCG
from src.test.unittest.testservice.testanalysisservice.testqcsmell.test_idq import TestIdQ
from src.test.unittest.testservice.testanalysisservice.testqcsmell.test_im import TestIM
from src.test.unittest.testservice.testanalysisservice.testqcsmell.test_iq import TestIQ
from src.test.unittest.testservice.testanalysisservice.testqcsmell.test_lc import TestLC
from src.test.unittest.testservice.testanalysisservice.testqcsmell.test_lpq import TestLPQ
from src.test.unittest.testservice.testanalysisservice.testqcsmell.test_roc import TestROC

# Test service.analysis_service

from src.test.unittest.testservice.testanalysisservice.test_analysis_operation import TestAnalysisOperation
from src.test.unittest.testservice.testanalysisservice.test_transpilation import TestTranspilation
from src.test.unittest.testservice.testanalysisservice.test_analysis_service_impl import TestAnalysisServiceImpl

""" integration test """

# Test service

from src.test.integrationtest.testservice.test_authentication_service_impl import TestITAuthenticationServiceImpl
from src.test.integrationtest.testservice.test_user_area_service_impl import TestITUserAreaServiceImpl
from src.test.integrationtest.testservice.test_analysis_service_impl import TestITAnalysisServiceImpl


# Test view

from src.test.integrationtest.testview.test_authentication_view import TestITAuthenticationView
from src.test.integrationtest.testview.test_user_area_view import TestITUserAreaView
from src.test.integrationtest.testview.test_analysis_view import TestITAnalysisView










