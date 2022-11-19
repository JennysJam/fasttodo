from __future__ import annotations

"""
Task Library And Application State
"""

from pydantic import BaseModel, PrivateAttr
from typing import *

Id = int
"Type alias for ID reference"

UNSETID = -1

class TaskReq(BaseModel):
    "Object used to request creation of an task."
    name: str
    "Name of task"    
    description: Optional[str]
    "Short description of task"
    notes: Optional[str]
    "Freeform notes of activity with task"


class Task(BaseModel):
    "Reification of a task object, with known ideas."

    name: str
    "Name of task"
    description: Optional[str]
    "Short description of task"
    notes: Optional[str]
    "Freeform notes of activity with task"

    complete: bool
    "If task is complete"
    id: Id
    "ID of object"


    parent: Optional[Id]
    "Optional Id for parent task. If null is toplevel."
    _parent: Optional[Task] = PrivateAttr(default=None)
    "Reference to parent, internal implementation"

    children: List[Id]
    "List of child tasks."
    _children: List[Task] = PrivateAttr(default_factory=list)
    "List of child tasks."

    @staticmethod
    def from_req(req: TaskReq, id: Id, parent: Optional[Task]) -> Task:
        """
        Construct Task from TaskReq

        Args:
            req: A task request
            id: The identifier to be used by the item
            parent: optionally, the parent item

        Returns:
            A newly constructed Task 
        """

        return Task(
            id= id,
            name = req.name,
            description = req.description,
            notes = req.notes,

            complete = False,
            

            parent = parent.id if parent is not None else None,
            _parent = parent,

            children = [],
            _children = []
        )

    def append_child(self, task: Task):
        "Append a child to this element"
        self.children.append(task.id)
        self._children.append(task)


class TaskApp:
    "Internal representation of TaskApp"

    def __init__(self):
        self.lookup_table: Dict[Id, Task] = dict()
        self.toplevel: List[Task] = list()
        self._nextid: Id = 0

    def get_all(self) -> List[Task]:
        "Return a list of all tasks in Task App"
        return list(self.lookup_table.values())

    def generate_id(self) -> Id:
        "Increment internal count and add new ID"
        res = self._nextid
        self._nextid += 1
        return res

    def get(self, id: Id) -> Task:
        "Get task by Id. Throws on errors"
        return self.lookup_table[id]

    def add(self, req: TaskReq, parent_id: Optional[Id]) -> Task:
        "Add new task from Task Request. Throws on errors"
        
        if parent_id is not None:
            parent = self.get(parent_id)
        else:
            parent = None
        
        # generate new id 
        newid = self.generate_id()

        result = Task.from_req(req, newid, parent)
        
        if parent is not None: 
            parent.append_child(result)

        self.lookup_table[newid] = result
        if parent is None:
            self.toplevel.append(result)
        
        return result