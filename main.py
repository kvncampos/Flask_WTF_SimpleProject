from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, validators
from flask_bootstrap import Bootstrap5

from db.creds import credentials

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


class MyForm(FlaskForm):
    email = EmailField('Email', [validators.DataRequired(message='Field is empty'),
                                 validators.Length(message='Email must have more than 8 characters', min=8),
                                 validators.Email(message='Invalid email address', granular_message=True)
                                 ])
    passwd = PasswordField('Password', [validators.DataRequired(message='Field is empty'),
                                          validators.Length(message='Password must have at least 8 characters', min=8),
                                          ])
    submit = SubmitField('Log In', [validators.DataRequired('Submit credentials')])


app = Flask(__name__)
app.secret_key = "testingsupersecretapp9000"

bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = MyForm()
    email = form.email.data
    passwd = form.passwd.data
    if form.validate_on_submit():
        if email in credentials and credentials[email] == passwd:
            return redirect('/success')
        else:
            return redirect('/denied')
    return render_template('login.html', form=form)


@app.route("/success")
def success():
    return render_template('success.html')


@app.route("/denied")
def denied():
    return render_template('denied.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
