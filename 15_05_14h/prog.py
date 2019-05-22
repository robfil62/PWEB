from sqlalchemy import *
from sqlalchemy.sql import *
from flask import *

def get_bd(budget,lieu,date_depart,date_retour):    #Recherche simple
    res=[]
    retours=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site, id_offre from Offre where (prix_offre <= ?) and (ville_depart == ?) and (date_offre >= ?) and (date_offre<=?)",budget,lieu,date_depart,date_retour):
        res.append(row)

    for destination in res: #Récupère aussi les retours
        for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site, id_offre from Offre where (prix_offre <= ?) and (ville_depart == ?) and (ville==?)",budget,destination[0],lieu):
            retours.append(row)
    for retour in retours:
        res.append(retour)

    connection.close()
    return res

def get_adv_bd(budget,lieu,date_aller,date_retour,meteo,environnement,urbanisme):   #Recherche avancée
    res=[]
    res_adv=[]
    retours=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select o.ville, o.nom_vendeur, o.moyen_transport, o.ville_depart, o.date_offre, o.prix_offre, o.site, o.id_offre from Offre as o, Destination as d, Meteo as m where (o.prix_offre <= ?) and (o.ville_depart == ?) and (o.date_offre >= ?) and (o.date_offre <= ?) and (d.ville==o.ville) and (d.environnement==?) and (d.urbanisme==?) and (o.ville==m.ville) and (m.meteo==?) and (strftime('%m',m.date_debut)<=strftime('%m',?)) and (strftime('%m',m.date_fin)>=strftime('%m',?))",budget,lieu,date_aller,date_retour, environnement, urbanisme,meteo, date_aller, date_retour):
        res_adv.append(row)

    for destination in res_adv: #Recherche les retours
        for row in connection.execute("select ville, nom_vendeur, moyen_transport, ville_depart, date_offre, prix_offre, site, id_offre from Offre where (prix_offre <= ?) and (ville_depart == ?) and (ville==?)",budget,destination[0],lieu):
            retours.append(row)
    for retour in retours:
        res_adv.append(retour)

    connection.close()
    if res_adv==[]: #Si pas de correspondance, recherche normale
        return [get_bd(budget,lieu,date_aller,date_retour),"Nous ne trouvons aucune offre qui corresponde parfaitement à votre demande"]
    else:
        return [res_adv,"Votre recherche a abouti"]

def verif_login_bd(pseudo, mdp, type):  #Vérifie la demande de connection au compte
    data=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    if type=='client':
        for row in connection.execute("select pseudo_client, mdp, email from Client where (pseudo_client = ?) and (mdp = ?)",pseudo,mdp):
            data.append(row)

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
        return data[0][0]

def regist_vendeur_bd(nom_vendeur, email, mdp): #Insert nouveau vendeur dans la bd
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("insert into Vendeur (nom_vendeur,email,mdp) values (?,?,?)", nom_vendeur,email,mdp)
    connection.close()

def regist_client_bd(nom_client, email, mdp):   #Insert nouveau client dans la bd
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("insert into Client (pseudo_client,mdp,email) values (?,?,?)", nom_client,mdp,email)
    connection.close()

def ajouter_offre_liste(nom_client, id_offre): #ajouter les requêtes
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.close()

def retirer_offre_liste(nom_client, id_offre): #ajouter les requêtes
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.close()

def recup_liste_client(nom_client): #ajouter les requêtes
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.close()

def new_offer_bd(destination, transport, depart, date,prix,lien, offreur):  #Insert nouvelle offre après vérification
    data=[]
    dest=[]
    prix=float(prix)
    offer=[destination,offreur,transport,depart,date,prix,lien]

    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()

    for row in connection.execute("select * from Offre where (nom_vendeur==?)",offreur):
        data.append(row)

    try :
        r = requests.get(offer[6])  #On vérifie l'accès au site
        if r.status_code != 200:
            connection.close()
            return "Erreur dans le lien"
    except:
        connection.close()
        return "Erreur dans le lien"

    for i in range (0,len(data)):   #On vérifie que l'offre n'existe pas déjà
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
    if dest==[]:    #Si c'est une nouvelle destination, on la crée dans les tables destination et meteo
        connection.execute("insert into Destination (ville, pays, environnement, urbanisme) values (?,NULL,NULL,NULL)",destination)
        connection.execute("insert into Meteo (ville, date_debut, date_fin,meteo) values (?,NULL,NULL,NULL)", destination)

    connection.close()
    return "Offre ajoutée"

def get_new_dest(): #Récupère les nouvelles destinations
    villes=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select d.ville from Destination as d where (d.pays is NULL)"):
        villes.append(row)

    connection.close()
    return villes

def get_new_vendeur():  #Récupère les nouveaux vendeurs
    vendeurs=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select nom_vendeur, email, mdp from Vendeur where (validation is NULL)"):
        vendeurs.append(row)

    connection.close()
    return vendeurs


def update_new_dest(ville,pays,environnement,urbanisme):    #Met à jour la destination
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("update Destination set pays=?, environnement=?, urbanisme=? where (ville=?)",pays,environnement,urbanisme,ville)
    connection.close()

def update_new_met(ville,date_debut,date_fin,meteo):    #Met à jour la météo
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("update Meteo set date_debut=?, date_fin=?, meteo=? where (ville=?)", date_debut,date_fin,meteo,ville)
    connection.close()

def accept_new_vend(nom_vendeur):   #Accept un vendeur
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("update Vendeur set validation=1 where (nom_vendeur=?)", nom_vendeur)
    connection.close()

def deny_new_vend(nom_vendeur): #Refuse un vendeur
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    connection.execute("delete from Vendeur where (nom_vendeur=?)", nom_vendeur)
    connection.close()

def vendeur_accepte(nom_vendeur):   #Méthode pour vérifier si un vendeur est accepté
    vendeurs=[]
    engine = create_engine('sqlite:///BASEWEB.db', echo=True)
    connection = engine.connect()
    for row in connection.execute("select nom_vendeur from Vendeur where (validation is NOT NULL) and (nom_vendeur=?)",nom_vendeur):
        vendeurs.append(row)
    connection.close()

    if len(vendeurs)==1:
        return 1
    else:
        return-1
