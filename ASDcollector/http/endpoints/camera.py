from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ASDcollector.usecase.record_camera import (
    record,
    stop,
    monitor,
)

from ASDcollector.usecase.calibrate_camera import (
    calibrate,
    delete,
    calibrate_test
)


"""Command"""

class PostCalibrateInput(BaseModel):
    user_id: str

async def post_calibrate(input: PostCalibrateInput):
    is_calibrated = calibrate(
        user_id=input.user_id,
    )

    return JSONResponse(content={
        "data": is_calibrated
    })


async def delete_calibrate(user_id: str):
    is_deleted = delete(
        user_id=user_id,
    )

    return JSONResponse(content={
        "data": is_deleted
    })


async def post_calibrate_test(user_id: str):
    is_tested = calibrate_test(
        user_id=user_id
    )

    return JSONResponse(content={
        "data": is_tested
    })


class PostRecordInput(BaseModel):
    video_id: int
    user_id: str

async def post_record(input: PostRecordInput):
    is_record = record(
        video_id=input.video_id, 
        user_id=input.user_id,
    )

    return JSONResponse(content={
        "data": is_record
    })


class PostStopInput(BaseModel):
    user_id: str

async def post_stop(input: PostStopInput):
    is_stopped = stop(input.user_id)

    return JSONResponse(content={
        "data": is_stopped
    })


"""Query"""

async def get_monitor():
    monitored = monitor()

    print(monitored)

    return JSONResponse(content={
        "data": monitored
    })