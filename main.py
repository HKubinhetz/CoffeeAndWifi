from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)

# Random key (remember to hide this one if you're hosting your project somewhere!):
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


def time_validator(form, field):
    if 'AM' not in field.data and 'PM' not in field.data:
        raise ValidationError('Field must be in an hour format ending in AM or PM, i.e. "10AM".')


def link_validator(form, field):
    if 'http' not in field.data or 'maps' not in field.data:
        raise ValidationError('Field must be a google maps link.')


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])

    location = StringField('Location URL',
                           validators=[DataRequired(), link_validator])

    open_time = StringField('Opening Time',
                            validators=[DataRequired(), time_validator])

    closing_time = StringField('Closing Time',
                               validators=[DataRequired(),  time_validator])

    coffee = SelectField('Coffee Rating',
                         choices=[('1', '☕'),
                                  ('2', '☕☕'),
                                  ('3', '☕☕☕'),
                                  ('4', '☕☕☕☕'),
                                  ('5', '☕☕☕☕☕')])

    wifi = SelectField('WiFi Rating',
                       choices=[('0', '✘'),
                                ('1', '📡'),
                                ('2', '📡📡'),
                                ('3', '📡📡📡'),
                                ('4', '📡📡📡📡'),
                                ('5', '📡📡📡📡📡')])

    outlets = SelectField('Outlet Rating',
                          choices=[('0', '✘'),
                                   ('1', '🔌'),
                                   ('2', '🔌🔌'),
                                   ('3', '🔌🔌🔌'),
                                   ('4', '🔌🔌🔌🔌'),
                                   ('5', '🔌🔌🔌🔌🔌')])

    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
