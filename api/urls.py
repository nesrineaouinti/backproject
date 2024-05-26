from django.urls import path
from .views import *
from.tests import *

urlpatterns = [ #les liens hedhom bech ykono fi react ,link mi react lel views
    path("", hello_view, name="note-list"),  
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:pk>/update/', JobUpdateView.as_view(), name='job-update'),
    path('jobs/<int:pk>/delete/', JobDeleteView.as_view(), name='job-delete'),

    path('email/', SendEmailAPI.as_view(), name='send-email'),

    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/create/<int:job_id>/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-delete'),
    path('applications/byjob/<int:job_id>/', ApplicationsByJobView.as_view(), name='applications-by-job'),
    
    path('contact/create/', ContactCreateView.as_view(), name='contact-create'),
    path('statistique/', JobApplicationStatsView.as_view(), name='job-application-stats'),
    #here the /delete just to calirfy , it does nothing , what really triggers the delete is the axios.delete in frontend which goes to the view and automatically triggers the delete
       


]