from ASDcollector.http.server import (
    templates, 
    session, 
    cors,
    lifespan,
    service_error_handler,
    Task,
    Router,
    Server,
    ExceptionHandler,
)
from ASDcollector.http.endpoints.user import (
    post_user,
    get_user_by_id
)
from ASDcollector.http.endpoints.solution import (
    get_solution_by_id,
    get_solution_video_by_id,
    get_every_solution,
)
from ASDcollector.http.endpoints.collection import (
    get_collection_by_id,
    get_collection_video_by_user_id_and_video_id,
)
from ASDcollector.http.endpoints.camera import (
    post_calibrate,
    delete_calibrate,
    post_calibrate_test,
    post_record,
    post_stop,
    get_monitor,
)
from ASDcollector.http.endpoints.openai import (
    post_openai
)
from ASDcollector.http.endpoints.csv import (
    post_csv
)
from ASDcollector.http.endpoints.text import (
    post_txt
)
from ASDcollector.http.endpoints.view import (
    home_page,
    capture_page,
    monitor_page,
    calibrate_page
)


# #
# server

server = Server(name="ASDcollector")


# #
# mount

server.mount(
    mount=templates()
)


# #
# middleware

server.middleware(
    middleware=session()
)

server.middleware(
    middleware=cors()
)


# #
# Task

server.task(
    task=lifespan(startup=[])
)

# #
# exception

server.exception(
    exception=service_error_handler()
)


# #
# API: back

# user
server.router(
    Router(path="/backend-api/user", methods=["POST"], endpoint=post_user, dependencies=[])
)

server.router(
    Router(path="/backend-api/user/{id}", methods=["GET"], endpoint=get_user_by_id, dependencies=[])
)

# video
server.router(
    Router(path="/backend-api/solution/v/{video_id}", methods=["GET"], endpoint=get_solution_video_by_id, dependencies=[])
)

server.router(
    Router(path="/backend-api/solution", methods=["GET"], endpoint=get_every_solution, dependencies=[])
)

server.router(
    Router(path="/backend-api/collection/video/u/{user_id}/v/{video_id}", methods=["GET"], endpoint=get_collection_video_by_user_id_and_video_id, dependencies=[])
)

# camera
server.router(
    Router(path="/backend-api/camera/calibrate", methods=["POST"], endpoint=post_calibrate, dependencies=[])
)

server.router(
    Router(path="/backend-api/camera/calibrate/u/{user_id}", methods=["DELETE"], endpoint=delete_calibrate, dependencies=[])
)

server.router(
    Router(path="/backend-api/camera/calibrate/test/u/{user_id}", methods=["POST"], endpoint=post_calibrate_test, dependencies=[])
)

server.router(
    Router(path="/backend-api/camera/record", methods=["POST"], endpoint=post_record, dependencies=[])
)

server.router(
    Router(path="/backend-api/camera/stop", methods=["POST"], endpoint=post_stop, dependencies=[])
)

server.router(
    Router(path="/backend-api/camera/monitor", methods=["GET"], endpoint=get_monitor, dependencies=[])
)

# openai
server.router(
    Router(path="/backend-api/openai", methods=["POST"], endpoint=post_openai, dependencies=[])
)

# csv
server.router(
    Router(path="/backend-api/csv", methods=["POST"], endpoint=post_csv, dependencies=[])
)

# text
server.router(
    Router(path="/backend-api/txt", methods=["POST"], endpoint=post_txt, dependencies=[])
)

# #
# API: front

# home
server.router(
    Router(path="/home", methods=["GET"], endpoint=home_page, dependencies=[])
)

# calibrate
server.router(
    Router(path="/calibrate/u/{user_id}", methods=["GET"], endpoint=calibrate_page, dependencies=[])
)

# capture
server.router(
    Router(path="/capture/u/{user_id}/v/{video_id}", methods=["GET"], endpoint=capture_page, dependencies=[])
)

# monitor
server.router(
    Router(path="/monitor/u/{user_id}", methods=["GET"], endpoint=monitor_page, dependencies=[])
)


# #
# server

app = server.app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "ASDcollector.bin.server:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=True,
    )