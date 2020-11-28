import sys

from app.views.WadTreeView import WadTreeView

class WadTreeController:
    def show(self, root, models):
        self.models = models
        self.view = WadTreeView(root, models, self)

    def remove_category(self, category, children):
        parent_id = category.get('category_id')
        for child in children:
            model = getattr(self.models, child['model_type'])
            model.update(child['id'], category_id=parent_id)
            model.save(child['id'])
        self.models.categories.remove(category['id'])

sys.modules[__name__] = WadTreeController()