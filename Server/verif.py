
import sqlite3
from sqlalchemy import *
from sqlalchemy.sql import *
import requests


def new_offer():
    data_1= []
    data_2= []
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select * from Offre where (validation==0)"):      #les offres non verifiées dans data_1
        data_1.append(row)
    for row in connection.execute("select * from Offre where (validation==1)"):      #les offres validées dans data_2
        data_2.append(row)

    for i in range (0,len(data_1)):                         #on verifie que l'offre n'existe pas déjà
        for j in (0,range len(data_2)):
            C=0
            for k in range(1,8):
                if data_1[i][k]==data_2[j][k]:
                    C+=1
            if C==7:                                        #si l'offre est identique (tous attributs sauf id) à une offre deja existante, elle est supprimée
                    connection.execute("delete from Offre where id_offre=?",data_1[i][0])    
        
        r = requests.get(data_1[i][7])          
        if r.status_code != 200:                            #si le lien n'est pas valide on supprime
                    connection.execute("delete from Offre where id_offre=?",data_1[i][0])


    connection.close()




