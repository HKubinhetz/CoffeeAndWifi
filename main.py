# --------------------------------- IMPORTS -----------------------------------
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired
import csv

# -------------------------- APP CREATION AND CONFIG --------------------------
app = Flask(__name__)
# Random key (remember to hide this one if you're hosting your project somewhere!):
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# -------------------------------- FUNCTIONS ----------------------------------
# ---------------------- PART 1 - CSV-RELATED FUNCTIONS  ----------------------

def get_cafes_from_csv():
    # This function reads the cafe database from a CSV file.
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        return list_of_rows


def write_cafe_to_csv(info_to_write):
    # This function writes a new cafe to the cafe database.
    with open('cafe-data.csv', 'a', newline='', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(info_to_write)
        print("Writing complete!")


def cafe_answers_to_list(form):
    # This function simply converts the cafe form answers to a list.
    cafe_info = [form.cafe.data, form.location.data,
                 form.open_time.data, form.closing_time.data,
                 form.coffee.data, form.wifi.data, form.outlets.data]
    return cafe_info


# ------------------------ PART 2 - CUSTOM VALIDATORS  ------------------------
def time_validator(form, field):
    # This function validates time structure in the form.
    if 'AM' not in field.data and 'PM' not in field.data:
        raise ValidationError('Field must be in an hour format ending in AM or PM, i.e. "10AM".')


def link_validator(form, field):
    # This function validates website structure in the form.
    if 'http' not in field.data or 'maps' not in field.data:
        raise ValidationError('Field must be a google maps link.')


# ---------------------------------- FORM -------------------------------------
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])

    location = StringField('Location URL',
                           validators=[DataRequired(), link_validator])

    open_time = StringField('Opening Time',
                            validators=[DataRequired(), time_validator])

    closing_time = StringField('Closing Time',
                               validators=[DataRequired(), time_validator])

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


# ------------------------------ FLASK ROUTES ---------------------------------
# Default home route
@app.route("/")
def home():
    return render_template("index.html")


# Route for adding a new cafe via a Flask Form
@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    # If form is submitted, it runs two functions to write in a new cafe in the CSV file.
    if form.validate_on_submit():
        form_answers = cafe_answers_to_list(form)
        write_cafe_to_csv(form_answers)
        return render_template('success.html')
    # If loading the page, it goes straight to the form page:
    return render_template('add.html', form=form)


# Route for a successful form submission
@app.route("/success")
def success():
    return render_template("success.html")


# Route for listing all the registered cafes
@app.route('/cafes')
def cafes():
    cafes_data = get_cafes_from_csv()
    return render_template('cafes.html', cafes=cafes_data)


# ------------------------------- EXECUTION -----------------------------------
if __name__ == '__main__':
    app.run(debug=True)
