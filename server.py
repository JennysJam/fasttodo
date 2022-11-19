"""
Server backend for Task app
"""
from task import Task, TaskApp, TaskReq, Id

from fastapi import FastAPI, HTTPException
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


@server.get('/debug/hi')
async def hi():
    return 'hi'


@server.get('/api/task')
async def task_list() -> List[Task]:
    "Return list of tasks"
    return taskapp.get_all()



@server.get('/api/task/{ident}')
async def get_task(ident: Id) -> Task:
    return taskapp.get(ident)


@server.post('/api/task')
async def post_task(body: TaskReq) -> Id:
    "Create new top level task"
    return taskapp.add(body, None).id


@server.post('/api/task/{ident}')
async def post_task_parent(ident: Id, body: TaskReq) -> Id:
    "Create new task with parent ident."
    return taskapp.add(body, ident).id


@server.delete('/api/task/{ident}')
async def delete_task(ident: Id) -> List[Id]:
    raise HTTPException( status_code=501, detail='Task Deletion Not Yet Supported' )

