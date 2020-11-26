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


class MockSignal():
    def __init__(self):
        self.funcs = []

    def connect(self, func):
        self.funcs.append(func)

class MockWorker():
    def __init__(self):
        self.finished = MockSignal()
    def start(self):
        for func in self.finished.funcs:
            func()
            

def test_happy_path():
    pool = WorkerPool.Instance()
    worker = MockWorker()
    
    pool.start(worker)

    assert(pool.pool == {})