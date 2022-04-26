import requests

from django.conf import settings
from django.http import Http404

from exporter.core.services import get_organisation
from exporter.goods.services import get_good


class OrganisationMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            organisation_id = str(self.request.session.get("organisation"))
            self.organisation = get_organisation(self.request, organisation_id)
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class GoodMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.good = get_good(self.request, kwargs["pk"], full_detail=True)[0]
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class Product2FlagMixin:
    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        return super().dispatch(request, *args, **kwargs)
