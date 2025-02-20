from django.shortcuts import render
from main import models

def index(request):
    leads = models.Lead.objects.filter(is_active=True)
    status = models.Status.objects.all()
    context = {
        'leads': leads,
        'status': status
    }
    return render(request, 'index.html', context)
