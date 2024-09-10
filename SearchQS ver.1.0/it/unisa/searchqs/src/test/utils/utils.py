import sys
sys.path.append("../../..")

from src.main.model.entity.registered_user import RegisteredUser

RU_TEST = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del greco", "Italia", 
                         "Italiana", "Computer Science", "3334445556", "f61891bd3df341843731e37a4f44feb93941838e31b07454a6c8a89de376cf8431636add1ae011d8b1f232ac294c58bf6f6dd0decac305ab14f7c0f5669969a7", 
                         "B330tClS7rNVZIUq", 10)

PATCH_CONNECTION_OPEN = "src.main.model.connection.mysql_connection.MySQLConnection.open"
PATCH_CONNECTION_CLOSE = "src.main.model.connection.mysql_connection.MySQLConnection.close"
PATCH_CONNECTION_START_TRANSACTION = "src.main.model.connection.mysql_connection.MySQLConnection.start_transaction"
PATCH_CONNECTION_COMMIT = "src.main.model.connection.mysql_connection.MySQLConnection.commit"
PATCH_CONNECTION_ROLLBACK = "src.main.model.connection.mysql_connection.MySQLConnection.rollback"

PATCH_CF_CHECK_LOGIN = "src.main.service.utils.check_form.check_login"
PATCH_CF_CHECK_LOGIN_AUTHENTICATION = "src.main.service.utils.check_form.check_login_authentication"
PATCH_CF_CHECK_REGISTRATION = "src.main.service.utils.check_form.check_registration"
PATCH_CF_CHECK_REGISTRATION_REGISTERED_USER_IS_PRESENT = "src.main.service.utils.check_form.check_registration_registered_user_is_present"
PATCH_CF_CHECK_MODIFICATION_PERSONAL_DATA = "src.main.service.utils.check_form.check_modification_personal_data"
PATCH_CF_CHECK_LOADING_Q_SYSTEM = "src.main.service.utils.check_form.check_loading_q_system"
PATCH_CF_CHECK_EXECUTION_ANALYSES = "src.main.service.utils.check_form.check_execution_analyses"

PATCH_RU_DAO_READ_BY_EMAIL = "src.main.model.dao.registereduserdao.registered_user_dao_impl.RegisteredUserDAOImpl.read_by_email"
PATCH_RU_DAO_CREATE = "src.main.model.dao.registereduserdao.registered_user_dao_impl.RegisteredUserDAOImpl.create"
PATCH_RU_DAO_UPDATE_BY_PARAMS = "src.main.model.dao.registereduserdao.registered_user_dao_impl.RegisteredUserDAOImpl.update_by_params"
PATCH_RU_DAO_READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS = "src.main.model.dao.registereduserdao.registered_user_dao_impl.RegisteredUserDAOImpl.read_num_registered_user_by_id_residential_address"

PATCH_RA_DAO_READ_ID_BY_PARAMS = "src.main.model.dao.residentialaddressdao.residential_address_dao_impl.ResidentialAddressDAOImpl.read_id_by_params"
PATCH_RA_DAO_CREATE = "src.main.model.dao.residentialaddressdao.residential_address_dao_impl.ResidentialAddressDAOImpl.create"
PATCH_RA_DAO_DELETE_BY_ID = "src.main.model.dao.residentialaddressdao.residential_address_dao_impl.ResidentialAddressDAOImpl.delete_by_id"

PATCH_SECURITY_GENERATION_RANDOM_STRING = "src.main.service.utils.security.generation_random_string"
PATCH_SECURITY_ENCRYPT_PASSWORD = "src.main.service.utils.security.encrypt_password"

PATCH_UA_SERVICE_DISPLAY_PERSONAL_DATA = "src.main.service.userareaservice.user_area_service_impl.UserAreaServiceImpl.display_personal_data"
PATCH_UA_SERVICE_MODIFICATION_PERSONAL_DATA = "src.main.service.userareaservice.user_area_service_impl.UserAreaServiceImpl.modification_personal_data"

