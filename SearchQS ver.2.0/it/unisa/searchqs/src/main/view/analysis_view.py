from flask import Blueprint, render_template, request, session, redirect, url_for
from src.main.service.analysisservice.analysis_service_impl import AnalysisServiceImpl
import src.main.view.utils.utils as utils
from werkzeug.utils import secure_filename
import json

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/display_analysis_area', methods=['GET', 'POST'])
def display_analysis_area():
    service = AnalysisServiceImpl()
    response = service.display_analysis_area()
    if response['success']:
        page_html = "analysistemplate/analysis_area.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)

@analysis_bp.route('/display_names_transpilations', methods=['GET', 'POST'])
def display_names_transpilations():
    service = AnalysisServiceImpl()
    response = service.display_names_transpilation()
    page_html = "analysistemplate/names_transpilation.html"
    return render_template(page_html, params=response)

@analysis_bp.route('/display_analyses_transpilation_selected', methods=['GET', 'POST'])
def display_analyses_transpilation_selected():
    service = AnalysisServiceImpl()
    keys = ["name_transpilation"]
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.display_analyses_transpilation_selected(attributes)
    if response['success']:
        page_html = "analysistemplate/analyses_transpilation_selected.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """

@analysis_bp.route('/display_form_loading_q_system', methods=['GET', 'POST'])
def display_form_loading_q_system():
    service = AnalysisServiceImpl()
    keys = ["name_transpilation"]
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.display_form_loading_q_system(attributes)
    if response['success']:
        page_html = "analysistemplate/loading_q_system.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """

@analysis_bp.route('/loading_q_system', methods=['GET', 'POST'])
def loading_q_system():
    service = AnalysisServiceImpl()
    file = utils.get_attribute_request_file(request, 'file')
    filename = secure_filename(file.filename)
    attributes = {'filename': filename, 'file': file}
    response = service.loading_q_system(attributes)
    if response['success']:
        transpilations = service.display_names_transpilation()['transpilations']
        transpilations_json = json.dumps(transpilations)
        response['transpilations'] = transpilations
        response['transpilations_json'] = transpilations_json
        response['errors'] = {}
        return render_template('analysistemplate/execution_analyses.html', params=response)
    elif response['success'] == False:
        return render_template('analysistemplate/loading_q_system.html', params=response)
    else:
        return render_template("errortemplate/error.html")

    """ 
    """

@analysis_bp.route('/execution_analyses', methods=['GET', 'POST'])
def execution_analyses():
    service = AnalysisServiceImpl()
    keys = ["id_qs", "name_qs", "optimization", "files_json", "transpilations_json"]
    keys_list = ["files_selected", "transpilations_selected"]
    attributes = utils.get_attributes_from_list_of_request(request, keys, keys_list)
    response = service.execution_analyses(attributes)
    if response['success']:
        page_html = 'analysistemplate/names_transpilation.html'
    elif response['success'] == False:
        page_html = 'analysistemplate/execution_analyses.html'
    else:
        page_html = 'errortemplate/error.html'
    return render_template(page_html, params=response)

@analysis_bp.route('/display_analysis', methods=['GET', 'POST'])
def display_analysis():
    service = AnalysisServiceImpl()
    keys = ['id_qs', 'name_qs', 'save_date', 'id_analysis', 'name_transpilation', 'optimization']
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.display_analysis(attributes)
    if response['success']:
        page_html = 'analysistemplate/analysis.html'
    else:
        page_html = 'errortemplate/error.html'
    return render_template(page_html, params=response)
    """
    """

@analysis_bp.route('/display_form_deletion_analysis', methods=['GET', 'POST'])
def display_form_deletion_analysis():
    service = AnalysisServiceImpl()
    keys = ["id_analysis", "id_qs", "name_transpilation", "route", "save_date_qs", "name_qs"]
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.display_form_deletion_analysis(attributes)
    if response['success']:
        page_html = "analysistemplate/deletion_analysis.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """

@analysis_bp.route('/deletion_analysis', methods=['GET', 'POST'])
def deletion_analysis():
    service = AnalysisServiceImpl()
    keys = ["id_analysis", "name_transpilation", "id_qs"]
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.deletion_analysis(attributes)
    if response['success']:
        page_html = "analysistemplate/analyses_transpilation_selected.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """














