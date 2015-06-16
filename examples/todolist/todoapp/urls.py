from django_ripozo import DjangoDispatcher
from ripozo.adapters import SirenAdapter, HalAdapter
from .resources import TaskBoardResource, TaskResource

dispatcher = DjangoDispatcher(base_url='/api')
dispatcher.register_resources(TaskBoardResource, TaskResource)
dispatcher.register_adapters(SirenAdapter, HalAdapter)

urlpatterns = dispatcher.url_patterns
