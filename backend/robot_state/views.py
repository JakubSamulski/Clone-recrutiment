import asyncio
import random

from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from robot_state.robot import RobotMock

from robot_state.robot import State

robot = RobotMock()


async def sse_stream(request):

    async def event_stream():
        while True:
            yield f"data: {robot.toJson()}\n\n"
            await asyncio.sleep(1 / 10)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


@api_view(["POST"])
def set_state(request):
    state = request.data.get("state")
    if state:
        if state.upper() not in State.__members__:
            return Response({"status": "error", "message": "Invalid state"}, status=401)
        robot.state = State[state.upper()]
        return Response({"status": "success", "state": robot.state.value})
    else:
        return Response(
            {"status": "error", "message": "State not provided"}, status=401
        )


@api_view(["POST"])
def reset(request):
    try:
        robot.reset()
        return Response({"status": "success", "message": "Robot reset"})
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=401)


@api_view(["POST"])
def change_fan_speed(request):
    fan_mode = request.data.get("fan_mode")
    value = request.data.get("value")
    if fan_mode:
        if fan_mode == "linear":
            robot.set_fan_speed(fan_mode)
        elif fan_mode == "custom" and value is not None:
            robot.set_fan_speed(fan_mode, value)
        else:
            return Response(
                {"status": "error", "message": "Invalid fan mode or value"}, status=401
            )
        return Response({"status": "success", "fan_speed": robot.fan_speed})
    else:
        return Response(
            {"status": "error", "message": "Fan mode not provided"}, status=401
        )
