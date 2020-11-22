import uuid

class Model:
    def __init__(self, **io):
        self.objects = {}
        self.subscriptions = {}
        self.subscriptions_index = -1
        self.loader = io.get('loader', lambda: [])
        self.saver = io.get('saver', lambda: None)

    def load(self):
        for obj in self.loader():
            if 'id' in obj:
                self.objects[obj['id']] = obj
            else:
                id = uuid.uuid1()
                self.objects[id] = obj

    def save(self):
        return self.saver(self.objects)

    def all(self):
        return [obj for obj in self.objects.values()]

    def create(self, **kwargs):
        id = uuid.uuid1()
        obj = { 'id': id, **kwargs }

        self.objects[id] = obj

        return id

    def find(self, id):
        return self.objects[id]

    def find_by(self, **kwargs):
        for obj_key in self.objects:
            found_object = all([kwargs[key] == self.objects[obj_key].get(key) for key in kwargs])

            if found_object:
                return self.objects[obj_key]

        return None

    def update(self, id, **kwargs):
        self.objects[id].update(kwargs)

    def delete(self, id):
        return self.objects.pop(id)

    def subscribe(self, func):
        self.subscriptions_index += 1

        func_index = str(self.subscriptions_index)
        self.subscriptions[func_index] = func

        def unsubscribe():
            self.subscriptions.pop(func_index)

        return unsubscribe

    def broadcast(self, data):
        for func in self.subscriptions.values():
            func(data)