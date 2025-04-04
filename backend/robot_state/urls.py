from django.urls import path
from robot_state.views import sse_stream, set_state

urlpatterns = [
    path("stream/", sse_stream, name="sse_stream"),
    path("state/", set_state, name="set_state"),
]
