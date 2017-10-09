from haystack import indexes
from newsApp.models import Article

class NewsIndex(indexes.SearchIndex, indexes.Indexable):
   
    text = indexes.CharField(document=True, use_template=True)


    headline = indexes.CharField(model_attr='headline')
    media = indexes.CharField(model_attr='source')
    content = indexes.CharField(model_attr='content')
    article_id = indexes.CharField(model_attr='id')
    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""

        return self.get_model().objects.all()