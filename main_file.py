from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from audio import printWAV
import time, random, threading
from turbo_flask import Turbo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ec7f20aec87d783c5f9aa84f11d7c7a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

interval= 9
FILE_NAME = "The_Science_of_DOGS.wav"
turbo = Turbo(app)

bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
  
    
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Welcome to dogsarecool',
                           text='Here you will learn about what makes dogs so cool')

  
@app.route("/dogs") 
def dogs():
    return render_template('dogs.html', subtitle='Dog Page',
                           text='This is the dog page, you\'ll get a chance to look at dogs')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm() 
    if form.validate_on_submit(): # checks if entries are valid
        pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data,
                password=pw)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e: 
            if 'user.username' in str(e):
                flash(f'Username taken, try again.', 'error')
            if 'user.email' in str(e):
                flash(f'Email already used, try another email.', 'error')
        else:        
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/captions")
def captions():
    TITLE = "The Science of DOGS"
    return render_template('captions.html', songName=TITLE, file=FILE_NAME)


@app.before_first_request
def before_first_request():
    #resetting time stamp file to 0
    file = open("pos.txt","w") 
    file.write(str(0))
    file.close()

    #starting thread that will time updates
    threading.Thread(target=update_captions, daemon=True).start()


@app.context_processor
def inject_load():
    # getting previous time stamp
    file = open("pos.txt","r")
    pos = int(file.read())
    file.close()

    # writing next time stamp
    file = open("pos.txt","w")
    file.write(str(pos+interval))
    file.close()

    #returning captions
    return {'caption':printWAV(FILE_NAME, pos=pos, clip=interval)}


def update_captions():
    with app.app_context():
        while True:
            # timing thread waiting for the interval
            time.sleep(interval)

            # forcefully updating captionsPane with caption
            turbo.push(turbo.replace(render_template('captionsPane.html'), 'load'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")