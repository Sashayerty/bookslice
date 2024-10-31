import flask_login as login
from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView


class BaseView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("admin_login", next=request.url))
