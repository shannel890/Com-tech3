from flask_socketio import join_room, leave_room, emit
from flask_login import current_user
from datetime import datetime
from app.models.message import  Message
from app.extension import db

def register_socketio_events(socketio):
    @socketio.on('join_group')
    def handle_join_group(data):
        if not data or 'group_id' not in data:
            return
        group_id = data['group_id']
        # Validate group_id is an integer
        try:
            group_id = int(group_id)
        except (ValueError, TypeError):
            return
        join_room(str(group_id))
        emit('status', {'msg': f"{current_user.name} joined group {group_id}"}, room=str(group_id))

    @socketio.on('leave_group')
    def handle_leave_group(data):
        if not data or 'group_id' not in data:
            return
        group_id = data['group_id']
        # Validate group_id is an integer
        try:
            group_id = int(group_id)
        except (ValueError, TypeError):
            return
        leave_room(str(group_id))
        emit('status', {'msg': f"{current_user.name} left group {group_id}"}, room=str(group_id))

    @socketio.on('send_message')
    def handle_send_message(data):
        if not data or 'group_id' not in data or 'content' not in data:
            return
        
        group_id = data['group_id']
        content = data['content']
        
        # Validate group_id is an integer
        try:
            group_id = int(group_id)
        except (ValueError, TypeError):
            return
        
        # Validate content is a string and not empty
        if not isinstance(content, str) or not content.strip():
            return
        
        # Enforce maximum message length (500 chars as per MessageForm)
        content = content[:500]

        # Store message in DB
        msg = Message(group_id=group_id, user_id=current_user.id, content=content, timestamp=datetime.utcnow())
        db.session.add(msg)
        db.session.commit()

        # Broadcast message to group
        emit('receive_message', {
            'user': current_user.name,
            'content': content,
            'timestamp': msg.timestamp.strftime('%H:%M:%S')
        }, room=str(group_id))
