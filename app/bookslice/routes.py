from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
)
from flask_login import current_user, login_required, login_user, logout_user

from app.bookslice.functions.notification_sender import (
    send_to_user_friend_request_notification,
)
from app.bookslice.functions.search_friends import search_partial_match_fuzzy
from app.models import Notifications, Users, db_session
from app.models.authors import Authors
from app.models.books import Books
from app.models.books_of_user import BooksOfUser
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


@bookslice.route("/conditions-of-using")
def conditions_of_using():
    return send_file(
        "./static/conditions_of_using/Условия_использования_BookSlice.pdf"
    )


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
        messages = ai.message(form.message.data, user_id=current_user.id)
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
        users_friends = [
            i.id
            for i in db_ses.query(Friendships)
            .filter_by(user_id=current_user.id)
            .all()
        ]
        all_users = db_ses.query(Users)
        users_names = list(
            map(
                lambda x: x.name,
                list(
                    filter(
                        lambda x: x.id not in users_friends,
                        all_users.filter(Users.id != current_user.id).all(),
                    )
                ),
            )
        )
        searched_users = list(
            set(search_partial_match_fuzzy(users_names, search))
        )
        searched_users_models = []
        for i in searched_users:
            searched_users_models.extend(all_users.filter_by(name=i).all())
            searched_users_models = set(searched_users_models)
    else:
        searched_users_models = []
        friends_of_user_ids = [
            i.friends_ids
            for i in db_ses.query(Friendships)
            .filter_by(user_id=current_user.id)
            .all()
        ]
        friends_of_user = []
        if friends_of_user_ids:
            for i in friends_of_user_ids:
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

    send_to_user_friend_request_notification(
        user_id=current_user.id,
        data=str(user_id),
        db_session=db_ses,
    )
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
    db_ses.query(Friendships).filter_by(
        user_id=current_user.id, friends_ids=user_id
    ).delete()
    db_ses.query(Friendships).filter_by(
        user_id=user_id, friends_ids=current_user.id
    ).delete()
    db_ses.commit()
    return redirect("/friends")


@bookslice.route(
    "/accept-friend-request/<int:user_id>",
    methods=[
        "POST",
        "GET",
    ],
)
@login_required
def accept_friend_request(user_id: int):
    """Принятие запроса в друзья"""
    friendships = (
        db_ses.query(Friendships).filter_by(user_id=current_user.id).all()
    )
    for i in friendships:
        if i.friends_ids == user_id:
            db_ses.query(Notifications).filter_by(
                user_id=current_user.id,
                data=user_id,
                type="friendrequest",
            ).delete()
            db_ses.commit()
            return redirect("/notifications")
    friend_to_friend, friend_to_current_user = (
        Friendships(
            user_id=user_id,
            friends_ids=current_user.id,
        ),
        Friendships(
            user_id=current_user.id,
            friends_ids=user_id,
        ),
    )
    db_ses.add(friend_to_current_user)
    db_ses.add(friend_to_friend)
    db_ses.query(Notifications).filter_by(
        user_id=current_user.id,
        data=user_id,
        type="friendrequest",
    ).delete()
    db_ses.commit()
    return redirect("/notifications")


@bookslice.route("/dismiss-friend-request/<int:user_id>")
@login_required
def dismiss_friend_request(user_id):
    """Функция отказа от запроса в друзья"""
    db_ses.query(Notifications).filter_by(
        user_id=current_user.id,
        data=user_id,
        type="friendrequest",
    ).delete()
    db_ses.commit()
    return redirect("/notifications")


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


@bookslice.route(
    "/get-user-data-for-ai",
    methods=[
        "POST",
        "GET",
    ],
)
def get_user_data_for_ai():
    user_id = request.args.get("user_id", default=None, type=int)
    if user_id:
        user = db_ses.query(Users).get(user_id)
        read_books_of_user_ids = list(
            map(
                lambda x: x.book_id,
                db_ses.query(BooksOfUser).filter_by(
                    user_id=user_id,
                    status="Прочитал",
                ),
            )
        )
        read_books_of_user_cartages = []
        all_books = db_ses.query(Books)
        all_authors = db_ses.query(Authors)
        for i in read_books_of_user_ids:
            book = all_books.filter_by(id=i).first()
            author = all_authors.filter_by(id=book.author).first().name
            read_books_of_user_cartages.append(
                {"id": i, "title": book.title, "author": author}
            )
        user_data = {
            "read_stats": {
                "count_of_read_books": user.read_books,
                "count_of_summarized_books": user.summarized_books,
            },
            "read_books": read_books_of_user_cartages,
        }
        all_books_ids = list(map(lambda x: x.id, all_books.all()))
        all_books_list_of_cartages = []
        for i in all_books_ids:
            book = all_books.filter_by(id=i).first()
            author = all_authors.filter_by(id=book.author).first().name
            all_books_list_of_cartages.append(
                {"id": i, "title": book.title, "author": author}
            )
        return jsonify(
            {
                "read_data_of_user": user_data,
                "data_of_books_of_all_catalog": all_books_list_of_cartages,
            }
        )
    else:
        return jsonify({"error": "User id not found."})
