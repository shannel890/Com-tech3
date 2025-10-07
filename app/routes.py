from flask import Blueprint,render_template,jsonify, request, flash, url_for, redirect
from flask_login import login_required, current_user
from app.models.message import Message
from app.models.group import Group
from app.form import MessageForm
from app.extension import db

main = Blueprint('main',__name__)

@main.route('/')
def landing_page():
    return render_template("landing_page.html")



@main.route('/api/groups/<int:group_id>/messages', methods=['GET'])
def get_messages(group_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Message.query.filter_by(group_id=group_id)\
                              .order_by(Message.timestamp.asc())\
                              .paginate(page=page, per_page=per_page, error_out=False)
    
    messages = [{
        'user_id': m.user_id,
        'content': m.content,
        'timestamp': m.timestamp.isoformat()
    } for m in pagination.items]
    
    return jsonify({
        'messages': messages,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    })

@main.route('/group/<int:group_id>/chat', methods=['GET', 'POST'])
@login_required
def group_chat(group_id):
    group = Group.query.get_or_404(group_id)
    messages = Message.query.filter_by(group_id=group_id).order_by(Message.timestamp.asc()).all()
    form = MessageForm()

    return render_template('group_chat.html', group=group, messages=messages, form=form)

