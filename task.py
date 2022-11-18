from __future__ import annotations

"""
Task Library And Application State
"""

from pydantic import BaseModel
from typing import *

Id = int
UNSETID = -1

"Type alias for ID reference"

class Task(BaseModel):
    "Reification of a task object, used with pydantic."
    name: str
    "Name of task"
    complete: bool
    "If task is complete"
    _id: Id = UNSETID
    "Interanl reference to ID. -1 at first"
    description: Optional[str]
    "Short description of task"
    notes: Optional[str]
    "Freeform notes of activity with task"
    parent: Optional[Id]
    "Optional Id for parent task. If null is toplevel."
    _parent: Optional[Task]
    "Reference to parent, internal implementation"
    children: List[Id]
    "List of child tasks."
    _children: Dict[Id, Task]
    "Map of Id's to Children."


class TaskApp:
    "Internal representation of TaskApp"

    def __init__(self):
        self.tasks: Dict[Id, Task] = dict()
        self._nextid: Id = 0

    def generate_id(self) -> Id:
        "Increment internal count and add new ID"
        res = self._nextid
        self._nextid += 1
        return res

    def get_task(self, ident: Id) -> Optional[Task]:
        "Return task by id or return None"
        return self.tasks.get(ident)
    
    def remove_task_id(self, ident: Id) -> None:
        pass # TODO

    def add(self, task: Task) -> Id:
       "Add newly unmarshalled task. Return ID"
       pass

    def remove(self, task: Task) -> None:
        "Remove task from system."