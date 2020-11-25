from core.utils.decorators import Singleton

@Singleton
class WorkerPool:
    def __init__(self):
        self.pool = {}
        self.worker_id = 0
    
    def start(self, worker):
        self.worker_id += 1
        worker_id = self.worker_id
        self.pool[worker_id] = worker
        worker.finished.connect(lambda: self.remove(worker_id))
        worker.start()
    
    def remove(self, worker_id):
        self.pool.pop(worker_id)
