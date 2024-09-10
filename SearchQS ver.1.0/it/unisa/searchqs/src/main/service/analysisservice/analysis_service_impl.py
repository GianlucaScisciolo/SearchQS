from src.main.service.analysisservice.i_analysis_service import IAnalysisService
from flask import session
from src.main.service.analysisservice.transpilation import Transpilation
from src.main.model.connection.mysql_connection import MySQLConnection
from src.main.model.dao.analysisdao.analysis_dao_impl import AnalysisDAOImpl
from src.main.model.dao.qsystemdao.q_system_dao_impl import QSystemDAOImpl
from src.main.model.dao.resultdao.result_dao_impl import ResultDAOImpl
from src.main.model.dao.sourcefiledao.source_file_dao_impl import SourceFileDAOImpl
from src.main.model.dao.resultdynamicanalysisdao.result_dynamic_analysis_dao_impl import ResultDynamicAnalysisDAOImpl
import traceback
from src.main.model.entity.q_system import QSystem
from datetime import datetime, timezone, timedelta
import zipfile
import subprocess
import sys
import os
import glob
from src.main.model.entity.analysis import Analysis
from src.main.model.entity.source_file import SourceFile
from src.main.model.entity.result import Result
import src.main.service.analysisservice.analysis_operation as a_op
import src.main.service.utils.check_form as check_form
import json

