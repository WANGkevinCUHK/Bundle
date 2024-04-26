from flask import Blueprint, request, jsonify
from models.event import Event
from models.user import User
from utils.auth import auth_required
from bson import ObjectId

event_bp = Blueprint('event', __name__, url_prefix='/event')


@event_bp.route('/', methods=['POST'])
@auth_required
def create_event(current_user):
    data = request.get_json()
    title = data.get('title')
    location = data.get('location')
    time = data.get('time')
    description = data.get('description')

    event = Event(title=title, location=location, time=time, description=description, creator=current_user)
    event.save()

    return jsonify(event.to_json()), 201


@event_bp.route('/', methods=['GET'])
def list_events():
    events = Event.objects()
    return jsonify([event.to_json() for event in events]), 200


@event_bp.route('/<event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.objects(id=ObjectId(event_id)).first()
    if not event:
        return jsonify({"message": "Event not found"}), 404
    return jsonify(event.to_json()), 200


@event_bp.route('/<event_id>/join', methods=['POST'])
@auth_required
def join_event(current_user, event_id):
    event = Event.objects(id=ObjectId(event_id)).first()
    if not event:
        return jsonify({"message": "Event not found"}), 404

    if current_user in event.participants:
        return jsonify({"message": "You have already joined this event"}), 400

    event.participants.append(current_user)
    event.save()

    return jsonify(event.to_json()), 200


@event_bp.route('/<event_id>/leave', methods=['POST'])
@auth_required
def leave_event(current_user, event_id):
    event = Event.objects(id=ObjectId(event_id)).first()
    if not event:
        return jsonify({"message": "Event not found"}), 404

    if current_user not in event.participants:
        return jsonify({"message": "You have not joined this event"}), 400

    event.participants.remove(current_user)
    event.save()

    return jsonify(event.to_json()), 200