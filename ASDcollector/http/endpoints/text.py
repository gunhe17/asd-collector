from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ASDcollector.usecase.write_txt import (
    write
)


"""Command"""

class PostTXTInput(BaseModel):
    user_id: str

async def post_txt(input: PostTXTInput):
    write(
        user_id=input.user_id,
    )

    return JSONResponse(content={
        "data": "TXT written successfully"
    })