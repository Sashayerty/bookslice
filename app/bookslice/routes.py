from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_required, login_user, logout_user

from app.models import Users, db_session
from app.static.forms import LoginForm, RegisterForm
from app.static.forms.chat import ChatForm

from .friends_model import friends as f
from .functions.AI import AI
from .notifications_model import notifications1, notifications2

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
    return render_template(
        "friends.html",
        title="Друзья",
        user_is_auth=current_user.is_authenticated,
        admin=(current_user.admin if current_user.is_authenticated else False),
        friends=f,
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
    # ! Здесь логика для функции по добавлению друзей!
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
    pass


@bookslice.route(
    "/notifications",
    methods=[
        "GET",
        "POST",
    ],
)
def notifications():
    """Отображение уведомлений юзера"""
    return render_template(
        "notifications.html",
        title="Уведомления",
        user_is_auth=current_user.is_authenticated,
        admin=(current_user.admin if current_user.is_authenticated else False),
        notifications_list=[
            notifications1,
            notifications2,
        ],
    )
