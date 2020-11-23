from fbs_runtime.application_context.PyQt5 import ApplicationContext
from core.utils.decorators import Singleton

@Singleton
class AppContext(ApplicationContext):
    def __init__(self):
        super().__init__()