from django.urls import path, re_path

from graphs.consumers import WSConsumer

ws_urlpatterns = [
    re_path(r'ws/some_url/$', WSConsumer.as_asgi())
]