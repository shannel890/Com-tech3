from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.message import Message
from app.models.user import User
from app.extension import db

api = Blueprint("api", __name__)

@api.route("/messages/<int:group_id>", methods=["GET"])
@login_required
def get_messages(group_id):
    """
    Fetch paginated chat messages for a group.
    Query params:
      ?page=1
      ?per_page=20
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = (
        Message.query
        .filter_by(group_id=group_id)
        .order_by(Message.timestamp.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    messages = [
        {
            "id": msg.id,
            "user_id": msg.user_id,
            "user_name": User.query.get(msg.user_id).name,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in pagination.items
    ]

    return jsonify({
        "messages": messages[::-1],  # reverse to show oldest first
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    })
