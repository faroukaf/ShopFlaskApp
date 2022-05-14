from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from market.dbmodels import User


class RegisterForm(FlaskForm):

    def validate_username(self, username2check):
        user = User.query.filter_by(username=username2check.data).first()

        if user:
            raise ValidationError("Already used user name!")

    def validate_email(self, email2check):
        user = User.query.filter_by(email=email2check.data).first()

        if user:
            raise ValidationError("Already used email address!")

    username = StringField(label='User Name', validators=[Length(min=3, max=30), DataRequired()])
    email = EmailField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=3), DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=3, max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=3), DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
