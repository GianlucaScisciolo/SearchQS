class SourceFile:
    def __init__(self, id=0, path="", file=""):
        self.id = id
        self.path = path
        self.file = file

    def __str__(self):
        return (f"SourceFile(id={self.id}, path={self.path}, file={self.file})")

    def __eq__(self, other):
        if not isinstance(other, SourceFile):
            return False
        return (self.id == other.id and self.path == other.path and self.file == other.file)

    def get_code_from_file(self):
        if self.file != "" and self.file is not None:
            return self.file.decode('utf-8')
        return ""
        
    def set_file_from_code(self, code):
        if code != "" and code is not None:
            self.file = code.encode('utf-8')
        else:
            self.file = ""







	