from src.main.service.authenticationservice.i_authentication_service import IAuthenticationService
from flask import session
import traceback
from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.registereduserdao.registered_user_dao_impl import RegisteredUserDAOImpl
from src.main.model.dao.residentialaddressdao.residential_address_dao_impl import ResidentialAddressDAOImpl
import mysql.connector
import src.main.service.utils.check_form as check_form
import src.main.service.utils.security as security

class AuthenticationServiceImpl(IAuthenticationService):
    
    def display_form_registration(self):
        if session == {}:
            return {'success': True, 'errors': {}}
        return {'success': None, 'error': 'Utente gia\' loggato.'}
    
    def registration(self, attributes):
        ru = RegisteredUser()
        ra = ResidentialAddress()
        connection = None
        ru_dao = None
        ra_dao = None
        errors = {}
        num_errors = 0
        try:
            connection = MySQLConnection()
            connection.open()
            ru_dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            ra_dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            connection.start_transaction()
            attributes['email_ru'] = attributes['email_ru'].lower()
            [errors, num_errors] = check_form.check_registration(attributes)       
            if num_errors > 0:
                raise Exception("i dati forniti nel form non sono corretti.")
            ru.set_by_attributes(attributes)
            ra.set_by_attributes(attributes)
            ru_db = ru_dao.read_by_email(ru.email)
            [errors, num_errors] = check_form.check_registration_registered_user_is_present(ru_db)
            if num_errors > 0:
                raise Exception("utente gia\' presente.")
            id_ra_db = ra_dao.read_id_by_params(ra)
            if id_ra_db == []:
                ra_dao.create(ra)
                id_ra_db = ra_dao.read_id_by_params(ra)
            ru.id_residential_address = id_ra_db
            ru.salt_hex = security.generation_random_string(16)
            ru.password = security.encrypt_password(ru.password, ru.salt_hex, security.PEPPER_HEX)
            if ru.profession == "":
                ru.profession = None
            if ru.num_cellphone == "":
                ru.num_cellphone = None
            ru_dao.create(ru)
            connection.commit()
            return {'success': True, 'errors': {}}
        except Exception as e:
            print(f"Errore durante la registrazione: {e.args}")
            traceback.print_exc()
            connection.rollback()
            if num_errors > 0:
                return {
                    'success': False, 
                    "errors": errors, 
                    'name_ru': attributes['name_ru'],
                    'surname_ru': attributes['surname_ru'],
                    'gender_ru': attributes['gender_ru'],
                    'birthdate_ru': attributes['birthdate_ru'],
                    'city_birthplace_ru': attributes['city_birthplace_ru'],
                    'nation_birthplace_ru': attributes['nation_birthplace_ru'], 
                    'nationality_ru': attributes['nationality_ru'],
                    'profession_ru': attributes['profession_ru'],
                    'num_cellphone_ru': attributes['num_cellphone_ru'],
                    'email_ru': attributes['email_ru'],
                    'password_ru': attributes['password_ru'], 
                    'confirm_password_ru': attributes['confirm_password_ru'],
                    'name_ra': attributes['name_ra'],
                    'number_ra': attributes['number_ra'], 
                    'city_ra': attributes['city_ra'],
                    'province_ra': attributes['province_ra'],
                    'cap_ra': attributes['cap_ra']
                }
            return {
                'success': None, 
                'error': 'La registrazione e\' fallita. Riprova.', 
            }
        finally:
            connection.close()
                        
    def display_form_login(self):
        if session == {}:
            return {'success': True, 'errors': {}}
        return {'success': None, 'error': "Utente gia\' loggato."}
                       
    def login(self, attributes):
        connection = None
        ru_dao = None
        errors = {}
        num_errors = 0
        try:
            connection = MySQLConnection()
            connection.open()
            ru_dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            attributes['email_ru'] = attributes['email_ru'].lower()
            [errors, num_errors] = check_form.check_login(attributes)
            if num_errors > 0:
                raise Exception("i dati forniti nel form del login non sono corretti.")
            ru_db = ru_dao.read_by_email(attributes['email_ru'])
            [errors, num_errors] = check_form.check_login_authentication(ru_db, attributes['password_ru'])
            if num_errors > 0:
                raise Exception("utente non trovato nel database.")
            session['is_logged'] = True
            session['email'] = attributes['email_ru']
            session['actor'] = "registered user"
            return {'success': True, "errors": {}}
        except Exception as e:
            print(f"Errore durante il login: {e.args}")
            traceback.print_exc()
            if num_errors > 0:
                return {'success': False, 
                        'errors': errors,
                        'email_ru': attributes['email_ru'], 
                        'password_ru': attributes['password_ru']}
            return {'success': None, 'error': "Il login e\' fallito. Riprova."}
        finally:
            connection.close()
    
    def logout(self):
        session.clear()
            
            

    
            
        








