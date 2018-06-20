from flask import Flask, request, render_template, flash, redirect, url_for, session
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired
from DineCision import yelprequest
from flask_wtf import FlaskForm
import random


API_KEY= "9aFYynAfext2uPCBlmYUdjsE_yKyue5f010epOxkBJ-qQnxSu1hTAmFZlLk2oJEorEbQopfTe5y4r08p70YaXd7zRpeUw9E6dKEEb7uMSN_U1i_921-UAqsj48UhW3Yx"

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'New York City, NY'
SEARCH_LIMIT = 5

app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class NameForm(Form):
    location = TextField('location:', validators=[validators.required()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    location = None
    if request.method == 'POST' and 'location' in request.form:
        location = request.form['location']
        return redirect(url_for('confirm', location=request.form.get('location')))
    #     # if form.validate():
    #     #     flash('Your entered: ' + location)
    #     # else:
    #     #     flash('Location is a required field')
        # session['location'] = form.location.data
        # return redirect('/result')
    return render_template('index.html')

@app.route('/confirm/<location>')
def confirm(location):
    random_business = yelp(location)
    return render_template('confirm.html', random_business=random_business['name'])


def yelp(location_input):

    url_params = {
        'location': location_input.replace(' ', '+'),
        'radius': 500,
        'is_closed': "false",
        'rating': 4,
        'limit': SEARCH_LIMIT,
        'categories': "restaurants, All",
        'price': 2
    }

    recommendation = []
    result = yelprequest(API_HOST, SEARCH_PATH, API_KEY, url_params)
    business_list = result["businesses"]
    random_business = random.choice(business_list)
    return random_business


if __name__ == "__main__":
    app.debug = True
    app.run()
