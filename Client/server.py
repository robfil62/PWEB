from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
import prog

app = Flask(__name__)
data=[]
app.secret_key="auhasard"

@app.route('/Odyssee')
def page_accueil():
    try :
        return render_template('page_accueil.html', logged=session['logged'])
    except:
        return render_template('page_accueil.html', logged=False)

@app.route('/')
def defaut():
    return redirect(url_for('page_accueil'))

@app.route('/Odyssee/search',methods=['GET'])
def search():
    if request.method == 'GET':
        data=prog.get_bd(request.args.get('budget'),
        request.args.get('lieu'),
        request.args.get('date_aller'),
        request.args.get('date_retour'));

        try:
            return render_template('results.html',liste=data, logged=session['logged'])
        except:
            return render_template('results.html',liste=data, logged=False)

@app.route('/Odyssee/ajouter_liste', methods=['POST'])
def ajouter_liste():
    if request.method == 'POST':
        prog.ajouter_offre_liste(session['username'],
        request.form['id_offre']);

        try:
            return render_template('results.html',liste=data, logged=session['logged'])
        except:
            return render_template('results.html',liste=data, logged=False)

@app.route('/Odyssee/retirer_liste', methods=['POST'])
def retirer_liste():
    if request.method == 'POST':
        prog.retirer_offre_liste(session['username'],
        request.form['id_offre']);
        return redirect(url_for('esp_client_page'));

@app.route('/Odyssee/adv_search',methods=['GET'])
def adv_search():
    if request.method == 'GET':
        data=prog.get_adv_bd(request.args.get('budget'),
        request.args.get("lieu"),
        request.args.get('date_aller'),
        request.args.get('date_retour'),
        request.args.get('meteo'),
        request.args.get('environnement'),
        request.args.get('urbanisme'));
        try:
            return render_template('results.html', liste=data, logged=session['logged'])
        except:
            return render_template('results.html', liste=data, logged=False)

@app.route('/Odyssee/advanced_search')
def advanced_search():
    return render_template('advanced_search.html')

@app.route('/Odyssee/login_offreur')
def offre_log_page():
    return render_template('login.html', message='Bonjour !')

@app.route('/Odyssee/login_admin')
def admin_log_page():
    return render_template('login_admin.html', message='Bonjour !')


@app.route('/Odyssee/sign_up_offreur')
def offre_reg_page():
    return render_template('sign_up.html')

@app.route('/Odyssee/client')
def esp_client_page():
    try:
        if(session['type'] == False):
            data=prog.recup_liste_client(session['username']);
            return render_template('page_client.html', liste=data);
        else:
            return render_template('login.html', message="Page réservée aux clients")
    except:
        return redirect(url_for('offre_log_page'))

@app.route('/Odyssee/offer')
def offrir():
    try:
        if(session['type'] == True):
            return render_template('offre.html',nom_vendeur=session['username'],message="Bonjour "+session['username']);
        else:
            return render_template('login.html', message="Page réservée aux vendeurs")
    except:
        return redirect(url_for('offre_log_page'))

@app.route('/login',methods =['POST'])
def verif():
    if(request.method=='POST'):
        if (request.form['type'] == 'vendeur'):
            nom_vendeur=prog.verif_login_bd(request.form['pseudo'],request.form['mdp']);
            if (nom_vendeur!=-1):
                session['username'] = nom_vendeur
                session['logged'] = True
                session['type'] = True
                return redirect(url_for('offrir'))
            else:
                return render_template('login.html',message="Problème d'authentification")
        else:
            session['username'] = request.form['pseudo']
            session['logged'] = True
            session['type'] = False
            return redirect(url_for('esp_client_page'))

@app.route('/log_adm',methods =['POST'])
def verif_adm():
    if(request.method=='POST'):
        nom=prog.verif_login_bd(request.form['pseudo'],request.form['mdp']);
        if (nom!=-1):
            session['username'] = nom
            session['logged'] = True
            return redirect(url_for('gerer'))
        else:
            return render_template('login.html',message="Problème d'authentification")

@app.route('/Odyssee/admin')
def gerer():
    try:
        if(session['logged'] == True):
            return render_template('admin.html')
        else:
            return redirect(url_for('page_accueil'))
    except:
        return redirect(url_for('admin_log_page'))


@app.route('/sign_up',methods =['POST'])
def register():
    if(request.method=='POST'):
        if(request.form['type'] == 'vendeur'):
            prog.regist_vendeur_bd(request.form['pseudo'],request.form['email'],request.form['mdp']);
            session['type'] = True #True pour vendeur, False pour client
        if(request.form['type'] == 'client'):
            session['type'] = False
        session['username'] = request.form['pseudo']
        session['logged'] = True
        return redirect(url_for('offrir'))
    else:
        return render_template('sign_up.html')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('page_accueil'))

@app.route('/new_offer',methods=['POST'])
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



if __name__=='__main__':
    app.run(debug=True)
