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
    return render_template('login.html', message=txt)

@app.route('/Odyssee/sign_up_offreur')
def offre_reg_page():
    return render_template('sign_up.html')

@app.route('/login',methods =['POST'])
def verif():
    if(request.method=='POST'):
        print(request.form['pseudo'],request.form['mdp']);
        nom_vendeur=prog.verif_login_bd(request.form['pseudo'],request.form['mdp']);
        if (nom_vendeur!=-1):
            return render_template('offre.html',nom_vendeur=nom_vendeur)
        else:
            return render_template('login.html',message="Problème d'authentification")

@app.route('/sign_up',methods =['POST'])
def register():
    if(request.method=='POST'):
        prog.regist_vendeur_bd(request.form['pseudo'],request.form['email'],request.form['mdp']);
        return render_template('offre.html',nom_vendeur=request.form['pseudo']);

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('page_accueil'))

if __name__=='__main__':
    app.run(debug=True)
