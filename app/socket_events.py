from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from datetime import datetime
from app.models.group import  Group
from app.models.message import  Message
from app.extension import db


socketio = SocketIO()  # initialized in app factory


# To store participants in active calls
# Format: { 'group_id_str': { user_id: user_name } }
call_participants = {}


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


# WebRTC Signaling Events
@socketio.on('join_call')
def handle_join_call(data):
    group_id = str(data['group_id'])
    user_id = current_user.id
    user_name = current_user.name

    join_room(group_id)

    if group_id not in call_participants:
        call_participants[group_id] = {}

    # Notify existing users
    emit('user_joined_call', {'user_id': user_id, 'user_name': user_name}, to=group_id, include_self=False)

    # Send current participants to the new user
    emit('all_users', {'users': [
        {'id': uid, 'name': uname} for uid, uname in call_participants.get(group_id, {}).items()
    ]})

    call_participants[group_id][user_id] = user_name
    print(f"User {user_name} joined call in group {group_id}. Participants: {call_participants[group_id]}")


@socketio.on('leave_call')
def handle_leave_call(data):
    group_id = str(data['group_id'])
    user_id = current_user.id

    leave_room(group_id)

    if group_id in call_participants and user_id in call_participants[group_id]:
        del call_participants[group_id][user_id]
        if not call_participants[group_id]:  # If group call is empty
            del call_participants[group_id]

        emit('user_left_call', {'user_id': user_id}, to=group_id)
        print(f"User {user_id} left call in group {group_id}. Remaining: {call_participants.get(group_id)}")


@socketio.on('offer')
def handle_offer(data):
    group_id = str(data['group_id'])
    emit('offer', data, to=group_id, include_self=False)


@socketio.on('answer')
def handle_answer(data):
    group_id = str(data['group_id'])
    emit('answer', data, to=group_id, include_self=False)


@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    group_id = str(data['group_id'])
    emit('ice_candidate', data, to=group_id, include_self=False)
