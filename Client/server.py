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

@app.route('/Odyssee/offer')
def offrir():
    try:
        if(session['logged'] == True):
            return render_template('offre.html',nom_vendeur=session['username'],message="Bonjour "+session['username']);
        else:
            return redirect(url_for('page_accueil'))
    except:
        return redirect(url_for('offre_log_page'))

@app.route('/login',methods =['POST'])
def verif():
    if(request.method=='POST'):
        nom_vendeur=prog.verif_login_bd(request.form['pseudo'],request.form['mdp']);
        if (nom_vendeur!=-1):
            session['username'] = nom_vendeur
            session['logged'] = True
            return redirect(url_for('offrir'))
        else:
            return render_template('login.html',message="Problème d'authentification")

@app.route('/sign_up',methods =['POST'])
def register():
    if(request.method=='POST'):
        prog.regist_vendeur_bd(request.form['pseudo'],request.form['email'],request.form['mdp']);
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
