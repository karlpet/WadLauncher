from app.workers.WorkerPool import *

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
