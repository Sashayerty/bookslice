import flask_login as login
from flask import redirect, request, url_for
from flask_admin.contrib.fileadmin import FileAdmin


class StaticFilesView(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("admin_login", next=request.url))
