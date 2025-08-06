from flask import Blueprint, render_template, request, session, redirect, url_for
# import requests
#from flask import Blueprint, redirect, url_for, request
from src.main.service.sitoservice.sito_service_impl import SitoServiceImpl

sito_bp = Blueprint('sito', __name__)

@sito_bp.route('/cambio_lingua', methods=['GET', 'POST'])
def cambio_lingua():
    service = SitoServiceImpl()
    response = service.cambio_lingua()
    return render_template('home.html')










