from src.main.service.sitoservice.i_sito_service import ISitoService
from flask import session

class SitoServiceImpl(ISitoService):
  def cambio_lingua(self):
    if "lingua" not in session:
      session["lingua"] = "inglese"
    else:
      if session["lingua"] == "italiano":
        session["lingua"] = "inglese"
      else: 
        session["lingua"] = "italiano"
    return {'success': True, 'errors': {}}

  def cambio_tema(self):
    if "tema" not in session:
      session["tema"] = "dark"
    else:
      if session["tema"] == "light":
        session["tema"] = "dark"
      else: 
        session["tema"] = "light"
    return {'success': True, 'errors': {}}









