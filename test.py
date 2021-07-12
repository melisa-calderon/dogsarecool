from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/dogs") 
def dogs():
    return render_template('dogs.html', subtitle='Dog Page', text='This is the dog page')
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")