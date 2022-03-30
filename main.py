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
                         choices=[('☕', '☕'),
                                  ('☕☕', '☕☕'),
                                  ('☕☕☕', '☕☕☕'),
                                  ('☕☕☕☕', '☕☕☕☕'),
                                  ('☕☕☕☕☕', '☕☕☕☕☕')])

    wifi = SelectField('WiFi Rating',
                       choices=[('✘', '✘'),
                                ('📡', '📡'),
                                ('📡📡', '📡📡'),
                                ('📡📡📡', '📡📡📡'),
                                ('📡📡📡📡', '📡📡📡📡'),
                                ('📡📡📡📡📡', '📡📡📡📡📡')])

    outlets = SelectField('Outlet Rating',
                          choices=[('✘', '✘'),
                                   ('🔌', '🔌'),
                                   ('🔌🔌', '🔌🔌'),
                                   ('🔌🔌🔌', '🔌🔌🔌'),
                                   ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
                                   ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')])

    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_info = []
        concatenated_string = ""

        cafe_info.append(form.cafe.data)
        cafe_info.append(form.location.data)
        cafe_info.append(form.open_time.data)
        cafe_info.append(form.closing_time.data)
        cafe_info.append(form.coffee.data)
        cafe_info.append(form.wifi.data)
        cafe_info.append(form.outlets.data)
        for info in cafe_info:
            concatenated_string += info + ","
        print(concatenated_string[:-1])

        with open('cafe-data.csv', 'a', newline='', encoding='utf8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(cafe_info)
            print("Writing complete!")
            return render_template('success.html')
    return render_template('add.html', form=form)


@app.route("/success")
def success():
    return render_template("success.html")


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
