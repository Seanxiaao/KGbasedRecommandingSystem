from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.


class Index(View):

    TEMPLATE = 'index.html'

    def get(self, request):
        return render(request, self.TEMPLATE)