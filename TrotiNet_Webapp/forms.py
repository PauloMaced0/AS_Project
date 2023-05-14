from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets import PasswordInput


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(min=-1, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=8, max=-1, message='Password must have at least 8 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired()])
    submit = SubmitField('Sign in')

    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self):
            return False
        if self.password.data != self.confirm_password.data:
            self.confirm_password.errors.append("Passwords must match")
            return False
        return True


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me ')
    submit = SubmitField('Login')


class UpdatePersonalForm(FlaskForm):
    firstname = StringField('First Name ', validators=[
                            DataRequired(), Length(min=2, max=50)])
    lastname = StringField('Last Name', validators=[
                           DataRequired(), Length(min=2, max=50)])
    birthdate = DateField('Birth Date', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[
                              DataRequired(), Length(min=9, max=9)])
    submit_personal_changes = SubmitField('Save changes')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(min=-1, max=120)])
    submit_account_changes = SubmitField('Save changes')


class UpdatePasswordForm(FlaskForm):
    currentpassword = PasswordField(
        'Current password', validators=[DataRequired()])
    newpassword = PasswordField('New password', validators=[DataRequired(), Length(
        min=8, max=-1, message='Password must have at least 8 characters')], widget=PasswordInput(hide_value=False))
    confirm_new_password = PasswordField(
        'Confirm new password', validators=[DataRequired()])
    submit_password_change = SubmitField('Change password')

    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self):
            return False
        if self.newpassword.data != self.confirm_new_password.data:
            self.confirm_new_password.errors.append("Passwords must match")
            return False
        return True


class UpdateProfilePic(FlaskForm):
    picture = FileField('Upload an image', validators=[
                        DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit_profilePic = SubmitField('Update')
