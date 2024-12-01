from datetime import datetime

from flask import Blueprint, redirect, render_template, request, session
from flask_login import current_user, login_required

from app.models import db_session
from app.models.achievements import Achievements
from app.models.achievements_of_users import AchievementsOfUsers
from app.models.users import Users

profile = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile",
    template_folder="../templates/profile",
)

db_session.global_init("../app.db")
db_ses = db_session.create_session()


def get_user_data(user):
    return {
        "name": user.name,
        "email": user.email,
        "id": user.id,
        "user_is_auth": current_user.is_authenticated,
        "admin": (
            current_user.admin if current_user.is_authenticated else False
        ),
    }


@profile.route("/", methods=["GET", "POST"])
@login_required
def index():
    page = request.args.get("page", type=str, default="data")
    if page not in ["data", "achievements", "stats"]:
        return redirect("/not-found")

    user_data = get_user_data(current_user)
    user_data.update({"current_user": True})

    if page == "data":
        return render_template(
            "profile.html", title="Профиль", **user_data, data=True
        )

    elif page == "achievements":
        achievements = (
            db_ses.query(AchievementsOfUsers)
            .filter_by(user_id=current_user.id)
            .all()
        )
        achievements_names = (
            sorted(
                [
                    db_ses.query(Achievements)
                    .filter_by(id=i.achievement_id)
                    .first()
                    for i in achievements
                ],
                key=lambda x: x.reward,
                reverse=True,
            )
            if achievements
            else 0
        )
        return render_template(
            "profile.html",
            title="Профиль",
            achievements=achievements_names,
            ach=True,
            **user_data
        )

    elif page == "stats":
        return render_template(
            "profile.html",
            title="Профиль",
            read_books=current_user.read_books or 0,
            summarized_books=current_user.summarized_books or 0,
            speed_of_reading=current_user.speed_of_reading,
            read_data=True,
            **user_data
        )


@profile.route("/check-speed-of-reading")
@login_required
def check_speed_of_reading():
    """Страница проверки скорости чтения"""
    return render_template(
        "check_speed_of_reading.html",
        title="Проверить скорость чтения",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
        user_id=current_user.id,
    )


@profile.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile_of_user(user_id: int):
    page = request.args.get("page", type=str, default="data")
    user = db_ses.query(Users).filter_by(id=user_id).first()
    if not user or page not in ["data", "achievements", "stats"]:
        return redirect("/not-found")

    user_data = get_user_data(user)
    user_data["current_user"] = user.id == current_user.id

    if page == "data":
        return render_template(
            "profile.html", title=user.name, data=True, **user_data
        )

    elif page == "achievements":
        achievements = (
            db_ses.query(AchievementsOfUsers).filter_by(user_id=user.id).all()
        )
        achievements_names = (
            sorted(
                [
                    db_ses.query(Achievements)
                    .filter_by(id=i.achievement_id)
                    .first()
                    for i in achievements
                ],
                key=lambda x: x.reward,
                reverse=True,
            )
            if achievements
            else 0
        )
        return render_template(
            "profile.html",
            title=user.name,
            achievements=achievements_names,
            ach=True,
            **user_data
        )

    elif page == "stats":
        return render_template(
            "profile.html",
            title=user.name,
            read_books=user.read_books or 0,
            summarized_books=user.summarized_books or 0,
            speed_of_reading=user.speed_of_reading,
            read_data=True,
            **user_data
        )


@profile.route("/start-test", methods=["POST", "GET"])
@login_required
def start_test():
    """Старт теста скорости чтения"""
    session["start_time"] = datetime.now().isoformat()
    return "", 204


@profile.route("/end-test", methods=["POST", "GET"])
@login_required
def end_test():
    """Конец теста скорости чтения"""
    start_time_str = session.get("start_time")
    if start_time_str is None:
        return redirect("/not-found")

    duration = (
        datetime.now() - datetime.fromisoformat(start_time_str)
    ).total_seconds() / 60
    reading_speed = 188 / duration

    db_ses.query(Users).get(current_user.id).speed_of_reading = int(
        reading_speed
    )
    db_ses.commit()
    session["start_time"] = None
    return redirect("/profile")
