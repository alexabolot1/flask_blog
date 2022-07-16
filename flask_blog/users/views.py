from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import User, Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateUserForm, RequestResetForm, ResetPasswordForm)

from flask_blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись успешно создана!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_post'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('posts.all_post'))
        else:
            flash('Неверные данные для входа', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=
                                    form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.date_posted.desc()) \
            .paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' +
                                            current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, posts=posts,
                           user=user)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На почту отправлено письмо с '
              'инструкциями по сбросу пароля.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Сброс пароля', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_post'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Это недействительный или просроченный токен', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.\
            generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был обновлен! '
              'Теперь вы можете авторизоваться', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           title='Сброс пароля', form=form)
