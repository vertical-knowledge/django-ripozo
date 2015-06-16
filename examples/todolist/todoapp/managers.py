from django_ripozo import DjangoManager
from .models import TaskBoard, Task

class TaskBoardManager(DjangoManager):
    # These are the default fields to use when performing any action
    fields = ('id', 'title', 'task_set.id',)
    update_fields = ('title',) # These are the only fields allowed when updating.
    model = TaskBoard
    paginate_by = 10

class TaskManager(DjangoManager):
    fields = ('id', 'title', 'description', 'completed', 'task_board_id',)
    model = Task
    paginate_by = 20
