from tkinter import *
import register
from port_class import *
import bdd
def menu():
        window = Tk()
        window.title('menu')
        window.resizable(width=False, height=False)
        requete = mysql()
        display(window,requete)
        window.mainloop()


def display(Mframe,port):
            ligne = 1
            colonne = 1
           
            for item in port:
                if ligne == 3 :
                    ligne = 1
                    colonne +=1
                try :
                    Port(Mframe,item[0],colonne,ligne)
                except Exception as e :
                    print(e)
                ligne+=1
            frame = Frame(Mframe)
            if ligne == 3 :  colonne = 1
            frame.grid(column=colonne,row=ligne)
            Button(frame,text="ENREGISTER", fg='white',command = lambda : register.menu(Mframe),bg='blue',width=20,height=5).grid(row = 0 ,column = 0)


def mysql():
        mycursor = bdd.Dtb()
        return mycursor.execute( 'select * from  port')
        
menu()
