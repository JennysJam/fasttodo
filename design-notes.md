# Design notes

## Files and notes
*server.py* which hosts server, *todo.py* hosts the implementation of the app state. *client/* will serve the static appsfiles for app and debug shell.

## Over View

Todos form a tree of todos -- there are top level todos, and they all have subtodos. Each Task (the reification of a todo item) has optionally a short description, some notes that can be freely edited. Completing a task will complete all of it's subtasks, uncompleting a task will uncomplete all of it's subtasks (it might make sense to have a seperate "was this ever actually complete?").

Tasks can also be deleted -- doing so _will_ delete their children. 

## Application State

application will have a library for them but it overall looks like

```py
@dataclass

Id = int

class Task:
    # have we finished it?
    complete: bool 
    # used for api
    parent: Option[Id] 
    # actual in memory transient info
    _parent: Option[Task] 
    # id of childrens
    children: List[Id] 
    # maps IDs to tasks
    _children: Dict[Id, Task] 
     # how many parents you have, 0 - xv
    _depth: int
    name: str # name of task
    # short description (meant to have no newlines ~ 1 sentence)
    description: Option[str] 
     # notes for todo, meant to be updated frequently. 
    notes: Option[str]
```

All tasks are assigned a unique id (could be uuid but im gonna just have incrementing from 0 for now). Tasks use id's for the serialization but actual pointers/memberships.

Top level TodoApp will be a map of Id's -> Todos

## Api Overview

generally using json for marshalling. has top level of api

- *GET* `/api/todo`  
    Returns list of TODOs, used for initial state  
    hypothetically could be list of Ids too

- *POST* `/api/todo`  
    Return ID of new TASK, or error.  
    Body paramters are  
    + Name
    + Description or Null
    + Parent id or null
    + Notes or Null
    + other params to be added...

- *GET* `/api/todo/{ident}`  
    Returns info on individual todo as specifed by id

- *REMOVE* `/api/todo/{ident}`  
    Remove api by ID  
    Returns list of Ids to remove from state (because of child items)

- *PUT* `/api/todo/{ident}/complete`  
    Completes/Uncompletes Task
    Accepts true or false
    Returns list of Ids that are considered also complete

- *PUT* `/api/todo/{ident}/field`  
    Use this to update item values (description, name, string, datetime, urgency, etc,) in place. A value of `null` will be used to set unset it.

## updated api

parent nodes should be passed as path parameters and creation requests should have a simple body (called TaskReq i think), so

- `PUT /api/task`  
    Create new task (toplevel)
- `PUT /api/task/{ident}`
    Create new task with parent as ident


## Client
Client will be a simple 1 page app that takes in data and appends values, which will be a little tree of divs most likely (or articles, semantically?). I think name/description should be shown and notes could be collapsable/scrollable.

## Debug Shell
Actual simple 1 page app with fields (method, url, body) to make XHR requests to the local app and show previous result. I think it would be neat


## Stretch goals

have datetimes and some extra state. more fancy ui elements, collapse items, testing. tagging system. general notes. notifications?
