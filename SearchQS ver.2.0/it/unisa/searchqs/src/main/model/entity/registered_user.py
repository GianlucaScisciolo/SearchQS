class RegisteredUser:
    def __init__(self, email="", name="", surname="", gender="", birthdate="", city_birthplace="", nation_birthplace="", 
                 nationality="", profession=None, num_cellphone=None, password="", salt_hex="", id_residential_address=0):
        self.email = email
        self.name = name
        self.surname = surname
        self.gender = gender
        self.birthdate = birthdate
        self.city_birthplace = city_birthplace
        self.nation_birthplace = nation_birthplace
        self.nationality = nationality
        self.profession = profession
        self.num_cellphone = num_cellphone
        self.password = password
        self.salt_hex = salt_hex
        self.id_residential_address = id_residential_address
    
    def __str__(self):
        return (f"RegisteredUser(email={self.email}, name={self.name}, surname={self.surname}, gender={self.gender}, " 
                f"birthdate={self.birthdate}, city_birthplace={self.city_birthplace}, " 
                f"nation_birthplace={self.nation_birthplace}, nationality={self.nationality}, " 
                f"profession={self.profession}, num_cellphone={self.num_cellphone}, password={self.password}, " 
                f"salt_hex={self.salt_hex}, id_residential_address={self.id_residential_address})")

    def __eq__(self, other):
        if isinstance(other, RegisteredUser):
            return (self.email == other.email and self.name == other.name and self.surname == other.surname 
                    and self.gender == other.gender and self.birthdate == other.birthdate 
                    and self.city_birthplace == other.city_birthplace 
                    and self.nation_birthplace == other.nation_birthplace and self.nationality == other.nationality 
                    and self.profession == other.profession and self.num_cellphone == other.num_cellphone 
                    and self.password == other.password and self.salt_hex == other.salt_hex 
                    and self.id_residential_address == other.id_residential_address)
        return False

    def set_by_attributes(self, attributes, prefix=""):
        if prefix is None:
            prefix = ""
        self.email = attributes.get(f'{prefix}email_ru', "")
        self.name = attributes.get(f'{prefix}name_ru', "")
        self.surname = attributes.get(f'{prefix}surname_ru', "")
        self.gender = attributes.get(f'{prefix}gender_ru', "")
        self.birthdate = attributes.get(f'{prefix}birthdate_ru', "")
        self.city_birthplace = attributes.get(f'{prefix}city_birthplace_ru', "")
        self.nation_birthplace = attributes.get(f'{prefix}nation_birthplace_ru', "")
        self.nationality = attributes.get(f'{prefix}nationality_ru', "")
        self.profession = attributes.get(f'{prefix}profession_ru', None)
        self.num_cellphone = attributes.get(f'{prefix}num_cellphone_ru', None)
        self.password = attributes.get(f'{prefix}password_ru', "")
        self.salt_hex = attributes.get(f'{prefix}salt_hex_ru', "")
        self.id_residential_address = attributes.get(f'{prefix}id_residential_address_ru', 0)








