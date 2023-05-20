"""Blogly application."""

from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from models import db, User

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def redirect_to_users():
    """Redirect to the list of users"""
    return redirect(url_for('list_users'))


@app.route('/users')
def list_users():
    """Show all users"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    """Create a new user"""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()

        return redirect('/users')  # Redirect to the list of users page

    return render_template('add_user.html')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show information about the given user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


@app.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit a user"""
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']

        db.session.commit()
        return redirect('/users')

    return render_template('edit_user.html', user=user)


@app.route('/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)