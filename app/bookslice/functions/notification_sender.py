from sqlalchemy.orm import Session

from app.models.db_session import create_session, global_init
from app.models.notifications import Notifications


def session_create() -> Session:
    global_init("app/app.db")
    db_session = create_session()
    return db_session


def send_to_user_friend_request_notification(
    user_id: int,
    data: str,
    db_session: Session = session_create(),
    type: str = "friendrequest",
) -> bool:
    notifications = db_session.query(Notifications)
    if notifications.filter_by(user_id=user_id, data=data, type=type).first():
        return True
    else:
        notification = Notifications(
            type=type,
            data=user_id,
            user_id=data,
        )
        db_session.add(notification)
        db_session.commit()
        return True