PATCH_QS_DAO_READ_BY_NAME_AND_EMAIL_REGISTERED_USER = "src.main.model.dao.qsystemdao.q_system_dao_impl.QSystemDAOImpl.read_by_name_and_email_registered_user"
PATCH_QS_DAO_CREATE = "src.main.model.dao.qsystemdao.q_system_dao_impl.QSystemDAOImpl.create"
PATCH_QS_DAO_READ_ID_BY_ATTRIBUTES = "src.main.model.dao.qsystemdao.q_system_dao_impl.QSystemDAOImpl.read_id_by_attributes"
PATCH_QS_DAO_DELETE_BY_ID = "src.main.model.dao.qsystemdao.q_system_dao_impl.QSystemDAOImpl.delete_by_id"

PATCH_OS_MAKEDIRS = "os.makedirs"
PATCH_OS_PATH_JOIN = "os.path.join"

PATCH_ZIPFILE = "zipfile.ZipFile"
PATCH_ZIPFILE_EXTRACTALL = "zipfile.ZipFile.extractall"

PATCH_SUBPROCESS_RUN = "subprocess.run"

PATCH_GLOB = "glob.glob"

PATCH_JSON_DUMPS = "json.dumps"

PATCH_FILE_OPEN = "builtins.open"

PATCH_SF_DAO_READ_BY_PARAMS = "src.main.model.dao.sourcefiledao.source_file_dao_impl.SourceFileDAOImpl.read_by_params"
PATCH_SF_DAO_CREATE = "src.main.model.dao.sourcefiledao.source_file_dao_impl.SourceFileDAOImpl.create"
PATCH_SF_DAO_READ_BY_ID = "src.main.model.dao.sourcefiledao.source_file_dao_impl.SourceFileDAOImpl.read_by_id"
PATCH_SF_DAO_DELETE_BY_ID = "src.main.model.dao.sourcefiledao.source_file_dao_impl.SourceFileDAOImpl.delete_by_id"

PATCH_A_OP_GET_NAMES_Q_CIRCUITS_FROM_FILE = "src.main.service.analysisservice.analysis_operation.get_names_q_circuits_from_file"
PATCH_A_OP_GET_RESULT_STATIC_ANALYSIS = "src.main.service.analysisservice.analysis_operation.get_result_static_analysis"
PATCH_A_OP_GET_RESULTS_DYNAMIC_ANALYSIS = "src.main.service.analysisservice.analysis_operation.get_results_dynamic_analysis"

PATCH_A_DAO_CREATE = "src.main.model.dao.analysisdao.analysis_dao_impl.AnalysisDAOImpl.create"
PATCH_A_DAO_READ_ID_BY_PARAMS_WITH_NAME_TRANSPILATION_NONE = "src.main.model.dao.analysisdao.analysis_dao_impl.AnalysisDAOImpl.read_id_by_params_with_name_transpilation_none"
PATCH_A_DAO_READ_ID_BY_PARAMS = "src.main.model.dao.analysisdao.analysis_dao_impl.AnalysisDAOImpl.read_id_by_params"
PATCH_A_DAO_DELETE_BY_ID = "src.main.model.dao.analysisdao.analysis_dao_impl.AnalysisDAOImpl.delete_by_id"
PATCH_A_DAO_READ_NUM_ANALYSES_BY_ID_Q_SYSTEM = "src.main.model.dao.analysisdao.analysis_dao_impl.AnalysisDAOImpl.read_num_analyses_by_id_q_system"


