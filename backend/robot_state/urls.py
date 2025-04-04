from django.urls import path
from robot_state.views import sse_stream

urlpatterns = [
    path("stream/", sse_stream, name="sse_stream"),
]
