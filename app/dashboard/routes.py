from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.group import Group
from app.models.message import Message
from app.models.membership import Membership


dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/')
@login_required
def index():
    groups = Group.query.all()
    return render_template('dashboard/dashboard.html', groups=groups, user=current_user)

@dashboard.route('/group/<int:group_id>')
@login_required
def view_group(group_id):
    group = Group.query.get_or_404(group_id)
    messages = Message.query.filter_by(group_id=group.id).order_by(Message.timestamp.asc()).all()
    return render_template('dashboard/group_chat.html', group=group, messages=messages, user=current_user)
