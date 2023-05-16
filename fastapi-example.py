from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
import uvicorn
from autometrics import (
    autometrics,
    get_autometrics_admin_html,
)
from prometheus_client import generate_latest

app = FastAPI()


# Set up a metrics endpoint for Prometheus to scrape
# `generate_lates` returns the latest metrics data in the Prometheus text format
@app.get("/metrics")
def metrics():
    return Response(generate_latest())


@app.get("/")
@autometrics
def read_root():
    do_something()
    return {"Hello": "World"}


@app.get("/async-test")
@autometrics
async def async_test_route():
    message = await my_async_function()
    return {"Hello": message}


# HACK - add the admin panel UI manually
@autometrics
@app.get("/autometrics/admin", response_class=HTMLResponse)
def autometrics_admin():
    return get_autometrics_admin_html()


@autometrics
def do_something():
    print("I did something")


@autometrics
async def my_async_function():
    print("I did something async")
    return "Hello, async world!"


@autometrics
def my_new_function_with_args(arg1, arg2):
    print("I did something with args")
    return f"Hello, {arg1} and {arg2}!"


if __name__ == "__main__":
    # run_admin_server()  # FIXME - server dies
    uvicorn.run(app, host="localhost", port=8080)
