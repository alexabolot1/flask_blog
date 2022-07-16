from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from flask_login import current_user
from flask_blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired(),
                                                            Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password1 = PasswordField('Пароль:', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите пароль:', validators=[DataRequired(),
                                                                 EqualTo('password1')])
    submit = SubmitField('Зарегистрироваться')

    # @staticmethod
    # def validate_username(username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('Это имя уже занято.')
    #
    # @staticmethod
    # def validate_email(email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('Этот email уже занят.')


class LoginForm(FlaskForm):
    email = StringField('Email:',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateUserForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Обновить фото профиля',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    @staticmethod
    def validate_username(username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя уже занято.')

    @staticmethod
    def validate_email(email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже занят')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Изменить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email-адресом '
                                  'отсутствует. '
                                  'Вы можете зарегистрировать его')


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField('Пароль:', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите пароль:',
                              validators=[DataRequired(),
                                          EqualTo('password1')])
    submit = SubmitField('Изменить пароль')

