from sqlalchemy.orm import Session

from app.models.db_session import create_session, global_init
from app.models.notifications import Notifications


def session_create() -> Session:
    global_init("app/app.db")
    db_session = create_session()
    return db_session


def send_to_user_friend_request_notification(
    user_id: int,
    friend_id: int,
    data: str | int,
    db_session: Session = session_create(),
) -> bool:
    notifications = db_session.query(Notifications)  # noqa
