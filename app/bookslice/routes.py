from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

from app.bookslice.functions.search_friends import search_partial_match_fuzzy
from app.models import Notifications, Users, db_session
from app.models.friend_requests import FriendRequests
from app.models.friendships import Friendships
from app.static.forms import LoginForm, RegisterForm
from app.static.forms.chat import ChatForm

from .functions.AI import AI

bookslice = Blueprint(
    "bookslice",
    __name__,
    template_folder="../templates/bookslice",
)
db_session.global_init("../app.db")
db_ses = db_session.create_session()
ai = AI()


@bookslice.route("/")
def index():
    """Главная страница"""
    return render_template(
        "index.html",
        title="Главная",
        user_is_auth=current_user.is_authenticated,
        admin=(current_user.admin if current_user.is_authenticated else False),
    )


@bookslice.route(
    "/register",
    methods=[
        "GET",
        "POST",
    ],
)
def register():
    """Страница регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        if len(form.password.data) < 8:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Длина пароля должна быть не менее 8 символов",
            )
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = Users(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template(
        "register.html",
        title="Регистрация",
        form=form,
    )


def render_login_page(title, form, message=""):
    return render_template(
        "login.html",
        title=title,
        form=form,
        message=message,
    )


@bookslice.route(
    "/login",
    methods=[
        "POST",
        "GET",
    ],
)
def login():
    """Страница входа"""
    form = LoginForm()
    if form.validate_on_submit():
        user = (
            db_ses.query(Users).filter(Users.email == form.email.data).first()
        )
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_login_page(
            title="Вход", form=form, message="Неправильный логин или пароль"
        )
    return render_login_page(title="Вход", form=form)


@bookslice.route(
    "/admin/login",
    methods=[
        "POST",
        "GET",
    ],
)
def admin_login():
    """Страница входа в админку"""
    form = LoginForm()
    if form.validate_on_submit():
        user = (
            db_ses.query(Users).filter(Users.email == form.email.data).first()
        )
        if user and user.check_password(form.password.data):
            login_user(
                user,
                remember=form.remember_me.data,
            )
            return redirect("/admin")
        elif user and not user.admin:
            return render_template(
                "admin/admin_login.html",
                message="У Вас нет доступа к админ-панели!",
                form=form,
            )
        return render_template(
            "admin/admin_login.html",
            message="Неправильный логин или пароль",
            form=form,
        )
    return render_template(
        "admin/admin_login.html",
        title="BookSlice Admin",
        form=form,
    )


@bookslice.route("/logout")
@login_required
def logout():
    """Страница выхода"""
    logout_user()
    return redirect("/")


@bookslice.route(
    "/ask",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def ask():
    """Страница для общения с ИИ"""
    form = ChatForm()
    if form.validate_on_submit():
        messages = ai.message(form.message.data)
        messages = ai.get_messages()
        return render_template(
            "ask.html",
            title="Спросить ИИ",
            form=form,
            user_is_auth=current_user.is_authenticated,
            admin=(
                current_user.admin if current_user.is_authenticated else False
            ),
            messages=messages,
            user_id=current_user.id,
        )
    messages = ai.get_messages()
    return render_template(
        "ask.html",
        title="Спросить ИИ",
        form=form,
        user_is_auth=current_user.is_authenticated,
        admin=(current_user.admin if current_user.is_authenticated else False),
        messages=messages,
        user_id=current_user.id,
    )


@bookslice.route(
    "/friends",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def friends():
    """Страница с друзьями"""
    search = request.args.get("search", type=str, default=None)
    if search:
        friends_of_user = []
        all_users = db_ses.query(Users)
        users_names = [i.name for i in all_users.all()]
        searched_users = list(
            set(search_partial_match_fuzzy(users_names, search))
        )
        searched_users_models = []
        for i in searched_users:
            searched_users_models.extend(all_users.filter_by(name=i).all())
            searched_users_models = set(searched_users_models)
    else:
        searched_users_models = []
        friends_of_user_ids = (
            db_ses.query(Friendships)
            .filter_by(user_id=current_user.id)
            .first()
        )
        friends_of_user = []
        if friends_of_user_ids:
            for i in friends_of_user_ids.friends_ids.split(", "):
                friends_of_user.append(
                    db_ses.query(Users).filter_by(id=int(i)).first()
                )
    return render_template(
        "friends.html",
        title="Друзья",
        user_is_auth=current_user.is_authenticated,
        admin=(current_user.admin if current_user.is_authenticated else False),
        friends=friends_of_user,
        searched_users=searched_users_models,
        search=search,
    )


@bookslice.route(
    "/add-friend/<int:user_id>",
    methods=[
        "POST",
        "GET",
    ],
)
@login_required
def add_friend(user_id: int):
    """Добавление в друзья"""
    users_requests_to_friends = (
        db_ses.query(FriendRequests).filter_by(user_id=user_id).first()
    )
    users_notifications_of_requests_to_friends = (
        db_ses.query(Notifications).filter_by(user_id=user_id).all()
    )
    if users_notifications_of_requests_to_friends:
        if users_notifications_of_requests_to_friends.friends_ids:
            if str(
                current_user.id
            ) in users_notifications_of_requests_to_friends.friends_ids.split(
                ", "
            ):
                return redirect("/friends")
            else:
                pass
    else:
        pass
    if users_requests_to_friends:
        pass
    else:
        pass
    # if users_requests_to_friends:
    #     list_of_users_requests_to_friends = (
    #         users_requests_to_friends.friends_ids.split(", ")
    #     )
    # else:
    #     list_of_users_requests_to_friends = []
    # if str(user_id) not in list_of_users_requests_to_friends:
    #     list_of_users_requests_to_friends.append(str(user_id))
    #     list_of_users_requests_to_friends.sort()
    #     if db_ses.query(Notifications).filter_by(
    #         user_id=user_id, data=current_user.id
    #     ):
    #         return redirect("/friends")
    #     else:
    #         notification_of_friend_request = Notifications(
    #             type="friendrequest",
    #             user_id=user_id,
    #             data=current_user.id,
    #         )
    #         db_ses.add(notification_of_friend_request)
    #     db_ses.commit()
    # else:
    #     return redirect("/friends")
    # ? ! Додумать эту хрень наконец-то
    return redirect("/friends")


@bookslice.route(
    "/delete-friend/<int:user_id>",
    methods=[
        "POST",
        "GET",
    ],
)
@login_required
def delete_friend(user_id: int):
    """Удаление из друзей"""
    # ! Здесь логика для функции по удалению друзей!
    return redirect("/friends")


@bookslice.route(
    "/accept-friend-request/<int:user_id>",
    methods=[
        "POST",
    ],
)
@login_required
def accept_friend_request(user_id: int):
    """Принятие запроса в друзья"""
    friend_requests = (
        db_ses.query(FriendRequests)
        .filter_by(user_id=current_user.id)
        .first()
        .friends_ids.split(", ")
    )
    if str(user_id) in friend_requests and user_id != current_user.id:
        db_ses.query(Friendships).filter_by(
            user_id=current_user.id
        ).first().friends_ids += ", " + str(user_id)
        return redirect("/notifications")
    else:
        return redirect("/not-found")


@bookslice.route(
    "/notifications",
    methods=[
        "GET",
        "POST",
    ],
)
def notifications():
    """Отображение уведомлений юзера"""
    notifications_list = (
        db_ses.query(Notifications).filter_by(user_id=current_user.id).all()
    )
    print(notifications_list)
    return render_template(
        "notifications.html",
        title="Уведомления",
        user_is_auth=current_user.is_authenticated,
        admin=(current_user.admin if current_user.is_authenticated else False),
        notifications_list=notifications_list,
    )


@bookslice.route(
    "/notification-read/<int:notification_id>", methods=["GET", "POST"]
)
def notification_read(notification_id):
    notification = db_ses.query(Notifications).filter_by(id=notification_id)
    notification.delete()
    db_ses.commit()
    return redirect("/notifications")
