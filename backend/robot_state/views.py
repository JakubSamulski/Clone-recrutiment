import asyncio
import random

from django.http import StreamingHttpResponse
from django.shortcuts import render


async def sse_stream(request):

    async def event_stream():
        while True:
            yield f"data:  {i}\n\n"
            i += 1
            await asyncio.sleep(1)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
