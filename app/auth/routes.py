from app import db
from app.auth import bp
from .forms import RegisterForm, LoginForm
from flask import render_template, redirect, url_for, flash, request
from app.models import User, Role
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', form=form)


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            phone=form.username.data,
            role = Role.query.get(1)
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successfull')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
