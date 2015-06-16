from ripozo import restmixins, ListRelationship, Relationship
from .managers import TaskBoardManager, TaskManager

class TaskBoardResource(restmixins.CRUDL):
    manager = TaskBoardManager()
    resource_name = 'taskboard'
    pks = ('id',)
    _relationships = (
        ListRelationship('task_set', relation='TaskResource'),
    )

    # We're going to add a simple way to add
    # tasks to a board by extending the
    @apimethod(route='/addtask', methods=['POST'])
    def add_task(cls, request):
        body_args = request.body_args
        body_args['task_board_id'] = request.get('id')
        request.body_args = body_args
        return TaskResource.create(request)

class TaskResource(restmixins.CRUD):
    manager = TaskManager()
    resource_name = 'task'
    pks = ('id',)
    _relationships = (
        Relationship('task_board', relation='TaskBoardResource'),
    )
