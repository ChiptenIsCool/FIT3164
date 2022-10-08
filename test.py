from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
import csv
app.config['SECRET_KEY'] = '0158950871737624af8c666d6ec6d223' #obtain from secrets fuction in python
#html file must be inside templates folder

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'


db=SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

class Suburb(db.Model):
    Suburb = db.Column(db.String(30))
    postcode = db.Column(db.Integer)
    incidents = db.Column(db.Integer)
    population = db.Column(db.Integer)
    lat = db.Column(db.Numeric)
    long = db.Column(db.Numeric)

    def __repr__(self):
        return f"Suburb('{self.Suburb}', '{self.postcode}', '{self.incidents}')"


'''
db2 = SQLAlchemy(app)
class Suburb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suburb = db.Column(db.String(100))
    postcode = db.Column(db.Integer)
    number_incidents = db.Column(db.Integer)
    population = db.Column(db.Integer)
    lat = db.Column(db.Integer)
    long = db.Column(db.Integer)

import csv

with open("source_file.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for i in reader:
        new_entry = Suburb(
        suburb = i[0],
        postcode = i[1],
        number_incidents = i[2],
        population = i[3],
        lat = i[4],
        long = 1[5])
        db.session.add(new_entry)
        db.session.commit()
'''


#dummy data
post = [
    {
        'author': 'Cipta Pratama',
        'title': 'How to be an Introvert',
        'Content': 'First Content',
        'date_posted': 'April'
    },
    {
        'author': 'Gavin Toby',
        'title': 'How to be an Extrovert',
        'Content': 'Second Content',
        'date_posted': 'August'
    }
]

@app.route("/")
@app.route("/test")
def test():
    return render_template('test.html') 
@app.route("/home")
def home():
    return render_template('home.html', posts = post) #post itu variable yg diatas, posts itu variable yg buat dipake di file HTMLnya

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data=='password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. please check again','danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
