from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from datetime import datetime
from app.models.group import  Group
from app.models.message import  Message
from app.extension import db


socketio = SocketIO()  # initialized in app factory


@socketio.on("join_group")
def handle_join_group(data):
    """When user joins a group room"""
    group_id = data.get("group_id")
    join_room(str(group_id))

    emit("receive_message", {
        "user": "System",
        "content": f"{current_user.name} joined the chat.",
        "timestamp": datetime.now().strftime("%H:%M"),
        "user_id": 0
    }, to=str(group_id))


@socketio.on("leave_group")
def handle_leave_group(data):
    """When user leaves a group room"""
    group_id = data.get("group_id")
    leave_room(str(group_id))

    emit("receive_message", {
        "user": "System",
        "content": f"{current_user.name} left the chat.",
        "timestamp": datetime.now().strftime("%H:%M"),
        "user_id": 0
    }, to=str(group_id))


@socketio.on("send_message")
def handle_send_message(data):
    """Handles sending and broadcasting messages"""
    group_id = data.get("group_id")
    content = data.get("content", "").strip()

    if not content:
        return

    # Store message in database
    msg = Message(
        group_id=group_id,
        user_id=current_user.id,
        content=content,
        timestamp=datetime.utcnow()
    )
    db.session.add(msg)
    db.session.commit()

    # Broadcast message to group
    emit("receive_message", {
        "user": current_user.name,
        "content": content,
        "timestamp": msg.timestamp.strftime("%H:%M"),
        "user_id": current_user.id
    }, to=str(group_id))
