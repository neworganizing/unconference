import json
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Organization


class ListOrganizations(ListView):
    model = Organization

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            json.dumps(str(self.get_queryset().values())),
            mimetype="application/json"
        )
