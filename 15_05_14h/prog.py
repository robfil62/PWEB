from sqlalchemy import *
from sqlalchemy.sql import *
from flask import *
import requests


def get_bd(budget,lieu,date_depart,date_retour):
    data=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()

    for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site from Offre where (prix_offre <= ?) and (ville_depart == ?) and (date_offre >= ?)",budget,lieu,date_depart):
        data.append(row)

    for destination in data:
        print(destination[1])
        for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site from Offre where (prix_offre <= ?) and (ville_depart == ?) and (ville==?)",budget,destination[1],lieu):
            data.append(row)
            print(row)

    connection.close()
    return data


def get_adv_bd(budget,lieu,date_aller,date_retour,meteo,environnement,urbanisme):
    data=[]
    data_adv=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()

    for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site from Offre as o, Destination as d, Meteo as m where (o.prix_offre <= ?) and (o.ville_depart == ?) and (o.date_offre >= ?) and (d.ville==o.ville) and (d.environnement==?) and (d.urbanisme==?) and (o.ville==m.ville) and (m.meteo==?) and (m.date_debut>=?) and (m.date_fin<=?)",budget,lieu,date_aller, environnement, urbanisme,meteo, date_aller, date_aller):
        data.append(row)

    for recherches in data:
        ville=recherches[1]
        for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site from Offre as o, Destination as d, Meteo as m where (d.ville==?) and (m.ville== ?) and (d.environnement==?) and (d.urbanisme==?) and (m.meteo==?) and (m.date_debut>=?) and (m.date_fin<=?)",ville, ville,environnement,urbanisme,meteo,date_aller,date_retour):
            data_adv.append(row)

    if data_adv==[]:
        return data

    else:
        return data_adv

    connection.close()

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

def new_offer_bd(destination, transport, depart, date,prix,lien, offreur):
    data=[]
    prix=float(prix)
    offer=[destination,offreur,transport,depart,date,prix,lien]

    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()

    for row in connection.execute("select * from Offre where (nom_vendeur==?)",offreur):
        data.append(row)

    try :
        r = requests.get(offer[6])
        if r.status_code != 200:
            connection.close()
            return "Erreur dans le lien"
    except:
        connection.close()
        return "Erreur dans le lien"

    for i in range (0,len(data)):
        C=0
        print(data[i])
        print("offre",offer)
        for k in range(1,8):
            print(data[i][k])
            print("offer ", offer[k-1])
            if data[i][k]==offer[k-1]:
                print("pzreil")
                C+=1

            if C==7:
                connection.close()
                return "Erreur dans l'offre"

    connection.execute("insert into Offre (ville, nom_vendeur, moyen_transport, ville_depart,date_offre,prix_offre,site) values (?,?,?,?,?,?,?)", destination,offreur,transport,depart,date,prix,lien)
    connection.close()
    return "Offre ajoutée"
