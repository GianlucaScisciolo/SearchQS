from src.main.service.userareaservice.i_user_area_service import IUserAreaService
from flask import session
import traceback
from src.main.model.dao.registereduserdao.registered_user_dao_impl import RegisteredUserDAOImpl
from src.main.model.dao.residentialaddressdao.residential_address_dao_impl import ResidentialAddressDAOImpl
from src.main.model.dao.qsystemdao.q_system_dao_impl import QSystemDAOImpl
from src.main.model.dao.analysisdao.analysis_dao_impl import AnalysisDAOImpl
from src.main.model.dao.resultdao.result_dao_impl import ResultDAOImpl
from src.main.model.dao.sourcefiledao.source_file_dao_impl import SourceFileDAOImpl
from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress
import mysql.connector
from src.main.model.connection.mysql_connection import MySQLConnection
import src.main.service.utils.check_form as check_form
import src.main.service.utils.security as security

class UserAreaServiceImpl(IUserAreaService):

    def display_user_area(self):
        if session == {} or session['actor'] != "registered user":
            return {'success': None, 'error': 'Errore durante la visualizzazione della propria area utente.'}
        return {'success': True, 'errors': {}}

    def display_form_deletion_account(self):
        if session == {} or session['actor'] != "registered user":
            return {'success': None, 'error': 'Errore durante la visualizzazione del form per eliminare l\'account.'}
        return {'success': True, 'errors': {}}
    
    def deletion_account(self):
        connection = None
        qs_dao = None
        a_dao = None
        r_dao = None
        sf_dao = None
        ru_dao = None
        ra_dao = None
        try:
            connection = MySQLConnection()
            connection.open()
            qs_dao = QSystemDAOImpl(connection.connection, connection.cursor)
            a_dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            r_dao = ResultDAOImpl(connection.connection, connection.cursor)
            sf_dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            ru_dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            ra_dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            connection.start_transaction()

            id_q_systems = []
            id_analyses = []
            id_source_files_results = set()
            id_q_systems = qs_dao.read_id_by_email_registered_user(session['email'])
            for id_qs in id_q_systems:
                id_analyses_qs = a_dao.read_id_by_id_q_system(id_qs)
                id_analyses.extend(id_analyses_qs)
            for id_a in id_analyses:
                id_source_files_results_analysis = r_dao.read_id_source_files_by_id_analysis(id_a)
                id_source_files_results = id_source_files_results.union(id_source_files_results_analysis)
            id_ra = ru_dao.read_id_residential_address_by_email(session['email'])
            ru_dao.delete_by_email(session['email'])
            for id_sf_r in id_source_files_results:
                num_linked_results = r_dao.read_num_results_by_id_source_file(id_sf_r)
                if num_linked_results == 0 or num_linked_results == []:
                    sf_dao.delete_by_id(id_sf_r)
            num_linked_ru = ru_dao.read_num_registered_user_by_id_residential_address(id_ra)
            if num_linked_ru == 0:
                ra_dao.delete_by_id(id_ra)

            connection.commit()
            session.clear()
            return {'success': True}
        except Exception as e:
            print(f"Errore durante l\'eliminazione dell\'account: {e.args}")
            traceback.print_exc()
            connection.rollback()
            return {'success': None}
        finally:
            connection.close()

    def display_personal_data(self):
        connection = None
        ru_dao = None
        ra_dao = None
        try:
            connection = MySQLConnection()
            connection.open()
            ru_dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            ra_dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            
            ru_db = ru_dao.read_by_email(session["email"])
            if ru_db == []:
                return {'success': True, "registered_user": []}
            ra_db = ra_dao.read_by_id(ru_db.id_residential_address)
            return {'success': True, "registered_user": ru_db, "residential_address": ra_db, 'id_ra': ra_db.id, "errors": {}}
        except Exception as e:
            print(f"Errore durante la visualizzazione dei dati personali: {e.args}")
            traceback.print_exc()
            connection.rollback()
            return {'success': None, 'error': "Errore durante la visualizzazione dei dati personali."}
        finally:
            connection.close()

    def modification_personal_data(self, attributes):
        new_ru = RegisteredUser()
        new_ra = ResidentialAddress()
        connection = None
        ru_dao = None
        ra_dao = None
        errors = {}
        num_errors = 0
        id_ra_db = 0
        try:
            connection = MySQLConnection()
            connection.open()
            ru_dao = RegisteredUserDAOImpl(connection.connection, connection.cursor)
            ra_dao = ResidentialAddressDAOImpl(connection.connection, connection.cursor)
            connection.start_transaction()

            personal_data = self.display_personal_data()
            personal_data['registered_user'].profession = attributes['profession_ru']
            personal_data['registered_user'].num_cellphone = attributes['num_cellphone_ru']
            personal_data['registered_user'].email = attributes['email_ru']
            personal_data['residential_address'].name = attributes['name_ra']
            personal_data['residential_address'].number = attributes['number_ra']
            personal_data['residential_address'].city = attributes['city_ra']
            personal_data['residential_address'].province = attributes['province_ra']
            personal_data['residential_address'].cap = attributes['cap_ra']
            ru_db = ru_dao.read_by_email(attributes['email_ru'])
            [errors, num_errors] = check_form.check_modification_personal_data(attributes, session['email'], ru_db)
            if num_errors > 0:
                raise Exception("errore durante la modifica dei dati personali.")
            id_ra_db = ra_dao.read_id_by_params(personal_data['residential_address'])
            if id_ra_db == []:
                ra_dao.create(personal_data['residential_address'])
                id_ra_db = ra_dao.read_id_by_params(personal_data['residential_address'])
            personal_data['registered_user'].id_residential_address = id_ra_db
            if personal_data['registered_user'].profession == "":
                personal_data['registered_user'].profession = None
            if personal_data['registered_user'].num_cellphone == "":
                personal_data['registered_user'].num_cellphone = None
            personal_data['registered_user'].salt_hex = security.generation_random_string(16)
            personal_data['registered_user'].password = security.encrypt_password(
                    attributes['password_ru'], personal_data['registered_user'].salt_hex, security.PEPPER_HEX)
            personal_data['residential_address'].id = id_ra_db
            ru_dao.update_by_params(personal_data['registered_user'], session['email'])
            num_ru = ru_dao.read_num_registered_user_by_id_residential_address(attributes['id_ra'])
            if num_ru < 1:
                ra_dao.delete_by_id(attributes['id_ra'])
            connection.commit()
            return {'success': True, 'errors': {}, 'registered_user': personal_data['registered_user'], 
                    'residential_address': personal_data['residential_address'], 'id_ra': id_ra_db}
        except Exception as e:
            print(f"Errore durante la modifica dei dati personali: {e.args}")
            traceback.print_exc()
            connection.rollback()
            if num_errors > 0:
                return {'success': False, 'errors': errors, 'registered_user': personal_data['registered_user'], 
                        'residential_address': personal_data['residential_address'], 
                        'password': attributes['password_ru'], 'confirm_password': attributes["confirm_password_ru"], 
                        'id_ra': attributes['id_ra']}
            return {'success': None, 'error': "Errore durante la modifica dei dati personali. Riprova."}
        finally:
            connection.close()
        
            










