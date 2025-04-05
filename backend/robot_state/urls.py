from django.urls import path
from robot_state.views import sse_stream, set_state, reset, change_fan_speed


urlpatterns = [
    path("stream/", sse_stream, name="sse_stream"),
    path("state/", set_state, name="set_state"),
    path("reset/", reset, name="reset"),
    path("fan_speed/", change_fan_speed, name="change_fan_speed"),
]
