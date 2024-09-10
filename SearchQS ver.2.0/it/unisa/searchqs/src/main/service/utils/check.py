import re
import datetime
from datetime import datetime, timedelta

def is_none(attribute):
    return attribute is None
    
def length_is_in_range(string, min, max):
    return ( (len(string) <= max) and (len(string) >= min) )

def regex_is_respected(string, regex_str):
    return re.search( re.compile(regex_str), string)

def is_present_in_elements(attribute, elements):
    return attribute in elements

def date_is_in_range_years(date, year_min, year_max):
    date = datetime.strptime(date, '%Y-%m-%d')
    current_date = datetime.now()
    date_min = current_date - timedelta(days=year_max*365)
    date_max = current_date - timedelta(days=year_min*365)
    return ( (date >= date_min) and (date <= date_max) )

def is_equal(el_1, el_2):
    return (el_1 == el_2)

def number_int_is_in_range_numbers_int(number, min: int, max: int):
    return ( (int(number) >= min) and (int(number) <= max) )

def is_empty(el):
    return len(el) == 0







