from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pypermedia.client import HypermediaClient
import requests


if __name__ == '__main__':
    siren_client = HypermediaClient.connect('http://localhost:8000/api/taskboard/', request_factory=requests.Request)
    task_board_list = siren_client.retrieve_list()
    created = task_board_list.create(title='My First Board')

    retrieve = created.retrieve()
    print(created.title)
    print(created.id)

    updated = retrieve.update(title='My Updated Board')
    print(updated.title)

    new_task = updated.add_task(title='My first task', description='I need to do something')
    print(new_task.title)
    print(new_task.description)
    print(new_task.completed)

    task_board = retrieve.retrieve()

    task = next(task_board.get_entities('task_set'))
    print(task.description)
    print(task.completed)

    task = task.update(completed=True)
    print(task.completed)

    parent_board = next(task.get_entities('task_board'))
    print(parent_board.title)

    deleted = task.delete()

    original_task = task.retrieve()
    print(original_task)
