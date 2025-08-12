from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from fastapi import Request
import subprocess
from subprocess import Popen

import traceback
import asyncio
import json
import os


# #
# Config

templates = Jinja2Templates(directory="./ASDcollector/http/templates")


# #
# page

async def home_page(request: Request):
    return templates.TemplateResponse("home/page.html", {
        "request": request
    })

async def calibrate_page(request: Request, user_id: str):
    return templates.TemplateResponse("calibrate/page.html", {
        "request": request
    })

async def capture_page(request: Request, user_id: str, video_id: int):
    return templates.TemplateResponse("capture/page.html", {
        "request": request,
    })

async def monitor_page(request: Request, user_id: str):
    return templates.TemplateResponse("monitor/page.html", {
        "request": request,
    })
