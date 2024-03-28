from flask import Flask, render_template, request, flash,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import imaplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/kapselite'
db = SQLAlchemy(app)
app.app_context() .push()

class clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"clients('{self.firstname}', '{self.surname}', '{self.email}', '{self.company}', '{self.country}', '{self.zip}', '{self.status}')"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Invalid username or password.')
            return redirect(url_for('signin'))

        # Check if password is correct
        if not user.password == password:
            flash('Invalid username or password.')
            return redirect(url_for('signin'))

        flash('Signin successful. Welcome, {}!'.format(user.username))
        return redirect(url_for('home'))

    return render_template('signin.html')
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('signup'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists.')
            return redirect(url_for('signup'))

        # Check if password matches confirmation
        if password != confirm_password:
            flash('Password and confirmation do not match.')
            return redirect(url_for('signup'))

        # Create new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful. Please log in.')
        return redirect(url_for('signin'))
   return render_template('signup.html')



@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        firstname = request.form['firstname']
        surname = request.form['surname']
        email = request.form['email']
        company = request.form['company']
        country = request.form['country']
        zip = request.form['zip']
        status = request.form['status']

        registration = clients(firstname=firstname, surname=surname, email=email, company=company,
                                    country=country, zip=zip, status=status)
        db.session.add(registration)
        db.session.commit()

    
        
        return render_template('form.html')
    return render_template('form.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/table')
def table():
    registrations = clients.query.all()
    return render_template('table.html', registrations=registrations)

@app.route('/widget')
def widget():
    return render_template('widget.html')

@app.route('/element')
def element():
    return render_template('element.html')

@app.route('/button')
def button():
    return render_template('button.html')

@app.route('/typography')
def typography():
    return render_template('typography.html')

@app.route('/404')
def notfound():
    return render_template('404.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')
@app.route('/emails')
def display_emails():
    # Email credentials and server details
    email_address = 'taniamanheru@gmail.com'
    password = '1353kyle'
    imap_server = 'pop.gmail.com'


    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, password)
    mail.select('inbox')

    # Retrieve email messages
    _, message_ids = mail.search(None, 'ALL')
    message_ids = message_ids[0].split()

    messages = []
    for message_id in message_ids:
        _, msg_data = mail.fetch(message_id, '(RFC822)')
        raw_email = msg_data[0][1]
        # Process the raw email data as needed
        messages.append(raw_email)

    # Close the connection to the server
    mail.logout()

    return render_template('widget.html', messages=messages)



if __name__ == '__main__':
    app.run(debug=True)