from flask import Blueprint, render_template, request, session, redirect, url_for
from src.main.service.userareaservice.user_area_service_impl import UserAreaServiceImpl
from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress
import src.main.view.utils.utils as utils

user_area_bp = Blueprint('user_area', __name__)
@user_area_bp.route('/display_user_area', methods=['GET', 'POST'])
def display_user_area():
    service = UserAreaServiceImpl()
    response = service.display_user_area()
    if response['success']:
        page_html = "userareatemplate/user_area.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)

@user_area_bp.route('/display_form_deletion_account', methods=['GET', 'POST'])
def display_form_deletion_account():
    service = UserAreaServiceImpl()
    response = service.display_form_deletion_account()
    if response['success']:
        page_html = "userareatemplate/deletion_account.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """

@user_area_bp.route('/deletion_account', methods=['GET', 'POST'])
def deletion_account():
    service = UserAreaServiceImpl()
    response = service.deletion_account()
    if response['success']:
        page_html = "home.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """

@user_area_bp.route('/display_personal_data', methods=['GET', 'POST'])
def display_personal_data():
    service = UserAreaServiceImpl()
    response = service.display_personal_data()
    if response['success']:
        page_html = "userareatemplate/personal_data.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """

@user_area_bp.route('/modification_personal_data', methods=['GET', 'POST'])
def modification_personal_data():
    service = UserAreaServiceImpl()
    keys = ["profession_ru", "num_cellphone_ru", "email_ru", "password_ru", "confirm_password_ru", 
            "name_ra", "number_ra", "city_ra", "province_ra", "cap_ra", "id_ra"]
    attributes = utils.get_attributes_from_list_of_request(request, keys, None)
    response = service.modification_personal_data(attributes)
    if response['success'] or response['success'] == False:
        page_html = "userareatemplate/personal_data.html"
    else:
        page_html = "errortemplate/error.html"
    return render_template(page_html, params=response)
    """
    """


    





     