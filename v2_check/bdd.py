from mysql.connector import connect

class Dtb():
    def __init__ (self):
        self.mydb = connect(
                    host="192.168.1.58",
                    user="bdd",
                    passwd="nqutic",
                    database="interface"
                    ) 
    
        self.mycursor = self.mydb.cursor()
        
    def execute(self,txt):
        self.mycursor.execute(txt)
        return self.mycursor.fetchall()
        


