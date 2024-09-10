import mysql.connector

class MySQLConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open(self):
        try:
            self.connection = mysql.connector.connect (
                host="host",
                user="user",
                password="password",
                database="testsearchqs" # oppure searchqs se non testiamo
            )
            self.cursor = self.connection.cursor()
            return True
        except mysql.connector.Error as e:
            print(f"Si è verificato un errore durante la connessione al database: {e}")
            self.connection = None
            self.cursor = None
            return False
    
    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            return True
        except mysql.connector.Error as e:
            print(f"Si è verificato un errore durante la chiusura della connessione al database: {e}")
            return False

    def fetchall(self):
        ris = self.cursor.fetchall()
        return ris

    def commit(self):
        return self.connection.commit()

    def rollback(self):
        return self.connection.rollback()

    def start_transaction(self):
        return self.connection.start_transaction()

    def rowcount(self):
        return self.connection.cursor().rowcount





