Creating your managers
======================

Managers are responsible for handling access
to the django models that you just created.
To start we are going to create a new file in
the todoapp called ``managers.py``.  After that
we are going to set up our managers.

.. code-block:: python

    from django_ripozo import DjangoManager
    from .models import TaskBoard, Task

    class TaskBoardManager(DjangoManager):
        # These are the default fields to use when performing any action
        fields = ('id', 'title', 'task_set.id',)
        update_fields = ('title',) # These are the only fields allowed when updating.
        model = TaskBoard
        paginate_by = 10

    class TaskManager(DjangoManager):
        fields = ('id', 'title', 'description', 'completed', 'task_board.id',)
        model = Task
        paginate_by = 20

That's how simple it is to set up our managers.