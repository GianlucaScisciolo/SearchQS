class ResidentialAddress:
    def __init__(self, id=0, name="", number=0, city="", province="", cap=""):
        self.id = id
        self.name = name
        self.number = number
        self.city = city
        self.province = province
        self.cap = cap
    
    def set_by_attributes(self, attributes, prefix=""):
        if prefix is None:
            prefix = ""
        self.id = attributes.get(f'{prefix}id_ra', 0)
        self.name = attributes.get(f'{prefix}name_ra', "")
        self.number = attributes.get(f'{prefix}number_ra', 0)
        self.city = attributes.get(f'{prefix}city_ra', "")
        self.province = attributes.get(f'{prefix}province_ra', "")
        self.cap = attributes.get(f'{prefix}cap_ra', "")

    def __str__(self):
        return (f"ResidentialAddress(id={self.id}, name={self.name}, number={self.number}, city={self.city}, "
                f"province={self.province}, cap={self.cap})")

    def __eq__(self, other):
        if isinstance(other, ResidentialAddress):
            return (self.id == other.id and self.name == other.name and self.number == other.number 
                    and self.city == other.city and self.province == other.province and self.cap == other.cap)
        return False









