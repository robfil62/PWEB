from sqlalchemy import *
from sqlalchemy.sql import *


def get_bd(budget,lieu,date_depart,date_retour):
    data= []
    villes = []
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    print(lieu)
    for row in connection.execute("select * from Offre where (prix_offre <= ?) and (ville_depart == ?) and (date_offre >= ?)",budget,lieu,date_depart):
        data.append(row)

    for row in connection.execute("select ville_depart from Offre where (prix_offre <= ?) and (ville_depart == ?) and (date_offre >= ?)",budget,lieu,date_depart):
        villes.append(row)

    for ville in villes:
        for row in connection.execute("select * from Offre where (prix_offre <= ?)and (ville_depart == ?) and (date_offre <= ?)",budget,ville[0],date_retour):
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
    connection.execute("insert into NewVendeur (nom_vendeur,email,mdp) values (?,?,?)", nom_vendeur,email,mdp)
    connection.close()

def new_offer_bd(destination, transport, depart, date, prix,lien, offreur):
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("insert into NewOffre (ville, nom_vendeur, moyen_transport, ville_depart,date_offre,prix_offre,site) values (?,?,?,?,?,?,?)", destination,offreur,transport,depart,date,prix,lien)
    connection.close()
