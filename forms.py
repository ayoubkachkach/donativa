from wtforms import Form, StringField, TextAreaField, PasswordField, validators


class UserSignupForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=15)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=15)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    address = StringField('Address', [validators.Length(min=3, max=50)])
    city = StringField('City', [validators.Length(min=3, max=20)])
    phone_number = StringField('Phone Number',[
            validators.Regexp('\d{6,}', message="Phone number can only contain 6 or more digits."),
        ])
    bio = StringField('Biography', [validators.Length(min=3, max=120)])



class OrganizationSignupForm(Form):
    name = StringField('Organization Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    address = StringField('Address', [validators.Length(min=3, max=50)])
    phone_number = StringField('Phone Number',[
            validators.Regexp('\d{6,}', message="Phone number can only contain 6 or more digits."),
        ])
