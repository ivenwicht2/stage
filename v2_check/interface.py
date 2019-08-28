from tkinter import *
from register import menu
from port_class import *
import bdd

def menu_start():
        #création de la fenêtre 
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
            #Bouton port
            frame = Frame(Mframe)
            if ligne == 3 :  colonne = 1
            frame.grid(column=colonne,row=ligne) 
            #Bouton enregister/ redirige vers le fichier register.pyo
            Button(frame,text="ENREGISTER", fg='white',command = lambda : menu(Mframe),bg='blue',width=20,height=5,font='lucida').grid(row = 0 ,column = 0)


def mysql():
        #Requête sql
        mycursor = bdd.Dtb()
        return mycursor.execute( 'select * from  port')
        
menu_start()
