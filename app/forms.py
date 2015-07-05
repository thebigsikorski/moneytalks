from flask.ext.wtf import Form
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class Districts(Form):
    zipcode = StringField('zipcode', validators=[DataRequired()])

class Issues(Form):
	keywords = StringField('keywords', validators=[DataRequired()])

class Vote(Form):
	myVotes = HiddenField('myVotes')

class Matches(Form):
	repMatches = HiddenField('repMatches');