from django.http import HttpResponse
from django.views.generic import View


class HomePage(View):
    def get(self, request):
        return HttpResponse('Hello World!')
