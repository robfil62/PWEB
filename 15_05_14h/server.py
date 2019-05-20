from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
import prog

app = Flask(__name__)
data=[]
app.secret_key="auhasard"

@app.route('/Odyssee')  #Page d'accueil
def page_accueil():
    try :
        return render_template('page_accueil.html', logged=session['logged'], message="Bonjour "+ session['username'])
    except:
        return render_template('page_accueil.html', logged=False)

@app.route('/Odyssee/search',methods=['GET'])   #Affichage des résultats
def search():
    if request.method == 'GET':
        data=prog.get_bd(request.args.get('budget'),
        request.args.get('lieu'),
        request.args.get('date_aller'),
        request.args.get('date_retour'));
        try :
            return render_template('results.html',liste=data, logged=session['logged'])
        except:
            return render_template('results.html',liste=data, logged=False)

@app.route('/Odyssee/advanced_search_page') #Affichage de la page recherches avancées
def advanced_search_page():
    return render_template('advanced_search.html')

@app.route('/Odyssee/adv_search',methods=['GET'])   #Affichage des résultats avancés
def adv_search():

    if request.method == 'GET':
        data=prog.get_adv_bd(request.args.get('budget'),
        request.args.get("lieu"),
        request.args.get('date_aller'),
        request.args.get('date_retour'),
        request.args.get('meteo'),
        request.args.get('environnement'),
        request.args.get('urbanisme'));

        try :
            return render_template('results.html',liste=data[0], message=data[1], logged=session['logged'])

        except :
            return render_template('results.html',liste=data[0], message=data[1], logged=False)

@app.route('/Odyssee/login_page')   #Affichage de la page login
def log_page():
    return render_template('login.html', message='Bonjour !')

@app.route('/login',methods =['POST'])  #Gère les login clients, vendeurs et admin
def verif():
    if(request.method=='POST'):
        if (request.form['type'] == 'vendeur'):

            nom_vendeur=prog.verif_login_bd(request.form['pseudo'],request.form['mdp'],'vendeur');
            if (nom_vendeur!=-1):
                session['username'] = nom_vendeur
                session['logged'] = True
                session['type'] = True
                return redirect(url_for('offrir'))
            else:
                return render_template('login.html',message="Problème d'authentification")

        if (request.form['type'] =='client'):
            nom_client=prog.verif_login_bd(request.form['pseudo'],request.form['mdp'],'client');
            if (nom_client!=-1):
                session['username'] = nom_client
                session['logged'] = True
                session['type'] = False
                return render_template('page_accueil.html',logged=session['logged'], message="Bonjour "+nom_client)

            else:
                return render_template('login.html',message="Problème d'authentification")

        if(request.form['type']=='admin'):

            nom_admin=prog.verif_login_bd(request.form['pseudo'],request.form['mdp'],'admin')
            if (nom_admin=="ADMIN"):
                session['username'] = nom_admin
                session['logged'] = True
                session['type'] = True
                return redirect(url_for('gerer'))
            else:
                return render_template('login.html',message="Problème d'authentification")



@app.route('/Odyssee/sign_up_page') #Affichage de la page sign_up
def offre_reg_page():
    return render_template('sign_up.html')

@app.route('/sign_up',methods =['POST'])    #Gère les sign_up
def register():
    if(request.method=='POST'):
        if(request.form['type']=="vendeur"):
            prog.regist_vendeur_bd(request.form['pseudo'],request.form['email'],request.form['mdp']);
            session['username'] = request.form['pseudo']
            session['logged'] = True
            session['type'] = True
            return render_template('page_accueil.html',message="Requête d'adhésion soumise")


        if(request.form['type']=="client"):
            prog.regist_client_bd(request.form['pseudo'],request.form['email'],request.form['mdp']);
            session['username'] = request.form['pseudo']
            session['logged'] = True
            session['type'] = False
            return render_template('page_accueil.html',logged=session['logged'], message="Bonjour "+session['username'])

    else:
        return render_template('sign_up.html')

@app.route('/Odyssee/offer')    #Affichage page vendeur pour nouvelles offres
def offrir():
    try:
        if(session['logged'] == True and session['type']==True and prog.vendeur_accepte(session['username'])==1):
            return render_template('offre.html',nom_vendeur=session['username'],message="Bonjour "+session['username']);
        else:
            return redirect(url_for('page_accueil'))
    except:
        return redirect(url_for('log_page'))

@app.route('/new_offer',methods=['POST'])   #Gère les nouvelles offres
def send_offer():
    if(request.method=='POST'):
        prog.new_offer_bd(request.form['destination'],
        request.form['transport'],
        request.form['depart'],
        request.form['date'],
        request.form['prix'],
        request.form['lien'],
        session['username']);

    return render_template('offre.html',nom_vendeur=session['username'],message='Offre envoyée');

@app.route('/Odyssee/admin')    #Affichage page admin
def gerer():
    try:
        if(session['logged'] == True and session['username']== 'ADMIN'):
            liste_new_dest=prog.get_new_dest()
            liste_new_vendeurs=prog.get_new_vendeur()
            return render_template('admin.html',liste1=liste_new_dest, liste2 = liste_new_vendeurs)
        else:
            return redirect(url_for('page_accueil'))
    except:
        return redirect(url_for('log_page'))

@app.route('/new_dest', methods=['POST'])
def send():
    try:

        if(session['logged'] == True and session['username']== 'ADMIN' and request.method=='POST'):
            prog.update_new_dest(request.form['ville'],request.form['pays'],
            request.form['environnement'],request.form['urbanisme']);

            prog.update_new_met(request.form['ville'], request.form['date_debut'],
            request.form['date_fin'], request.form['meteo']);
            return redirect(url_for('gerer'))

    except:
        return redirect(url_for('gerer'))

@app.route('/new_vend_accept', methods=['POST'])
def accept():
    try:
        if(session['logged'] == True and session['username']== 'ADMIN' and request.method=='POST'):
            prog.accept_new_vend(request.form['nom_vendeur']);
            return redirect(url_for('gerer'))
    except:
        return redirect(url_for('gerer'))

@app.route('/new_vend_deny', methods=['POST'])
def deny():
    try:
        if(session['logged'] == True and session['username']== 'ADMIN' and request.method=='POST'):
            prog.deny_new_vend(request.form['nom_vendeur']);
            return redirect(url_for('gerer'))
    except:
        return redirect(url_for('gerer'))

@app.route('/Odyssee/client')    #Affichage page client
def enregistre():
    try:
        if(session['logged'] == True or session['username']== 'Admin'):
            return render_template('client.html')
        else:
            return redirect(url_for('page_accueil'))
    except:
        return redirect(url_for('log_page'))

@app.route('/logout')   #Logout session
def logout():
   session.clear()
   return redirect(url_for('page_accueil'))

if __name__=='__main__':
    app.run(debug=True)
