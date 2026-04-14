from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/stream")
def events_stream():
    def event_gen():
        yield "event: heartbeat\ndata: ok\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")