PATCH_R_DAO_CREATE = "src.main.model.dao.resultdao.result_dao_impl.ResultDAOImpl.create"
PATCH_R_DAO_READ_ID_BY_PARAMS = "src.main.model.dao.resultdao.result_dao_impl.ResultDAOImpl.read_id_by_params"
PATCH_R_DAO_READ_BY_ID_ANALYSIS = "src.main.model.dao.resultdao.result_dao_impl.ResultDAOImpl.read_by_id_analysis"
PATCH_R_DAO_READ_ID_SOURCE_FILES_BY_ID_ANALYSIS = "src.main.model.dao.resultdao.result_dao_impl.ResultDAOImpl.read_id_source_files_by_id_analysis"
PATCH_R_DAO_READ_NUM_RESULTS_BY_ID_SOURCE_FILE = "src.main.model.dao.resultdao.result_dao_impl.ResultDAOImpl.read_num_results_by_id_source_file"

PATCH_RDA_DAO_CREATE = "src.main.model.dao.resultdynamicanalysisdao.result_dynamic_analysis_dao_impl.ResultDynamicAnalysisDAOImpl.create"
PATCH_RDA_DAO_READ_BY_ID_RESULT = "src.main.model.dao.resultdynamicanalysisdao.result_dynamic_analysis_dao_impl.ResultDynamicAnalysisDAOImpl.read_by_id_result"

PATCH_A_SERVICE_LOGIN = "src.main.service.authenticationservice.authentication_service_impl.AuthenticationServiceImpl.login"
PATCH_A_SERVICE_REGISTRATION = "src.main.service.authenticationservice.authentication_service_impl.AuthenticationServiceImpl.registration"

PATCH_ANALYSIS_SERVICE_DELETION_ANALYSIS = "src.main.service.analysisservice.analysis_service_impl.AnalysisServiceImpl.deletion_analysis"
PATCH_ANALYSIS_SERVICE_DISPLAY_ANALYSIS = "src.main.service.analysisservice.analysis_service_impl.AnalysisServiceImpl.display_analysis"
PATCH_ANALYSIS_SERVICE_LOADING_Q_SYSTEM = "src.main.service.analysisservice.analysis_service_impl.AnalysisServiceImpl.loading_q_system"
PATCH_ANALYSIS_SERVICE_DISPLAY_NAMES_TRANSPILATION = "src.main.service.analysisservice.analysis_service_impl.AnalysisServiceImpl.display_names_transpilation"
PATCH_ANALYSIS_SERVICE_EXECUTION_ANALYSES = "src.main.service.analysisservice.analysis_service_impl.AnalysisServiceImpl.execution_analyses"

PATCH_UTILS_GET_ATTRIBUTES_FROM_LIST_OF_REQUEST = "src.main.view.utils.utils.get_attributes_from_list_of_request"
PATCH_UTILS_GET_ATTRIBUTE_REQUEST_FILE = "src.main.view.utils.utils.get_attribute_request_file"

code = """
from IPython.display import IFrame
s = '110101'
from qiskit import *

n = len(s)
circuit = QuantumCircuit(n+1,n)
# Step 0
circuit.x(n) # the n+1 qubits are indexed 0...n, so the last qubit is index    <--
circuit.barrier() # just a visual aid for now
# Step 1
circuit.h(range(n+1)) # range(n+1) returns [0,1,2,...,n] in Python. This covers all the qubits    <--
circuit.barrier() # just a visual aid for now
# Step 2
for ii, yesno in enumerate(reversed(s)):
    if yesno == '1': 
        circuit.cx(ii, n)
circuit.barrier() # just a visual aid for now
# Step 3
circuit.h(range(n+1)) # range(n+1) returns [0,1,2,...,n] in Python. This covers all the qubits
circuit.barrier() # just a visual aid for now
circuit.measure(range(n), range(n)) # measure the qubits indexed from 0 to n-1 and store them into the classical bits indexed 0 to n-1
qc = QuantumCircuit(2)
# Applica una porta Hadamard al primo qubit
qc.h(0)
# Applica una porta CNOT tra il primo e il secondo qubit
qc.cx(0, 1)
        """





