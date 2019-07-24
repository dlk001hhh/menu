from haystack import indexes
from myApp.models import Dish


class DishIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Dish

    def index_queryset(self, using=None):
        return self.get_model().objects.all()