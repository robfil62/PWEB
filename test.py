from flask import Flask
app = Flask(__name__)

@app.route('/')
def hey():
    return 'Coucou !'

if __name__ == '__main__':
    app.run(debug=True)
