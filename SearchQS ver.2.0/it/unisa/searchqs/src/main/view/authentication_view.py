from flask import Blueprint, render_template, request, session, redirect, url_for
from src.main.service.authenticationservice.authentication_service_impl import AuthenticationServiceImpl
import requests
from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress
from src.main.view.utils import utils

authentication_bp = Blueprint('authentication', __name__)

@authentication_bp.route('/display_form_registration', methods=['GET', 'POST'])
def display_form_registration():
    service = AuthenticationServiceImpl()
    response = service.display_form_registration()
    page_html = ""
    if response['success']:
        page_html = "authenticationtemplate/registration.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)

@authentication_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    service = AuthenticationServiceImpl()
    keys = ["name_ru","surname_ru","gender_ru","birthdate_ru","city_birthplace_ru","nation_birthplace_ru", 
            "nationality_ru","profession_ru","num_cellphone_ru","email_ru","password_ru", "name_ra","number_ra", 
            "city_ra","province_ra","cap_ra","confirm_password_ru"]        
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.registration(attributes)
    page_html = ""
    if response['success']:
        page_html = 'authenticationtemplate/login.html'
    elif response['success'] == False:
        page_html = 'authenticationtemplate/registration.html'
    else:
        return render_template("errortemplate/error.html")
    return render_template(page_html, params=response)

    '''
    elif response['errors'] != {}:
        response = utils.get_response_from_list_of_request(request, response, keys)
        return render_template('authenticationtemplate/registration.html', params=response)
    '''

@authentication_bp.route('/display_form_login', methods=['GET', 'POST'])####
def display_form_login():
    service = AuthenticationServiceImpl()
    response = service.display_form_login()
    page_html = ""
    if response['success']:
        page_html = "authenticationtemplate/login.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)

@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    service = AuthenticationServiceImpl()
    keys = ["email_ru","password_ru"]
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.login(attributes)
    page_html = ""
    if response['success']:
        page_html = 'home.html'
    elif response['success'] == False:
        page_html = 'authenticationtemplate/login.html'
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    
@authentication_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    service = AuthenticationServiceImpl()
    service.logout()
    return render_template('home.html')
''' 
'''








