Setting up Django
=================

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
        task_board = models.ForeignKey('TaskBoard')

You'll need to run makemigrations and migrate again.

You're now all set up and ready to start building your api.


