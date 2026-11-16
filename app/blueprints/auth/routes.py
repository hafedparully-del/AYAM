from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from urllib.parse import urlparse
from app.extensions import db
from app.models import User
from . import bp
from .forms import LoginForm, RegistrationForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Rute main.index akan dibuat di Tahap 3

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email atau kata sandi tidak valid.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            # Redirect berdasarkan role
            if user.role == 'admin':
                next_page = url_for('auth.login')  # Sementara arahkan ke login, diganti ke admin.dashboard nanti
            else:
                next_page = url_for('auth.login')
        return redirect(next_page)

    return render_template('login.html', title='Masuk', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email sudah terdaftar. Silakan gunakan email lain.', 'error')
            return redirect(url_for('auth.register'))

        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan masuk.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Daftar', form=form)