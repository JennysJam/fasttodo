"""
Server backend for Task app
"""
from task import Task, TaskApp, Id

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from typing import *

# top level internal state
server = FastAPI()

taskapp = TaskApp()

# mount static files
server.mount('/client', StaticFiles(directory='client'), name='client')


# endpoints
@server.get('/')
async def index():
    "Top level entry point, routes to client name"
    return RedirectResponse('/client/index.html')


@server.get('/debug')
async def debugger():
    "Top level short cut for utility debugger/terminal"
    return RedirectResponse('/client/debug.html')

@server.get('/api/hi')
async def hi():
    return 'hi'

@server.get('/api/task')
async def task_list() -> List[Task]:
    "Return list of tasks"
    pass


@server.get('/api/task/{ident}')
async def get_task(ident: Id) -> Task:
    pass


@server.post('/api/task/')
async def post_task(body: Task) -> Id:
    pass


@server.delete('/api/task/{ident}')
async def delete_task(ident: Id) -> List[Id]:
    pass

