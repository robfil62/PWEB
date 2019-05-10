from flask import *
from sqlalchemy import *
from sqlalchemy.sql import *
import prog

app = Flask(__name__)
data=[]
app.secret_key = "auhasard"

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

@app.route('/Odyssee/log_offreur')
def offre_log_page():
    txt = 'Bonjour !'
    return render_template('index.html', message=txt)

@app.route('/Odyssee/page_offreur')
def offre_page():
    return render_template('page_offreur.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    session['name'] =escape(request.form['name'])
    return redirect(url_for('offre_page'))

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('page_accueil'))

if __name__=='__main__':
    app.run(debug=True)
