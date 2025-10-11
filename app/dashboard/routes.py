from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.group import Group
from app.models.message import Message
from app.models.membership import Membership
from app.models.user import User
from app.extension import db
from app.form import GroupForm, MessageForm, AddMemberForm

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

@dashboard.route('/group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def view_group(group_id):
    group = Group.query.get_or_404(group_id)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(content=form.content.data, group_id=group_id, user_id=current_user.id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('dashboard.view_group', group_id=group_id))
    messages = Message.query.filter_by(group_id=group.id).order_by(Message.timestamp.asc()).all()
    return render_template('group_chat.html', group=group, messages=messages, form=form, user=current_user)

@dashboard.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        try:
            new_group = Group(
                name=form.name.data,
                description=form.description.data,
                owner_id=current_user.id
            )
            db.session.add(new_group)
            db.session.commit()
            # Add the creator as a member of the group
            membership = Membership(user_id=current_user.id, group_id=new_group.id)
            db.session.add(membership)
            db.session.commit()
            flash('Group created successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the group. Please try again.', 'danger')
    return render_template('dashboard/create_group.html', form=form, user=current_user)

@dashboard.route('/group/<int:group_id>/call')
@login_required
def group_call(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('dashboard/call.html', group=group, user=current_user)

@dashboard.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('dashboard/profile.html', user=user)

@dashboard.route('/group/<int:group_id>/add_member', methods=['GET', 'POST'])
@login_required
def add_member(group_id):
    group = Group.query.get_or_404(group_id)
    form = AddMemberForm()
    if form.validate_on_submit():
        identifier = form.identifier.data
        user = User.query.filter((User.email == identifier) | (User.phone_number == identifier)).first()
        if user:
            membership = Membership(user_id=user.id, group_id=group.id)
            db.session.add(membership)
            db.session.commit()
            flash('Member added successfully!', 'success')
            return redirect(url_for('dashboard.view_group', group_id=group_id))
        else:
            flash('User not found.', 'danger')
    return render_template('dashboard/add_member.html', form=form, group=group, user=current_user)
