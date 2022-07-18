from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView


class ProductSearchView(TemplateView):
    template_name = "search/products.html"

    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_SEARCH:
            raise Http404("No feature flag")

        return super().dispatch(*args, **kwargs)
