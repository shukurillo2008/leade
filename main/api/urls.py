from django.urls import path, include
from . import views

urlpatterns = [
    #auth and docs
    path('auth/', include('main.api.auth.urls')),
    
    #status
    path('status/', views.StatusApiView.as_view(), name='status_url'),
    path('lead-type/', views.LeadTypeApiView.as_view(), name='lead_type_url'),
    path('lead/', views.LeadApiView.as_view(), name='lead_url'),
    path('lead-history/', views.LeadHistoryApiView.as_view(), name='lead_history_url'),
]
