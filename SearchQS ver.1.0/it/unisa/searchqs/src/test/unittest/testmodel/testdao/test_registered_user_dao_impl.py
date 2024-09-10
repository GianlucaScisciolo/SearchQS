import sys
sys.path.append("../../../../..")

import unittest
from unittest.mock import Mock, patch
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.registereduserdao.registered_user_dao_impl import RegisteredUserDAOImpl
from src.main.model.entity.registered_user import RegisteredUser

class TestRegisteredUserDAOImpl(unittest.TestCase):
    patch_execute_action = "src.main.model.dao.registereduserdao.registered_user_dao_impl.RegisteredUserDAOImpl.execute_action"
    patch_execute_select = "src.main.model.dao.registereduserdao.registered_user_dao_impl.RegisteredUserDAOImpl.execute_select"

    """ Test __init__ """

    def test_1_init(self):
        connection = MySQLConnection()
        connection.connection = Mock()
        connection.cursor = Mock()
        dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
        self.assertEqual(dao.connection, connection.connection)
        self.assertEqual(dao.cursor, connection.cursor)
        connection.close()

    """ Test create """

    def test_2_create_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
        
            ru_test = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                                     "Italia", "Italia", "Computer Science", "3334445556", "mr_PassWord_80", 
                                     "Salt Hex", 4)
            result = dao.create(ru_test)
            connection.close()

            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.CREATE, 
                                    ("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                                     "Italia", "Italia", "Computer Science", "3334445556", "mr_PassWord_80", 
                                     "Salt Hex", 4), 1)

    def test_3_create_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            ru_test = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                                     "Italia", "Italia", "Computer Science", "3334445556", "mr_PassWord_80", 
                                     "Salt Hex", 4)
            try:
                dao.create(ru_test)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.CREATE, 
                                    ("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                                     "Italia", "Italia", "Computer Science", "3334445556", "mr_PassWord_80", 
                                     "Salt Hex", 4), 1)
                connection.close()

    """ Test read_by_email """

    def test_4_read_by_email_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [
                ("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                 "Italia", "Italia", "Computer Science", "3334445556", "mr_PassWord_80", "Salt Hex", 4)
            ]
            oracle = RegisteredUser("mr_80@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                                    "Italia", "Italia", "Computer Science", "3334445556", "mr_PassWord_80", 
                                    "Salt Hex", 4)
            result = dao.read_by_email("mr_80@test.test")
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_EMAIL, ("mr_80@test.test",))

    def test_5_read_by_email_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [] 
            oracle = []
            result = dao.read_by_email("mr_80@test.test")
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_BY_EMAIL, ("mr_80@test.test",))

    def test_6_read_by_email_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_by_email("mr_80@test.test")
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_BY_EMAIL, ("mr_80@test.test",))
                connection.close()
        
    """ Test read_id_residential_address_by_email """

    def test_7_read_id_residential_address_by_email_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(4,)]
            oracle = 4
            result = dao.read_id_residential_address_by_email("mr_80@test.test")
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_RESIDENTIAL_ADDRESS_BY_EMAIL, 
                                                        ("mr_80@test.test",))

    def test_8_read_id_residential_address_by_email_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [] 
            oracle = []
            result = dao.read_id_residential_address_by_email("mr_80@test.test")
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(dao.READ_ID_RESIDENTIAL_ADDRESS_BY_EMAIL, 
                                                        ("mr_80@test.test",))

    def test_9_read_id_residential_address_by_email_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_id_residential_address_by_email("mr_80@test.test")
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(dao.READ_ID_RESIDENTIAL_ADDRESS_BY_EMAIL, 
                                                            ("mr_80@test.test",))
                connection.close()

    """ Test read_num_registered_user_by_id_residential_address """
    
    def test_10_read_num_registered_user_by_id_residential_address_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = [(10,)]
            oracle = 10
            result = dao.read_num_registered_user_by_id_residential_address(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(
                    dao.READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS, (4,))

    def test_11_read_num_registered_user_by_id_residential_address_not_result(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = []
            oracle = 0
            result = dao.read_num_registered_user_by_id_residential_address(4)
            connection.close()

            self.assertEqual(result, oracle)
            mock_execute_select.assert_called_once_with(
                    dao.READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS, (4,))

    def test_12_read_num_registered_user_by_id_residential_address_failure(self):
        with patch(self.patch_execute_select) as mock_execute_select:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_select.return_value = None
            try:
                dao.read_num_registered_user_by_id_residential_address(4)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_select.assert_called_once_with(
                    dao.READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS, (4,))
                connection.close()

    """ Test update_by_params_with_password """
    def test_13_update_by_params(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            ru_test = RegisteredUser("new_emali@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                                     "Italia", "Italia", "Computer Science", "3334445556", "test_password_80", 
                                     "Salt Hex", 4)
            current_email = "current_email@test.test"
            result = dao.update_by_params(ru_test, current_email)
            connection.close()
            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.UPDATE_BY_PARAMS, 
                                    ("Computer Science", "3334445556", "new_emali@test.test", 
                                      "test_password_80", "Salt Hex", 4, "current_email@test.test"), 1)
            
    def test_14_update_by_params(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            ru_test = RegisteredUser("new_emali@test.test", "Mario", "Rossi", 'M', "1980-10-05", "Torre del Greco", 
                                     "Italia", "Italia", "Computer Science", "3334445556", "test_password_80", 
                                     "Salt Hex", 4)
            current_email = "current_email@test.test"
            try:
                dao.update_by_params(ru_test, current_email)
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.UPDATE_BY_PARAMS, 
                                        ("Computer Science", "3334445556", "new_emali@test.test", 
                                          "test_password_80", "Salt Hex", 4, current_email), 1)
                connection.close()

    """ Test delete_by_email """

    def test_15_delete_by_email_success(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.return_value = True
            result = dao.delete_by_email("mr_80@test.test")
            connection.close()

            self.assertTrue(result)
            mock_execute_action.assert_called_once_with(dao.DELETE_BY_EMAIL, ("mr_80@test.test",), 1)
        
    def test_16_delete_by_email_failure(self):
        with patch(self.patch_execute_action) as mock_execute_action:
            connection = MySQLConnection()
            connection.connection = Mock()
            connection.cursor = Mock()
            dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            mock_execute_action.side_effect = Exception
            try:
                dao.delete_by_email("mr_80@test.test")
            except Exception as e:
                assert isinstance(e, Exception)
            finally:
                mock_execute_action.assert_called_once_with(dao.DELETE_BY_EMAIL, ("mr_80@test.test",), 1)
                connection.close()