class AnalysisServiceImpl(IAnalysisService):
    def display_analysis_area(self):
        if session == {} or session['actor'] != "registered user":
            return {'success': None, 'error': 'Errore durante la visualizzazione dell\'area analisi.'}
        return {'success': True, 'errors': {}}
    
    def display_names_transpilation(self):
        t = Transpilation
        return {'success': True, 'transpilations': t.LIST_NAMES_TRANSPILATION}
    
    def display_analyses_transpilation_selected(self, attributes):
        connection = None
        a_dao = None
        qs_dao = None
        try:
            connection = MySQLConnection()
            connection.open()
            a_dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            qs_dao = QSystemDAOImpl(connection.connection, connection.cursor)
            q_systems = qs_dao.read_by_email_registered_user(session['email'])
            if q_systems == []:
                return {'success': True, 'analyses': []}
            analyses = []
            for qs in q_systems:
                analyses_qs = []
                if attributes["name_transpilation"] != "None":
                    analyses_qs = a_dao.read_by_name_transpilation_and_id_q_system(attributes['name_transpilation'], qs.id)
                else:
                    analyses_qs = a_dao.read_by_id_q_system_without_transpilation(qs.id)
                for a_qs in analyses_qs:
                    if analyses_qs != []:
                        analyses.append({'q_system': qs, 'analysis': a_qs})
            return {'success': True, 'analyses': analyses}
        except Exception as e:
            print(f"Errore durante la visualizzazione delle analisi: {e.args}")
            traceback.print_exc()
            return {'success': None}
        finally:
            connection.close()

    def display_form_loading_q_system(self, attributes):
        if session == {} or session['actor'] != "registered user":
            return {'success': None, 'error': 'Utente gia\' loggato.'}
        return {'success': True, 'errors': {}, 'name_transpilation': attributes['name_transpilation']}
        
    def loading_q_system(self, attributes): 
        filename = attributes['filename']
        qs_dao = None
        errors = {}
        num_errors = 0
        try:
            connection = MySQLConnection()
            connection.open()
            qs_dao = QSystemDAOImpl(connection.connection, connection.cursor)
            connection.start_transaction()
            [errors, num_errors] = check_form.check_loading_q_system(attributes)
            if num_errors > 0:
                raise Exception("I dati inseriti nel form loading_q_system non sono validi.")
            qs = QSystem()
            (qs.name, qs.email_registered_user) = (
                filename, session['email']
            )
            id_qs = 0
            qs_db = qs_dao.read_by_name_and_email_registered_user(qs.name, session['email'])
            if qs_db == []:
                qs_dao.create(qs)
                id_qs = qs_dao.read_id_by_attributes(qs)
                if id_qs == []:
                    raise Exception("id sistema quantistico non trovato.")
            else:
                id_qs = qs_db.id
            os.makedirs(f'app_{id_qs}', exist_ok=True)
            path_zip = os.path.join(f'app_{id_qs}/', filename)
            attributes['file'].save(path_zip)
            with zipfile.ZipFile(path_zip, 'r') as zip_ref:
                zip_ref.extractall(f'app_{id_qs}')
            subprocess.run(['pipreqs', f'app_{id_qs}'])
            subprocess.run([sys.executable, '-m', 'venv', f'app_{id_qs}\\\\venv'])
            subprocess.run([os.path.join(f'app_{id_qs}', 'venv', 'Scripts', 'pip'), 'install', '-r', os.path.join(f'app_{id_qs}', 'requirements.txt')])
            python_files = glob.glob(os.path.join(f"app_{id_qs}", qs.name[0:(len(qs.name)-4)], "**/*.py"), recursive=True)
            python_files = [file.replace(f'app_{id_qs}\\\\', '') for file in python_files]
            python_files = [file.replace(f'app_{id_qs}/', '') for file in python_files]
            files_json = json.dumps(python_files)
            connection.commit()
            return {'success': True, 'python_files': python_files, 'files_json': files_json, 'id_qs': id_qs, 'name_qs': qs.name, 'num_errors': num_errors}
        except Exception as e:
            print(f"Errore durante il caricamento del sistema quantistico; {e.args}")
            traceback.print_exc()
            connection.rollback()
            if num_errors > 0:
                return {'success': False, 'errors': errors, 'num_errors': num_errors}
            return {'success': None, 
                    'error': "Errore durante il caricamento del sistema quantistico. Riprova."}
        finally:
            connection.close()

    def execution_analyses(self, attributes):
        connection = None
        sf_dao = None
        a_dao = None
        r_dao = None
        rda_dao = None
        errors = {}
        num_errors = 0
        try:
            connection = MySQLConnection()
            connection.open()
            sf_dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            a_dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            r_dao = ResultDAOImpl(connection.connection, connection.cursor)
            rda_dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
            connection.start_transaction()
        
            [errors, num_errors] = check_form.check_execution_analyses(attributes)
            if num_errors > 0:
                raise Exception("dati del form per l\'esecuzione delle analisi non validi.")
            file_contents = {}
            for file in attributes['files_selected']:
                with open(f"{file}", 'r') as f:
                    file_contents[file] = f.read()
            source_files_and_names_qc = []
            for file, content in file_contents.items():
                sf = SourceFile()
                sf.path = file
                sf.set_file_from_code(content)
                sf_db = sf_dao.read_by_params(sf)
                if sf_db == []:
                    sf_dao.create(sf)
                    sf_db = sf_dao.read_by_params(sf)
                sf.id = sf_db.id
                names_qc = a_op.get_names_q_circuits_from_file(sf.path)
                source_files_and_names_qc.append((sf, names_qc))
            current_datetime = datetime.now(tz=timezone.utc)
            current_datetime_ita = current_datetime.astimezone(timezone(timedelta(hours=2)))
            current_datetime_ita = current_datetime_ita.strftime('%Y-%m-%d %H:%M:%S')
            for t in attributes['transpilations_selected']:
                if t == "None":
                    t = None
                a = Analysis()
                (a.id, a.name_transpilation, a.optimization, a.save_date, a.id_q_system) = (
                    0, t, attributes['optimization'], current_datetime_ita, attributes['id_qs']
                )

                is_created = a_dao.create(a)
                if t is None:
                    a.id = a_dao.read_id_by_params_with_name_transpilation_none(a)
                else:
                    a.id = a_dao.read_id_by_params(a)
                for sf_and_nqc in source_files_and_names_qc:
                    rsa = a_op.get_result_static_analysis(
                            sf_and_nqc[0].path, sf_and_nqc[0].get_code_from_file(), sf_and_nqc[1], a.name_transpilation, 
                            a.optimization)
                    r = Result()
                    (r.id, r.result_static_analysis, r.id_analysis, r.id_source_file) = (0, rsa, a.id, sf_and_nqc[0].id)
                    r_dao.create(r)
                    r.id = r_dao.read_id_by_params(r)
                    results_da = a_op.get_results_dynamic_analysis(
                            sf_and_nqc[0].path, sf_and_nqc[0].get_code_from_file(), sf_and_nqc[1], a.name_transpilation, 
                            a.optimization, r.id)
                    for rda in results_da:
                        rda_dao.create(rda)
            connection.commit()
            t = Transpilation()
            return {
                'success': True, 
                'transpilations': t.LIST_NAMES_TRANSPILATION
            }
        except Exception as e:
            print(f"Errore durante l\'esecuzione dell\'analisi; {e.args}")
            traceback.print_exc()
            connection.rollback()
            if num_errors > 0:
                return {
                    'success': False,
                    'id_qs': attributes['id_qs'],
                    'name_qs': attributes['name_qs'],
                    'errors': errors, 
                    'num_errors': num_errors, 
                    'files_json': attributes['files_json'],
                    'transpilations_json': attributes['transpilations_json'],
                    'python_files': json.loads(attributes['files_json']),
                    'transpilations': json.loads(attributes['transpilations_json'])
                }
            return {'success': None, 'error': "Errore durante l\'esecuzone delle analisi. Riprova."}
        finally:
            connection.close()
    
    def display_analysis(self, attributes):
        connection = None
        r_dao = None
        sf_dao = None
        rda_dao = None
        try:
            connection = MySQLConnection()
            connection.open()
            r_dao = ResultDAOImpl(connection.connection, connection.cursor)
            sf_dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            rda_dao = ResultDynamicAnalysisDAOImpl(connection.connection, connection.cursor)
            response = {}
            qs = QSystem()
            qs.id = attributes['id_qs']
            qs.name = attributes['name_qs']
            qs.email_registered_user = session['email']
            response['q_system'] = qs
            a = Analysis()
            a.id = attributes['id_analysis']
            a.name_transpilation = attributes['name_transpilation']
            a.optimization = attributes['optimization']
            a.save_date = attributes['save_date']
            a.id_q_system = qs.id
            response['analysis'] = a
            results_output = []
            results = r_dao.read_by_id_analysis(a.id)
            if results == []:
                response['success'] = True
                response['results'] = results
                return response
            for index in range(0, len(results)):
                t = Transpilation()
                id_sf: int = results[index].id_source_file
                sf: SourceFile = sf_dao.read_by_id(id_sf)
                rsa = results[index].result_static_analysis
                results_da = rda_dao.read_by_id_result(results[index].id)
                if results_da != [] and a.name_transpilation != 'None':
                    code_sf = sf.get_code_from_file()
                    code_sf = (f"""
from qiskit import transpile\n{code_sf}
                    """)
                    for rda in results_da:
                        code_sf += f"""
{rda.name_q_circuit} = transpile({rda.name_q_circuit}, basis_gates={t.LIST_GATES[a.name_transpilation]}, optimization_level={a.optimization})
                        """
                    sf.set_file_from_code(code_sf)
                results_output.append({'source_file': sf, 'result_static_analysis': rsa, 'results_dynamic_analysis': results_da})
            response['results'] = results_output
            response['success'] = True
            return response
        except Exception as e:
            print(f"Errore durante la visualizzazione del sistema quantistico; {e.args}")
            traceback.print_exc()
            return {'success': None, 'error': "Errore durante la visualizzazione dell\'analisi. Riprova."}
        finally:
            connection.close()

    def display_form_deletion_analysis(self, attributes):
        if session == {} or session['actor'] != "registered user":
            return {'success': None, 'error': 'Utente gia\' loggato.'}
        return {
            'success': True, 
            'error': "Errore durante la visualizzazione del form per l\'eliminazione dell\'analisi. Riprova.",
            'id_analysis': attributes['id_analysis'], 
            'id_qs': attributes['id_qs'], 
            'name_transpilation': attributes['name_transpilation'], 
            'route': attributes['route'], 
            'save_date_qs': attributes['save_date_qs'], 
            'name_qs': attributes['name_qs']
        }

    def deletion_analysis(self, attributes):
        connection = None
        r_dao = None
        sf_dao = None
        a_dao = None
        qs_dao = None
        try:
            connection = MySQLConnection()
            connection.open()
            r_dao = ResultDAOImpl(connection.connection, connection.cursor)
            sf_dao = SourceFileDAOImpl(connection.connection, connection.cursor)
            a_dao = AnalysisDAOImpl(connection.connection, connection.cursor)
            qs_dao = QSystemDAOImpl(connection.connection, connection.cursor)
            connection.start_transaction()

            id_source_files_results = r_dao.read_id_source_files_by_id_analysis(attributes['id_analysis'])                
            a_dao.delete_by_id(attributes['id_analysis'])
            for id_sf_r in id_source_files_results:
                num_linked_results = r_dao.read_num_results_by_id_source_file(id_sf_r)
                if num_linked_results == 0:
                    sf_dao.delete_by_id(id_sf_r)
            num_analyses_qs = a_dao.read_num_analyses_by_id_q_system(attributes['id_qs'])
            if num_analyses_qs == 0:
                qs_dao.delete_by_id(attributes['id_qs'])
            
            connection.commit()
            return {'success': True}
        except Exception as e:
            print(f"Errore durante l\'eliminazione dell\'analisi: {e.args}")
            traceback.print_exc()
            connection.rollback()
            return {'success': None, 'error': "Errore durante l'eliminazione dell'analisi selezionata. Riprova."}
        finally:
            connection.close()












