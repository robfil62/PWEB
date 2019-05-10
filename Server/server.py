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
        data=prog.get_bd(request.args.get('budget','0'));
        if (data==[]):
            return render_template('no_results.html')
        else:
            return render_template('results.html',data=data)

@app.route('/Odyssee/advanced_search')
def advanced_search():
    return render_template('advanced_search.html')

@app.route('/Odyssee/login_offreur')
def offre_log_page():
    txt = 'Bonjour !'
    return render_template('index.html', message=txt)

@app.route('/Odyssee/register_offreur')
def offre_reg_page():
    txt = 'Bonjour ! Entrez votre nom, votre addresse mail et votre mdp pour vous inscrire'
    return render_template('register_offreur.html', message=txt)

@app.route('/vendeur',methods =['POST'])
def verif():
    if(request.method=='POST'):
        nom_vendeur=prog.verif_login_bd(request.form['email'],request.form['mdp']);
        if (nom_vendeur!=-1):
            return render_template('page_offreur.html',nom_vendeur=nom_vendeur)
        else:
            return render_template('index.html',message="Problème d'authentification")

@app.route('/new_vendeur',methods =['POST'])
def register():
    if(request.method=='POST'):
        prog.regist_vendeur_bd(request.form['nom_vendeur'],request.form['email'],request.form['mdp']);
        return render_template('page_offreur.html',nom_vendeur=request.form['nom_vendeur']);

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('page_accueil'))


@app.route('/init_bd_vendeur')
def init():
    engine = create_engine('sqlite:///BASE.db', echo=True)
    connection = engine.connect()

    connction.close()
if __name__=='__main__':
    app.run(debug=True)
