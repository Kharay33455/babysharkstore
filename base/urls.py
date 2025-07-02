from django.urls import path
from .views import *

app_name="base"

urlpatterns=[
    path("", index, name="index"),
    path("generate/<slug:gen_type>/", generate_link, name="gen_link"),
    path("login/", login_request, name = "login_request"),
    path("fetch-data", fetch_data, name="fetch_data"),
    path("handle-session/<session_id>/<action>/", handle_session, name="handle_session"),
]