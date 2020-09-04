from app.admin import bp
from .forms import AddUserForm, LoginForm, DiscountForm
from app import db
from flask import render_template, redirect, url_for, flash, request
from app.models import User, Discount
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.role == 'Admin':
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is not None:
            if not user.role.role == 'Admin':
                flash('You\'re not an admin. Login here')
                return redirect(url_for('auth.login'))
            if not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('admin.login'))
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin.dashboard')
            return redirect(next_page)
    return render_template('admin/login.html', form=form)



@bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            phone=form.username.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successfull')
        return redirect(url_for('admin.add_user'))
    return render_template('admin/add_user.html', form=form)

@bp.route('/discount', methods=['GET', 'POST'])
def discount():
    form = DiscountForm()
    if form.validate_on_submit():
        discount = Discount(
            code = form.code.data,
            code_type = form.code_type.data,
            expiry_date = form.expiry_date.data,
            rate = form.amount_percentage.data
        )
        try:
            db.session.add(discount)
            db.session.commit()
        except:
            db.session.rollback()
        flash('Discount Registered')
        return redirect(url_for('admin.discount'))
    return render_template('admin/discount.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')