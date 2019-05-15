from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
import prog

app = Flask(__name__)
data=[]
app.secret_key="auhasard"

@app.route('/Odyssee')
def page_accueil():
    return render_template('page_accueil.html')

@app.route('/Odyssee/search',methods=['GET'])
def search():
    if request.method == 'GET':
        data=prog.get_bd(request.args.get('budget','0'),
        request.args.get('lieu',''),
        request.args.get('date_aller',''),
        request.args.get('date_retour',''));
        ville = [];
        compagnie = [];
        moyen = [];
        depart = [];
        date = [];
        prix=[];
        lien=[];
        for elem in data:
            ville.append(elem[1]);
            compagnie.append(elem[2]);
            moyen.append(elem[3]);
            depart.append(elem[4]);
            date.append(elem[5]);
            prix.append(elem[6]);
            lien.append(elem[7]);
        return render_template('results.html',ville=ville, compagnie=compagnie, moyen=moyen, depart=depart, calendar=date, lien=lien, prix=prix)

@app.route('/Odyssee/advanced_search')
def advanced_search():
    return render_template('advanced_search.html')

@app.route('/Odyssee/login_offreur')
def offre_log_page():
    return render_template('login.html', message='Bonjour !')

@app.route('/Odyssee/sign_up_offreur')
def offre_reg_page():
    return render_template('sign_up.html')

@app.route('/login',methods =['POST'])
def verif():
    if(request.method=='POST'):
        nom_vendeur=prog.verif_login_bd(request.form['pseudo'],request.form['mdp']);
        if (nom_vendeur!=-1):
            return render_template('offre.html',nom_vendeur=nom_vendeur,message="Bonjour "+nom_vendeur)
        else:
            return render_template('login.html',message="Problème d'authentification")

@app.route('/sign_up',methods =['POST'])
def register():
    if(request.method=='POST'):
        prog.regist_vendeur_bd(request.form['pseudo'],request.form['email'],request.form['mdp']);
        return render_template('offre.html',nom_vendeur=request.form['pseudo'],message="Bonjour");

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
        request.form['offreur']);

    return render_template('offre.html',nom_vendeur=request.form['offreur'],message='Offre envoyée');

if __name__=='__main__':
    app.run(debug=True)
