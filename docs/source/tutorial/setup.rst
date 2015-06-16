django-ripozo tutorial
======================

In this tutorial we will create a todo list
application.

Setting up Django
-----------------

*Note* This is not a tutorial for Django.  If you
need some more info on Django please visit:
`the django tutorial <https://docs.djangoproject.com/en/1.8/intro/tutorial01/>`_.

In this tutorial we will create a todo list
application. First we need to install the
necessary dependencies. It is recommended
that you work within a virtualenv.

.. code-block:: bash

    pip install django-ripozo

This should install an appropriate version of Django
as well.

Now we need to create our project and app.

.. code-block:: bash

    django-admin startproject todolist

You'll need to sync your database.

.. code-block:: bash

    python ./manage.py migrate

Now we need to create our todo app.

.. code-block:: bash

    python ./manage.py startapp todoapp

Now in our ``todolist/settings.py`` we will want to
add ``'django_ripozo'`` and ``'todoapp'`` to the
INSTALLED_APPS tuple.

Alright, now we're going to edit the ``todoapp/models.py``
file and add the following models.

.. code-block:: python

    class TaskBoard(models.Model):
        title = models.CharField(max_length=50)


    class Task(models.Model):
        title = models.CharField(max_length=50)
        description = models.TextField()
        completed = models.BooleanField(default=False)
        task_board = models.ForeignKey('TaskBoard', related_name='task_set')

You'll need to run makemigrations and migrate again.

You're now all set up and ready to start building your api.

Creating your managers
----------------------

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
        fields = ('id', 'title', 'description', 'completed', 'task_board_id',)
        model = Task
        paginate_by = 20

That's how simple it is to set up our managers.

Creating your resources
-----------------------

Resources are the core of ripozo.  These are common
across all manager and dispatcher packages.  This means,
assuming that the application was developed well, you could
reuse the resources in flask or mix them in with the sqlalchemy
manager.

The first thing we are going to do is create a file in the todoapp
directory called ``resources.py``.  Then we will add the following

.. code-block:: python

    from ripozo import restmixins, ListRelationship, Relationship, apimethod
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
            Relationship('task_board', property_map=dict(task_board_id='id'), relation='TaskBoardResource'),
        )



We now have a reusable core to our RESTful API.  This is reusable across
various web frameworks, databases (you will have to change the manager),
or REST protocol.


Setting up your dispatcher.
---------------------------

The dispatcher is responsible for translating the
request into something that the framework (Django)
can understand and translating the ripozo response
into the frameworks preferred method.  First create a ``urls.py`` file
in your todoapp directory.  In that file:

.. code-block:: python

    from django_ripozo import DjangoDispatcher
    from ripozo.adapters import SirenAdapter, HalAdapter
    from .resources import TaskBoardResource, TaskResource

    dispatcher = DjangoDispatcher(base_url='/api')
    dispatcher.register_resources(TaskBoardResource, TaskResource)
    dispatcher.register_adapters(SirenAdapter, HalAdapter)

    urlpatterns = dispatcher.url_patterns

And right there you've set up your url patterns
and registered the resources with the application.


