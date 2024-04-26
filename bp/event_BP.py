from flask import Blueprint

#
# from flask import request, render_template, redirect, url_for, session
# from ..models.event import Event
# from ..models.user import User
# from ..models import db
# from ..utils.forms import EventForm


event_bp = Blueprint("event", __name__, url_prefix="/event")


@event_bp.route('/', methods=['POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            location=form.location.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            description=form.description.data,
            creator_id=session['user_id']
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('event.get_event', id=event.id))
    return render_template('create_event.html', form=form)


@event_bp.route('/', methods=['GET'])
def get_events():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    events = Event.query.order_by(Event.start_time.desc()).paginate(page, per_page, error_out=False)
    return render_template('event_list.html', events=events)


@event_bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get(id)
    return render_template('event_detail.html', event=event)


@event_bp.route('/<int:id>/attendees', methods=['POST'])
def attend_event(id):
    event = Event.query.get(id)
    user = User.query.get(session['user_id'])
    event.attendees.append(user)
    db.session.commit()
    return redirect(url_for('event.get_event', id=id))


@event_bp.route('/<int:id>/attendees/<int:user_id>', methods=['DELETE'])
def cancel_attend_event(id, user_id):
    event = Event.query.get(id)
    user = User.query.get(user_id)
    event.attendees.remove(user)
    db.session.commit()
    return redirect(url_for('event.get_event', id=id))
