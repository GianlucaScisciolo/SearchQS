class QSystem:
    def __init__(self, id=0, name="", email_registered_user=""):
        self.id = id
        self.name = name
        self.email_registered_user = email_registered_user
        
    def __str__(self):
        return (f"QSystem(id={self.id}: {type(self.id)}, name={self.name}: {type(self.name)}, "
                f"email_registered_user={self.email_registered_user}: {type(self.email_registered_user)})")
        
    def __eq__(self, other):
        if isinstance(other, QSystem):
            return (
                self.id == other.id
                and self.name == other.name
                and self.email_registered_user == other.email_registered_user
            )
        return False









