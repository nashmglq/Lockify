import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from models import db, User

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = "static/uploads"

@routes.route('/')
def landing():
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    return render_template('landing.html')

@routes.route('/contact')
def contactUs():
    if 'user_id' in session: 
        return redirect(url_for('routes.dashboard'))
    return render_template('contactUs.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session: 
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('routes.dashboard'))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('routes.login'))

    return render_template('login.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:  
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash("Username or email already exists", "error")
            return redirect(url_for('routes.register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('routes.login'))

    return render_template('register.html')

@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:  
        flash("You must log in first", "error")
        return redirect(url_for('routes.login'))
    return render_template('authenticated/dashboard.html')

@routes.route('/logout')
def logout():
    session.pop('user_id', None) 
    flash("You have been logged out.", "info")
    return redirect(url_for('routes.login'))

@routes.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.username = request.form["username"]
        user.email = request.form["email"]

        if "profile_pic" in request.files:
            file = request.files["profile_pic"]
            if file and file.filename != "":
                filename = file.filename
                file.save(f"static/uploads/{filename}")
                user.profile_pic = filename
            else:
                if not user.profile_pic:
                    user.profile_pic = "default.jpg"

        db.session.commit()
        return redirect(url_for("profile.profile"))

    return render_template("authenticated/profile.html", user=user)
