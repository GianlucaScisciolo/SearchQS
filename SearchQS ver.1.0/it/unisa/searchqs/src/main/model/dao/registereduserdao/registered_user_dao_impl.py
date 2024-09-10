from src.main.model.dao.dao.dao_impl import DAOImpl
from src.main.model.dao.registereduserdao.i_registered_user_dao import IRegisteredUserDAO
from src.main.model.entity.registered_user import RegisteredUser

class RegisteredUserDAOImpl(DAOImpl, IRegisteredUserDAO):
    def __init__(self, connection, cursor):
        super().__init__(connection, cursor)

    """ Queries """

    # Create
    
    CREATE = """
INSERT INTO registered_user (
    email, name, surname, gender, birthdate, city_birthplace, nation_birthplace, nationality, profession, 
    num_cellphone, password, salt_hex, id_residential_address
) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Read

    READ_BY_EMAIL = """
SELECT 
    email, name, surname, gender, birthdate, city_birthplace, nation_birthplace, nationality, profession, 
    num_cellphone, password, salt_hex, id_residential_address 
FROM 
    registered_user 
WHERE 
    email = %s;
    """

    READ_ID_RESIDENTIAL_ADDRESS_BY_EMAIL = """
SELECT 
    id_residential_address 
FROM 
    registered_user 
WHERE 
    email = %s;
    """

    READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS = """
SELECT 
    COUNT(*) AS num_registered_user 
FROM 
    registered_user 
WHERE 
    id_residential_address = %s;
    """

    """
        keys = ["profession_ru", "num_cellphone_ru", "email_ru", "password_ru", "confirm_password_ru", 
            "name_ra", "number_ra", "city_ra", "province_ra", "cap_ra"]
    """
    # Update
    UPDATE_BY_PARAMS = """
UPDATE registered_user 
SET profession = %s, num_cellphone = %s, email = %s, password = %s, salt_hex = %s, id_residential_address = %s 
WHERE email = %s;
    """

    # Delete

    DELETE_BY_EMAIL = """
DELETE FROM registered_user 
WHERE 
    email = %s;
    """

    """ Methods """

    # Create

    def create(self, ru):
        attributes = (ru.email, ru.name, ru.surname, ru.gender, ru.birthdate, ru.city_birthplace, 
                      ru.nation_birthplace, ru.nationality, ru.profession, ru.num_cellphone, ru.password, 
                      ru.salt_hex, ru.id_residential_address)
        create = self.execute_action(self.CREATE, attributes, 1)
        if create:
            return create
        raise Exception 

    # Read

    def read_by_email(self, email):
        registered_user = self.execute_select(self.READ_BY_EMAIL, (email,))
        if registered_user is None:
            raise Exception
        if registered_user != []:
            ru = RegisteredUser()
            (ru.email, ru.name, ru.surname, ru.gender, ru.birthdate, ru.city_birthplace, ru.nation_birthplace, 
                ru.nationality, ru.profession, ru.num_cellphone, ru.password, ru.salt_hex, 
                ru.id_residential_address) = registered_user[0]
            registered_user = ru
        return registered_user

    def read_id_residential_address_by_email(self, email):
        id_ra = self.execute_select(self.READ_ID_RESIDENTIAL_ADDRESS_BY_EMAIL, (email,))
        if id_ra is None:
            raise Exception
        if id_ra != []:
            id_ra = id_ra[0][0]
        return id_ra

    def read_num_registered_user_by_id_residential_address(self, id_ra):
        num_ru = self.execute_select(self.READ_NUM_REGISTERED_USER_BY_ID_RESIDENTIAL_ADDRESS, (id_ra,))
        if num_ru is None:
            raise Exception
        if num_ru == []:
            num_ru = 0
        else:
            num_ru = num_ru[0][0]
        return num_ru

    # Update
    def update_by_params(self, ru, current_email):
        update = self.execute_action(self.UPDATE_BY_PARAMS, 
                                     (ru.profession, ru.num_cellphone, ru.email, 
                                      ru.password, ru.salt_hex, ru.id_residential_address, current_email), 1)
        if update:
            return update
        raise Exception 
    
    # Delete

    def delete_by_email(self, email):
        delete = self.execute_action(self.DELETE_BY_EMAIL, (email,), 1)
        if delete:
            return delete
        raise Exception










