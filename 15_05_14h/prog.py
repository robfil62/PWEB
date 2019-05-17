from sqlalchemy import *
from sqlalchemy.sql import *
from flask import *
import requests


def get_bd(budget,lieu,date_depart,date_retour):
    res=[]
    retours=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()

    for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site from Offre where (prix_offre <= ?) and (ville_depart == ?) and (date_offre >= ?)",budget,lieu,date_depart):
        res.append(row)

    for destination in res:
        for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site from Offre where (prix_offre <= ?) and (ville_depart == ?) and (ville==?)",budget,destination[0],lieu):
            retours.append(row)

    for retour in retours:
        res.append(retour)

    connection.close()
    return res


def get_adv_bd(budget,lieu,date_aller,date_retour,meteo,environnement,urbanisme):
    res=[]
    res_adv=[]
    retours=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()

    for row in connection.execute("select o.ville, o.nom_vendeur, o.moyen_transport, o.ville_depart, o.date_offre, o.prix_offre, o.site from Offre as o, Destination as d, Meteo as m where (o.prix_offre <= ?) and (o.ville_depart == ?) and (o.date_offre >= ?) and (o.date_offre <= ?) and (d.ville==o.ville) and (d.environnement==?) and (d.urbanisme==?) and (o.ville==m.ville) and (m.meteo==?) and (strftime('%m',m.date_debut)<=strftime('%m',?)) and (strftime('%m',m.date_fin)>=strftime('%m',?))",budget,lieu,date_aller,date_retour, environnement, urbanisme,meteo, date_aller, date_retour):
        res_adv.append(row)

    for destination in res_adv:
        for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site from Offre where (prix_offre <= ?) and (ville_depart == ?) and (ville==?)",budget,destination[0],lieu):
            retours.append(row)


    for retour in retours:
        res_adv.append(retour)

    if res_adv==[]:
        return [get_bd(budget,lieu,date_aller,date_retour),"Nous ne trouvons aucune offre qui corresponde parfaitement à votre demande"]

    else:
        return [res_adv,"Votre recherche a abouti"]

    connection.close()
def verif_login_bd(pseudo, mdp, type):
    data=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    if type=='client':
        for row in connection.execute("select pseudo_client, mdp, email from Client where (pseudo_client = ?) and (mdp = ?)",pseudo,mdp):
            data.append(row)
            print("datatata ",data)

    if type=='vendeur':
        for row in connection.execute("select * from Vendeur where (nom_vendeur = ?) and (mdp = ?) and (validation==1)",pseudo,mdp):
            data.append(row)

    if type=='admin':
        for row in connection.execute("select * from Vendeur where (nom_vendeur = ?) and (mdp = ?) ",pseudo,mdp):
            data.append(row)

    connection.close()
    if (len(data)!=1):
        return -1

    else:
        print(data[0][0])
        return data[0][0]

def regist_vendeur_bd(nom_vendeur, email, mdp):
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("insert into Vendeur (nom_vendeur,email,mdp) values (?,?,?)", nom_vendeur,email,mdp)
    connection.close()

def regist_client_bd(nom_client, email, mdp):
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("insert into Client (pseudo_client,mdp,email) values (?,?,?)", nom_client,mdp,email)
    connection.close()

def new_offer_bd(destination, transport, depart, date,prix,lien, offreur):
    data=[]
    dest=[]
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
        for k in range(1,8):
            if data[i][k]==offer[k-1]:
                C+=1

            if C==7:
                connection.close()
                return "Erreur dans l'offre"

    connection.execute("insert into Offre (ville, nom_vendeur, moyen_transport, ville_depart,date_offre,prix_offre,site,validation) values (?,?,?,?,?,?,?,1)", destination,offreur,transport,depart,date,prix,lien)

    for row in connection.execute("select * from Destination where (ville==?)",destination):
        dest.append(row)

    if dest==[]:
        connection.execute("insert into Destination (ville, pays, environnement, urbanisme) values (?,NULL,NULL,NULL)",destination)
        connection.execute("insert into Meteo (ville, date_debut, date_fin,meteo) values (?,NULL,NULL,NULL)", destination)

    connection.close()
    return "Offre ajoutée"

def get_new_dest():
    villes=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select d.ville, d.pays, d.environnement, d.urbanisme, m.date_debut, m.date_fin, m.meteo from Destination as d, Meteo as m where (d.pays is NULL) and (d.ville==m.ville) order by d.ville"):
        villes.append(row)

    connection.close()
    return villes

def get_new_vendeur():
    vendeurs=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select nom_vendeur, email, mdp from Vendeur where (validation is NULL)"):
        vendeurs.append(row)

    connection.close()
    return vendeurs


def update_new_dest(ville,pays,environnement,urbanisme):
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("update into Destination (ville,pays,environnement,urbanisme) values (?,?,?,?)", ville,pays,environnement,urbanisme)
    connection.close()

def update_new_met(ville,date_debut,date_fin,meteo):
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("update into Meteo (ville,date_debut,date_fin,meteo) values (?,?,?,?)", ville,date_debut,date_fin,meteo)
    connection.close()
