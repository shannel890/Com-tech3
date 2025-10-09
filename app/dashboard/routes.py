from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.group import Group
from app.models.message import Message
from app.models.membership import Membership
from app.models.user import User
from app.extension import db
from app.form import GroupForm

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def index():
    groups = Group.query.all()
    return render_template('dashboard/dashboard.html', groups=groups, user=current_user)

@dashboard.route('/contacts')
@login_required
def contacts():
    users = User.query.all()
    groups = Group.query.all()
    return render_template('dashboard/contacts.html', users=users, groups=groups, user=current_user)

@dashboard.route('/group/<int:group_id>')
@login_required
def view_group(group_id):
    group = Group.query.get_or_404(group_id)
    messages = Message.query.filter_by(group_id=group.id).order_by(Message.timestamp.asc()).all()
    return render_template('group_chat.html',group=group, messages=messages, user=current_user)

@dashboard.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()  # ✅ create form instance
    if request.method == 'POST':
        group_name = request.form.get('name')
        group_description = request.form.get('description')
        if group_name:
            new_group = Group(name=group_name, description=group_description, owner_id=current_user.id)
            db.session.add(new_group)
            db.session.commit()
            # Add the creator as a member of the group
            membership = Membership(user_id=current_user.id, group_id=new_group.id)
            db.session.add(membership)
            db.session.commit()
            flash('Group created successfully!', 'success')
            return redirect(url_for('dashboard.index'))
    return render_template('dashboard/create_group.html', form=form, user=current_user)

@dashboard.route('/call')
@login_required
def call():
    return render_template('dashboard/call.html', user=current_user)

@dashboard.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('dashboard/profile.html', user=user)
