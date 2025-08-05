from src.main.model.entity.registered_user import RegisteredUser
from src.main.model.entity.residential_address import ResidentialAddress
import src.main.service.utils.check as check
from src.main.service.utils.security import password_is_correct
import datetime

def check_registration(attributes):
    errors = {
        'name_ru': "",
        'surname_ru': "",
        'gender_ru': "",
        'birthdate_ru': "",
        'birthplace_ru': "",
        'nationality_ru': "",
        'profession_ru': "",
        'num_cellphone_ru': "",
        'email_ru': "",
        'password_ru': "",
        'confirm_password_ru': "",
        'residential_address_ru': "",
    }

    num_errors = 0

    """ Controllo name_ru """
    if not check.length_is_in_range(attributes['name_ru'], 1, 25):
        errors['name_ru'] += "La lunghezza del nome deve essere tra 1 e 25 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['name_ru'], r"^[A-Za-zÀ-ù '-]{1,25}$"):
        errors['name_ru'] += "Il formato del nome non è valido.\n"
        num_errors += 1

    """ Controllo surname_ru """
    if not check.length_is_in_range(attributes['surname_ru'], 1, 25):
        errors['surname_ru'] += "La lunghezza del cognome deve essere tra 1 e 25 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['surname_ru'], r"^[A-Za-zÀ-ù '-]{1,25}$"):
        errors['surname_ru'] += "Il formato del cognome non è valido.\n"
        num_errors += 1

    """ Controllo gender_ru """
    if not check.is_present_in_elements(attributes['gender_ru'], {'M', 'F', 'N'}):
        errors['gender_ru'] += "Genere inserito non valido.\n"
        num_errors += 1

    """ Controllo birthdate_ru """
    if check.is_empty(attributes['birthdate_ru']) or not check.date_is_in_range_years(attributes['birthdate_ru'], 14, 101):
        errors['birthdate_ru'] += "Data di nascita inserita non valida, deve essere compresa tra i 14 anni e i 101 anni.\n"
        num_errors += 1

    """ Controllo city_birthplace_ru """
    if not check.length_is_in_range(attributes['city_birthplace_ru'], 1, 34):
        errors['birthplace_ru'] += "La lunghezza della citta\' di nascita deve essere tra 1 e 34 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['city_birthplace_ru'], r"^[A-Za-zÀ-ù '-]{1,34}$"):
        errors['birthplace_ru'] += "Il formato della citta\' di nascita non e\' valido.\n"
        num_errors += 1

    """ Controllo nation_birthplace_ru """
    if not check.length_is_in_range(attributes['nation_birthplace_ru'], 1, 56):
        errors['birthplace_ru'] += "La lunghezza della nazione di nascita deve essere tra 1 e 56 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['nation_birthplace_ru'], r"^[A-Za-zÀ-ù '-]{1,56}$"):
        errors['birthplace_ru'] += "Il formato della nazione di nascita non e\' valido.\n"
        num_errors += 1

    """ Controllo nationality_ru """
    if not check.length_is_in_range(attributes['nationality_ru'], 1, 56):
        errors['nationality_ru'] += "La lunghezza della nazionalita\' deve essere tra 1 e 56 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['nationality_ru'], r"^[A-Za-zÀ-ù '-]{1,56}$"):
        errors['nationality_ru'] += "Il formato della nazionalita\' non e\' valido.\n"
        num_errors += 1

    """ Controllo profession_ru """
    if not check.length_is_in_range(attributes['profession_ru'], 0, 25):
        errors['profession_ru'] += "La lunghezza della professione deve essere tra 0 e 25 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['profession_ru'], r"^[A-Za-zÀ-ù '-]{0,25}$"):
        errors['profession_ru'] += "Il formato della professione non e\' valido.\n"
        num_errors += 1

    """ Controllo num_cellphone_ru """
    if not check.length_is_in_range(attributes['num_cellphone_ru'], 0, 0):
        if not check.length_is_in_range(attributes['num_cellphone_ru'], 10, 10):
            errors['num_cellphone_ru'] += "Il numero di cellulare deve contenere 10 numeri da 1 a 9.\n"
            num_errors += 1
        if not check.regex_is_respected(attributes['num_cellphone_ru'], r"^3[0-9]{9}$"):
            errors['num_cellphone_ru'] += "Il formato del numero di cellulare non e\' valido. Il primo numero deve essere 3.\n"
            num_errors += 1

    """ Controllo email_ru """
    if not check.length_is_in_range(attributes['email_ru'], 6, 254):
        errors['email_ru'] += "La lunghezza dell\'email deve essere tra 6 e 254 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['email_ru'], r"^([a-z\d\._-]+)@([a-z\d-]+)\.([a-z]{2,8})(\.[a-z]{2,8})?$"):
        errors['email_ru'] += "Il formato dell\'email non e\' valido.\n"
        num_errors += 1

    """ Controllo password_ru """
    if not check.length_is_in_range(attributes['password_ru'], 8, 128):
        errors['password_ru'] += "La lunghezza della password deve essere tra 8 e 128 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['password_ru'], r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&#_])[A-Za-z\d@$!%*?&#_]{8,128}$"):
        errors['password_ru'] += """
Il formato della password non e\' valido. Deve avere almeno:
- 1 lettera maiuscola.
- 1 lettera minuscola.
- 1 carattere speciale tra i seguenti: @ $ ! % * ? & # _.
- 1 numero.
        """
        num_errors += 1

    """ Controllo confirm_password """
    if not check.is_equal(attributes['password_ru'], attributes['confirm_password_ru']):
        errors['confirm_password_ru'] += "Le 2 password inserite non sono uguali.\n"
        num_errors += 1

    """ Controllo name_ra """
    if not check.length_is_in_range(attributes['name_ra'], 1, 50):
        errors['residential_address_ru'] += "La lunghezza del nome deve essere tra 1 e 50 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['name_ra'], r"^[A-Za-zÀ-ù '-]{1,50}$"):
        errors['residential_address_ru'] += "Il formato del nome non e\' valido.\n"
        num_errors += 1

    """ Controllo number_ra """
    if check.is_empty(attributes['number_ra']) or not check.number_int_is_in_range_numbers_int(attributes['number_ra'], 1, 14500):
        errors['residential_address_ru'] += "Il numero civico deve essere compreso tra 1 e 14500 estremi inclusi.\n"
        num_errors += 1

    """ Controllo city_ra """
    if not check.length_is_in_range(attributes['city_ra'], 1, 34):
        errors['residential_address_ru'] += "La lunghezza della citta\' deve essere tra 1 e 34 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['city_ra'], r"^[A-Za-zÀ-ù '-]{1,34}$"):
        errors['residential_address_ru'] += "Il formato della citta\' non e\' valido.\n"
        num_errors += 1

    """ Controllo province_ra """
    if not check.regex_is_respected(attributes['province_ra'], r"^[A-Z]{2}$"):
        errors['residential_address_ru'] += "La provincia deve essere costituita solamente da 2 lettere maiuscole.\n"
        num_errors += 1

    """ Controllo cap_ra """
    if not check.regex_is_respected(attributes['cap_ra'], r"^[0-9]{5}$"):
        errors['residential_address_ru'] += "La provincia deve essere costituita solamente da 5 numeri che vanno da 0 a 9.\n"
        num_errors += 1

    if num_errors == 0:
        errors = {}
    return [errors, num_errors]

def check_registration_registered_user_is_present(ru_db):
    errors = {
        'email_ru': ""
    }

    num_errors = 0
    if ru_db != []:
        errors['email_ru'] += "Utente con la stessa e-mail gia\' presente.\n"
        num_errors += 1
    
    return [errors, num_errors]
    
def check_login(attributes):
    errors = {
        'email_ru': "",
        'password_ru': ""
    }

    num_errors = 0

    """ Controllo email_ru """
    if not check.length_is_in_range(attributes['email_ru'], 6, 254):
        errors['email_ru'] += "La lunghezza dell\'e-mail deve essere tra 6 e 254 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['email_ru'], r"^([a-z\d\._-]+)@([a-z\d-]+)\.([a-z]{2,8})(\.[a-z]{2,8})?$"):
        errors['email_ru'] += "Il formato dell\'e-mail non e\' valido.\n"
        num_errors += 1
    
    """ Controllo password_ru """
    if not check.length_is_in_range(attributes['password_ru'], 8, 128):
        errors['password_ru'] += "La lunghezza della password deve essere tra 8 e 128 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['password_ru'], r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&#_])[A-Za-z\d@$!%*?&#_]{8,128}$"):
        errors['password_ru'] += """
Il formato della password non e\' valido. Deve avere almeno:
- 1 lettera maiuscola.
- 1 lettera minuscola.
- 1 carattere speciale tra i seguenti: @ $ ! % * ? & # _.
- 1 numero.
        """
        num_errors += 1
    if num_errors == 0:
        errors = {}
    return [errors, num_errors]

def check_login_authentication(ru_db, password_ru):
    errors = {
        'form_login': ""
    }

    num_errors = 0

    if ( (ru_db == []) or (not password_is_correct(password_ru, ru_db.password, ru_db.salt_hex)) ):
        errors['form_login'] += "Password e/o e-mail non corretta.\n"
        num_errors += 1
    if num_errors == 0:
        errors = {}
    return [errors, num_errors]
    
def check_loading_q_system(attributes):
    errors = {
        'file': ""
    }
    num_errors = 0
    length = len(attributes['filename']) - 4
    if not attributes['filename'].endswith('.zip'):
        errors['file'] = "Il sistema quantistico caricato non è del tipo .zip.\n"
        num_errors += 1
    if not check.length_is_in_range(attributes['filename'][:length], 1, 30):
        errors['file'] += "La lunghezza del nome del sistema quantistico deve essere tra 1 e 30 estremi inclusi.\n"
        num_errors += 1
    return [errors, num_errors]

def check_execution_analyses(attributes):
    errors = {
        'files_selected': "",
        'transpilations_selected': "",
        'optimization': ""
    }
    num_errors = 0
    if check.is_empty(attributes['files_selected']):
        errors['files_selected'] = "Nessun file selezionato. Seleziona almeno un file.\n"
        num_errors += 1
    if check.is_empty(attributes['transpilations_selected']):
        errors['transpilations_selected'] = "Nessun scelta selezionata. Seleziona almeno una scelta.\n"
        num_errors += 1
    if not check.number_int_is_in_range_numbers_int(attributes['optimization'], 0, 3):
        errors['optimization'] = "Non e\' stato scelto il tipo di ottimizzazione (tra 0 e 3 estremi inclusi).\n"
        num_errors += 1
    return [errors, num_errors]

def check_modification_personal_data(attributes, current_email, ru_db):
    errors = {
        'profession_ru': "",
        'num_cellphone_ru': "",
        'email_ru': "",
        'password_ru': "",
        'confirm_password_ru': "",
        'residential_address_ru': ""
    }
    num_errors = 0

    """ Controllo profession_ru """
    if not check.length_is_in_range(attributes['profession_ru'], 0, 25):
        errors['profession_ru'] += "La lunghezza della professione deve essere tra 0 e 25 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['profession_ru'], r"^[A-Za-zÀ-ù '-]{0,25}$"):
        errors['profession_ru'] += "Il formato della professione non e\' valido.\n"
        num_errors += 1

    """ Controllo num_cellphone_ru """
    if not check.length_is_in_range(attributes['num_cellphone_ru'], 0, 0):
        if not check.length_is_in_range(attributes['num_cellphone_ru'], 10, 10):
            errors['num_cellphone_ru'] += "Il numero di cellulare deve contenere 10 numeri da 1 a 9.\n"
            num_errors += 1
        if not check.regex_is_respected(attributes['num_cellphone_ru'], r"^3[0-9]{9}$"):
            errors['num_cellphone_ru'] += "Il formato del numero di cellulare non e\' valido. Il primo numero deve essere 3.\n"
            num_errors += 1

    """ Controllo email_ru """
    if not check.length_is_in_range(attributes['email_ru'], 6, 254):
        errors['email_ru'] += "La lunghezza dell\'email deve essere tra 6 e 254 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['email_ru'], r"^([a-z\d\._-]+)@([a-z\d-]+)\.([a-z]{2,8})(\.[a-z]{2,8})?$"):
        errors['email_ru'] += "Il formato dell\'email non e\' valido.\n"
        num_errors += 1

    """ Controllo password_ru """
    if not check.length_is_in_range(attributes['password_ru'], 8, 128):
        errors['password_ru'] += "La lunghezza della password deve essere tra 8 e 128 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['password_ru'], r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&#_])[A-Za-z\d@$!%*?&#_]{8,128}$"):
        errors['password_ru'] += """
Il formato della password non e\' valido. Deve avere almeno:
- 1 lettera maiuscola.
- 1 lettera minuscola.
- 1 carattere speciale tra i seguenti: @ $ ! % * ? & # _.
- 1 numero.
        """
        num_errors += 1

    if not check.is_equal(attributes["password_ru"], attributes["confirm_password_ru"]):
        errors['confirm_password_ru'] = "Le 2 password inserite non sono uguali."
        num_errors += 1

    """ Controllo name_ra """
    if not check.length_is_in_range(attributes['name_ra'], 1, 50):
        errors['residential_address_ru'] += "La lunghezza del nome deve essere tra 1 e 50 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['name_ra'], r"^[A-Za-zÀ-ù '-]{1,50}$"):
        errors['residential_address_ru'] += "Il formato del nome non e\' valido.\n"
        num_errors += 1

    """ Controllo number_ra """
    if check.is_empty(attributes['number_ra']) or not check.number_int_is_in_range_numbers_int(attributes['number_ra'], 1, 14500):
        errors['residential_address_ru'] += "Il numero civico deve essere compreso tra 1 e 14500 estremi inclusi.\n"
        num_errors += 1

    """ Controllo city_ra """
    if not check.length_is_in_range(attributes['city_ra'], 1, 34):
        errors['residential_address_ru'] += "La lunghezza della citta\' deve essere tra 1 e 34 estremi inclusi.\n"
        num_errors += 1
    if not check.regex_is_respected(attributes['city_ra'], r"^[A-Za-zÀ-ù '-]{1,34}$"):
        errors['residential_address_ru'] += "Il formato della citta\' non e\' valido.\n"
        num_errors += 1

    """ Controllo province_ra """
    if not check.regex_is_respected(attributes['province_ra'], r"^[A-Z]{2}$"):
        errors['residential_address_ru'] += "La provincia deve essere costituita solamente da 2 lettere maiuscole.\n"
        num_errors += 1

    """ Controllo cap_ra """
    if not check.regex_is_respected(attributes['cap_ra'], r"^[0-9]{5}$"):
        errors['residential_address_ru'] += "La provincia deve essere costituita solamente da 5 numeri che vanno da 0 a 9.\n"
        num_errors += 1

    """ Controllo se l'email è associata ad un altro utente """
    if num_errors == 0 and attributes['email_ru'] != current_email and ru_db != []:
        errors['email_ru'] += "Utente con l\'email inserita gia\' presente.\n"
        num_errors += 1

    return [errors, num_errors]

















