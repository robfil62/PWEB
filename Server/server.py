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

@app.route('/Odyssee/search?<budget>',methods=['GET'])
def search(budget):
    if request.method == 'GET':
        data=prog.get_bd(budget);
        if (data==[]):
            return render_template('no_results.html')
        else:
            return render_template('results.html',data=data)

@app.route('/Odyssee/advanced_search')
def advanced_search():
    return render_template('advanced_search.html')

@app.route('/Odyssee/index')
def index():
    if 'username' in session:
       username = session['username']

    app.url_for('page_accueil')


@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      session['username'] = request.form['username']
      return redirect(url_for('index'))
   return '''
   <form action = "" method = "post">
      <p><input type = text name = username/></p>
      <p<<input type = submit value = Login/></p>
   </form>
   '''


@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)
