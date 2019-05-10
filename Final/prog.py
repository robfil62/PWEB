from sqlalchemy import *
from sqlalchemy.sql import *


def get_bd(budget):
    data= []
    engine = create_engine('sqlite:///BASE.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select * from Offre where (prix_offre <= ?)",budget):
        data.append(row)

    connection.close()

    return data

def verif_login_bd(pseudo, mdp):
    data=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select * from Vendeur where (nom_vendeur = ?) and (mdp = ?)",pseudo,mdp):
        data.append(row)

    connection.close()
    if (len(data)!=1):
        return -1

    else:
        return data[0][0]


def regist_vendeur_bd(nom_vendeur, email, mdp):
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("insert into Vendeur (nom_vendeur,email,mdp) values (?,?,?)", nom_vendeur,email,mdp)
    connection.close()
