
from flask import render_template, flash, redirect, request, url_for, Blueprint, session
from flask_login import login_required, logout_user, login_user, current_user
from form import SignUpForm, LoginForm, BlogDataForm, UserForm, RequestResetForm, ResetPasswordForm
from model import db, UserData, BlogData
from flask_bcrypt import Bcrypt
from sqlalchemy import exc, select
from sqlalchemy.orm import Session, Query
from werkzeug.utils import secure_filename
import random, math
import uuid
import os

bcrypt = Bcrypt()
route = Blueprint('route', __name__,template_folder=os.path.abspath('templates'))

@route.route('/home_page')
@login_required
def home():
    blogs = db.session.execute(db.select(BlogData)).scalars()
    return render_template('index.html', blogs= blogs)


@route.route('/admin')
def admin():
    
    return render_template('admin.html')

@route.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():        
        form_email = form.email.data
        db_user = UserData.query.filter(UserData.email==form_email).first()
        print(db_user)
        if form_email == db_user.email:
            if bcrypt.check_password_hash(db_user.password, form.password.data):
                login_user(db_user, remember=True)  
                session.permanent = True
                return redirect(url_for('route.home', username=db_user.username))
            else:
                flash("wrong passowrd!",'danger')
        else:
            flash("Email not Found", 'error')
    else:
        print(form.errors)
    return render_template("login.html", form=form)

@route.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("route.home"))
    form = SignUpForm()
    if form.is_submitted():
        if form.password.data==form.repassword.data:
            print('passed from here')
            crypted_pass = bcrypt.generate_password_hash(form.password.data)
            new_user = UserData(username=form.username.data, email=form.email.data, password=crypted_pass)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('route.login'))
            except exc.IntegrityError:
                db.session.rollback()
        else:
            flash("Check Email or Password!!", 'error')
    return render_template("signup.html", form=form)

@route.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    # session.pop(current_user)
    logout_user()
    return redirect(url_for('route.login'))

@route.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # myblogs =  db.session.execute(db.select(BlogData).filter_by(user_data=current_user.id)).scalars()
    myblogs = BlogData.query.filter_by(writer_id=current_user.id).all()
    form = UserForm()
    id = current_user.id

    if form.is_submitted():

        profile_pic = request.files['profile_pic']
        pic_filename = secure_filename(profile_pic.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename

        user = UserData.query.get_or_404(id)
        saver = request.files['profile_pic']
        
        user.profile_pic = pic_name

        db.session.add(user)
        db.session.commit()
        upload_folder = os.environ.get('UPLOAD_FOLDER')
        abs_path = os.path.abspath(upload_folder)
        print(abs_path)
        saver.save(os.path.join(abs_path, pic_name))

    return render_template('account.html', data=current_user, form=form, myblogs=myblogs)

@route.route('/blog/<id>', methods=['GET'])
@login_required
def blog_page(id):
    blog = db.session.execute(db.select(BlogData).filter_by(id=id)).scalar_one()
    blogs = BlogData.query.all()
    return render_template('blog_page.html', blog=blog)

@route.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    form = BlogDataForm()
    session = db.session
    
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        # check if there is any file

        blog_thumbnail = request.files['blog_thumbnail']
        print(blog_thumbnail.name)
        pic_filename = secure_filename(blog_thumbnail.filename)
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        saver = request.files['blog_thumbnail']
        upload_folder = os.environ.get('UPLOAD_FOLDER')
        abs_path = os.path.abspath(upload_folder)

        # Save the blog Title, Content and Thumbnail to BlogData Table In DB
        blog = BlogData(title=title, content=content, user_data=current_user, blog_thumbnail=pic_name, category=category)
        db.session.add(blog)
        db.session.commit()
        saver.save(os.path.join(abs_path, pic_name))

        return redirect(url_for('route.home'))
    
    return render_template('create_blog.html', form=form)
    
@route.route('/delete_blog/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_blog(id):
    blog_post = BlogData.query.get_or_404(id)

    try:
        db.session.delete(blog_post)
        db.session.commit()

        flash('Blog Post Deleted Successfully!', 'success')

        return redirect(url_for('route.account'))
    except:
        flash("Whoops! there was a problem")
        return redirect(url_for('route.account'))


@route.route('/delete_account/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_account(id):
    pass


# @route.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('route.home'))
#     form = RequestResetForm()
#     return render_template('reset_request.html', title='Reset Password', form=form)

@route.route('/category/<string:category>')
def filter_by_category(category):
    if category=='All':
        return redirect(url_for('route.home'))
    else:
        # category = db.session.execute(db.select(BlogData).filter_by(category=category)).scalars()
        category = BlogData().query.filter_by(category=category).all()
        
        
        # return redirect(url_for('route.home', blogs= category))
    
    return render_template('index.html', blogs= category)

